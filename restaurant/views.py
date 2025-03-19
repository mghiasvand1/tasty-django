from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateAccountForm, SendFeedbackForm, ReservationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Newsletter, Menu, Gallery, SpecialFood, Blog, CountBlogViews, Comment, Reservation
from django.utils.timezone import datetime
from django.utils.translation import get_language_from_request
from ip2geotools.databases.noncommercial import DbIpCity
from countryinfo import CountryInfo

def indexPage(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    userLocation = DbIpCity.get(ip, api_key='free')
    userCountry = userLocation.country
    userCountryLanguageCode = CountryInfo(userCountry).languages()[0]
    breakfastOmelettesMenu = Menu.objects.all().filter(category="omelettes", meal="BREAKFAST")
    breakfastWaffleMenu = Menu.objects.all().filter(category="waffle", meal="BREAKFAST")
    lunchAppetizersMenu = Menu.objects.all().filter(category="appetizers", meal="LUNCH")
    lunchMainMenu = Menu.objects.all().filter(category="main", meal="LUNCH")
    lunchKidsMenu = Menu.objects.all().filter(category="kids", meal="LUNCH")
    lunchPizzaMenu = Menu.objects.all().filter(category="pizza", meal="LUNCH")
    dessertCheesecakeMenu = Menu.objects.all().filter(category="cheesecake", meal="DESSERT")
    dessertIcecreamMenu = Menu.objects.all().filter(category="icecream", meal="DESSERT")
    dessertSpecialtyMenu = Menu.objects.all().filter(category="specialty", meal="DESSERT")
    beveragesIceddrinksMenu = Menu.objects.all().filter(category="iceddrinks", meal="BEVERAGES")
    beveragesHotdrinksMenu = Menu.objects.all().filter(category="hotdrinks", meal="BEVERAGES")
    galleryImages= Gallery.objects.all()
    special = SpecialFood.objects.last()
    specialBreakfastImageName = special.breakfastPicture.url.split("/")[5]
    specialLunchImageName = special.lunchPicture.url.split("/")[5]
    specialBeverageImageName = special.beveragePicture.url.split("/")[5]
    blogs = Blog.objects.all()
    comments = Comment.objects.all().filter(status="SHOW")
    context = {
        'userCountryLanguageCode':userCountryLanguageCode,
        'breakfastOmelettesMenu':breakfastOmelettesMenu,
        'breakfastWaffleMenu':breakfastWaffleMenu,
        'lunchAppetizersMenu':lunchAppetizersMenu,
        'lunchMainMenu':lunchMainMenu,
        'lunchKidsMenu':lunchKidsMenu,
        'lunchPizzaMenu':lunchPizzaMenu,
        'dessertCheesecakeMenu':dessertCheesecakeMenu,
        'dessertIcecreamMenu':dessertIcecreamMenu,
        'dessertSpecialtyMenu':dessertSpecialtyMenu,
        'beveragesIceddrinksMenu':beveragesIceddrinksMenu,
        'beveragesHotdrinksMenu':beveragesHotdrinksMenu,
        'galleryImages':galleryImages,
        'special':special,
        'specialBreakfastImageName':specialBreakfastImageName,
        'specialLunchImageName':specialLunchImageName ,
        'specialBeverageImageName':specialBeverageImageName,
        'blogs':blogs,
        'comments':comments,
        }
    return render(request, "restaurant/index.html", context)


def CreateAccountView(request):
    if request.user.is_authenticated == False:
        form = CreateAccountForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            User.objects.create(username=username, email=email, password=password)
            user = User.objects.get(username=username, email=email, password=password)
            login(request, user)
            availableInNewsletter = Newsletter.objects.all().filter(username=username)
            if availableInNewsletter.exists() == False:
                Newsletter.objects.create(username=username, email=email, subscribtion=True)
            return redirect("indexPage")
        context = {"form": form}
        return render(request, "restaurant/createAccount.html", context)
    else:
        return render(request, "restaurant/403.html")


def deleteAccountView(request):
    userId = request.user.id
    username = request.user.username
    wholeUsers = User.objects.all()
    wholeUsersId = []
    for user in wholeUsers:
        wholeUsersId.append(user.id)
    userIndexId = wholeUsersId.index(userId)
    newsletterObject = Newsletter.objects.get(username=username)
    newsletterObject.delete()
    User.objects.all()[userIndexId].delete()
    return redirect("indexPage")

def error404(request, exception):
    return render(request, 'restaurant/404.html')
    
def error403(request, exception):
    return render(request, 'restaurant/403.html')
 
def showSampleView(request, id):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    userLocation = DbIpCity.get('206.71.50.230', api_key='free')
    # 206.71.50.230 USA
    # 109.71.40.0 Portugal
    # 103.130.144.0 Iran
    # 18.184.170.128 Germany
    #  ip
    userCountry = userLocation.country
    userCountryLanguageCode = CountryInfo(userCountry).languages()[0]
    blog = get_object_or_404(Blog, id=id)
    if request.user.is_authenticated:
        if blog is not None:
            username = request.user.username
            checkRecent = CountBlogViews.objects.all().filter(blogId=id, username=username)
            if checkRecent.exists()==False:
                blog.views += 1
                blog.save()
                CountBlogViews.objects.create(blogId = id ,username=username)
                blogPicture = blog.picture.url.split("/")[5]
                context = {
                    'userCountryLanguageCode':userCountryLanguageCode,
                    'blog':blog,
                    'blogPicture':blogPicture,
                }
                return render(request,'restaurant/sample.html', context)
            else:
                blogPicture = blog.picture.url.split("/")[5]
                context = {
                    'userCountryLanguageCode':userCountryLanguageCode,
                    'blog':blog,
                    'blogPicture':blogPicture,
                }
                return render(request,'restaurant/sample.html', context)
        else:
            raise Http404
    else:
        return redirect("createAccount")


def commentView(request):
    if request.user.is_authenticated:
        form = SendFeedbackForm(request.POST or None)
        if form.is_valid():
            title = form.cleaned_data["title"]
            star = form.cleaned_data["star"]
            message = form.cleaned_data["message"]
            Comment.objects.create(title=title, star=star, message=message, status="NOT SEEN YET")
            return redirect("indexPage")
        context = {"form": form}
        return render(request, "restaurant/comment.html", context)
    else:
        return redirect("createAccount")

def subscribtionView(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        username = request.user.username
        user = Newsletter.objects.get(username=username)
        if user.subscribtion == True:
            user.subscribtion = False
            user.save()
            status='subscribe'
        else:
            user.subscribtion = True
            user.save()
            status='unsubscribe'
    else:
        return redirect("createAccount")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    userLocation = DbIpCity.get('206.71.50.230', api_key='free')
    # 206.71.50.230 USA
    # 109.71.40.0 Portugal
    # 103.130.144.0 Iran
    # 18.184.170.128 Germany
    #  ip
    userCountry = userLocation.country
    userCountryLanguageCode = CountryInfo(userCountry).languages()[0]
    breakfastOmelettesMenu = Menu.objects.all().filter(category="omelettes", meal="BREAKFAST")
    breakfastWaffleMenu = Menu.objects.all().filter(category="waffle", meal="BREAKFAST")
    lunchAppetizersMenu = Menu.objects.all().filter(category="appetizers", meal="LUNCH")
    lunchMainMenu = Menu.objects.all().filter(category="main", meal="LUNCH")
    lunchKidsMenu = Menu.objects.all().filter(category="kids", meal="LUNCH")
    lunchPizzaMenu = Menu.objects.all().filter(category="pizza", meal="LUNCH")
    dessertCheesecakeMenu = Menu.objects.all().filter(category="cheesecake", meal="DESSERT")
    dessertIcecreamMenu = Menu.objects.all().filter(category="icecream", meal="DESSERT")
    dessertSpecialtyMenu = Menu.objects.all().filter(category="specialty", meal="DESSERT")
    beveragesIceddrinksMenu = Menu.objects.all().filter(category="iceddrinks", meal="BEVERAGES")
    beveragesHotdrinksMenu = Menu.objects.all().filter(category="hotdrinks", meal="BEVERAGES")
    galleryImages= Gallery.objects.all()
    special = SpecialFood.objects.last()
    specialBreakfastImageName = special.breakfastPicture.url.split("/")[5]
    specialLunchImageName = special.lunchPicture.url.split("/")[5]
    specialBeverageImageName = special.beveragePicture.url.split("/")[5]
    blogs = Blog.objects.all()
    comments = Comment.objects.all().filter(status="SHOW")
    context={
        'userCountryLanguageCode':userCountryLanguageCode,
        'status':status,
        'breakfastOmelettesMenu':breakfastOmelettesMenu,
        'breakfastWaffleMenu':breakfastWaffleMenu,
        'lunchAppetizersMenu':lunchAppetizersMenu,
        'lunchMainMenu':lunchMainMenu,
        'lunchKidsMenu':lunchKidsMenu,
        'lunchPizzaMenu':lunchPizzaMenu,
        'dessertCheesecakeMenu':dessertCheesecakeMenu,
        'dessertIcecreamMenu':dessertIcecreamMenu,
        'dessertSpecialtyMenu':dessertSpecialtyMenu,
        'beveragesIceddrinksMenu':beveragesIceddrinksMenu,
        'beveragesHotdrinksMenu':beveragesHotdrinksMenu,
        'galleryImages':galleryImages,
        'special':special,
        'specialBreakfastImageName':specialBreakfastImageName,
        'specialLunchImageName':specialLunchImageName ,
        'specialBeverageImageName':specialBeverageImageName,
        'blogs':blogs,
        'comments':comments,
    }
    return render(request, "restaurant/index.html", context)


def reservationView(request):
    form = ReservationForm(request.POST or None)
    if form.is_valid() and request.user.is_authenticated and request.method == "POST":
        email = request.user.email
        phone = form.cleaned_data["phone"]
        personnumber = form.cleaned_data["personnumber"]
        tabletype = form.cleaned_data["tabletype"]
        meal = form.cleaned_data["meal"]
        date = datetime.now()
        Reservation.objects.create(email=email, phone=phone, personnumber=personnumber, tabletype=tabletype, date=date, meal=meal, acceptance="NOT SEEN YET")
        return redirect("indexPage")
    elif not request.user.is_authenticated:
        return redirect("createAccount")
    context = {"form": form}
    return render(request, "restaurant/reservation.html", context)