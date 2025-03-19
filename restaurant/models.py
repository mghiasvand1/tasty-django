from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.mail import send_mail



class Reservation(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    personnumber = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False
    )
    tabletype = models.CharField(max_length=10, null=False, blank=False, choices=[("NORMAl", "NORMAL"), ("SPECIAL", "SPECIAL")])
    date = models.DateField(blank=True, null=True)
    meal = models.CharField(max_length=10, blank=False, null=False)
    acceptance =  models.CharField(max_length=100, null=False, blank=False, choices=[("ACCEPTED", "ACCEPTED"), ("NOT ACCEPTED", "NOT ACCEPTED"), ("NOT SEEN YET", "NOT SEEN YET")])

    def __str__(self):
        return self.email




class Comment(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    message = models.CharField(max_length=200, blank=False, null=False)
    star = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, null=False
    )
    status = models.CharField(
        max_length=9,
        choices=[("SHOW", "SHOW"), ("NOT SHOW", "NOT SHOW")],
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["-star"]

        def __str__(self):
            return self.title




class Menu(models.Model):
    meal = models.CharField(
        max_length=10,
        choices=[
            ("BREAKFAST", "BREAKFAST"),
            ("LUNCH", "LUNCH"),
            ("DESSERT", "DESSERT"),
            ("BEVERAGES", "BEVERAGES"),
        ],
        blank=False,
        null=False,
    )
    name = models.CharField(max_length=30, blank=False, null=False)
    category = models.CharField(max_length=30, choices=[("omelettes", "omelettes"), ("waffle", "waffle"), ("appetizers", "appetizers"), ("kids", "kids"), ("main", "main"), ("pizza", "pizza"), ("cheesecake", "cheesecake"), ("icecream", "icecream"), ("specialty", "specialty"), ("iceddrinks", "iceddrinks"), ("hotdrinks", "hotdrinks")], blank=False, null=False)
    ingredient = models.CharField(max_length=70, blank=False, null=False)
    price = models.IntegerField(
        validators=[MinValueValidator(5)], blank=False, null=False
    )

    def __str__(self):
        return self.name




class Gallery(models.Model):
    picture = models.ImageField(
        upload_to="restaurant/static/restaurant/img/", blank=False, null=False
    )


class Newsletter(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    subscribtion = models.BooleanField(null=False, blank=False)



class Blog(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    summary = models.CharField(max_length=200, blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    picture = models.ImageField(blank=False, null=False, upload_to="restaurant/static/restaurant/img/")
    views = models.PositiveIntegerField(default=0)
    date = models.DateField(blank=False, null=False, default=timezone.now)

    class Meta:
        ordering = ["-date"]
        def __str__(self):
            return self.title



class SpecialFood(models.Model):
    breakfastName = models.CharField(max_length=30, blank=False, null=False)
    breakfastIngredients = models.CharField(max_length=70, blank=False, null=False)
    breakfastPrice = models.IntegerField(
        validators=[MinValueValidator(5)], blank=False, null=False
    )
    breakfastPicture = models.ImageField(blank=False, null=False, upload_to="restaurant/static/restaurant/img/")
    lunchName = models.CharField(max_length=30, blank=False, null=False)
    lunchIngredients = models.CharField(max_length=70, blank=False, null=False)
    lunchPrice = models.IntegerField(
        validators=[MinValueValidator(5)], blank=False, null=False
    )
    lunchPicture = models.ImageField(blank=False, null=False, upload_to="restaurant/static/restaurant/img/")
    beverageName = models.CharField(max_length=30, blank=False, null=False)
    beverageIngredients = models.CharField(max_length=70, blank=False, null=False)
    beveragePrice = models.IntegerField(
        validators=[MinValueValidator(5)], blank=False, null=False
    )
    beveragePicture = models.ImageField(blank=False, null=False, upload_to="restaurant/static/restaurant/img/")

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        subscribedUsers = Newsletter.objects.all().filter(subscribtion=True)
        subscribedEmails = []
        for user in subscribedUsers:
            subscribedEmails.append(user.email)
        send_mail('Tasty special food', 'Please visit Tasty website to see the special food .', 'mohammadmohammadkhani82@gmail.com', subscribedEmails, fail_silently=False,)




class CountBlogViews(models.Model):
    blogId = models.PositiveIntegerField(null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)