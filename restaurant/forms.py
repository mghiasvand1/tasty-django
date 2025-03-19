from django import forms
from django.contrib.auth.models import User
from .models import Comment, Reservation


class CreateAccountForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "id": "password"})
    )
    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmPassword"]

    def clean(self):
        cleanedData = super(CreateAccountForm, self).clean()
        password = cleanedData.get("password")
        confirmPassword = cleanedData.get("confirmPassword")
        if password != confirmPassword:
            raise forms.ValidationError("Two given passwords do not match together .")

class SendFeedbackForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title", "class":"form-control"})
    )
    star = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Star", "class":"form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message", "class":"form-control", 'rows':3, 'cols':15}))
    class Meta:
        model = Comment
        fields = ["title", "star", "message"]

class ReservationForm(forms.ModelForm):
    phone = forms.CharField()
    personnumber = forms.CharField()
    choices1 = [("SPECIAL", "SPECIAL"), ("NORMAL", "NORMAL")]
    choices2=[("BREAKFAST", "BREAKFAST"),("LUNCH", "LUNCH"),("DESSERT", "DESSERT"),("BEVERAGES", "BEVERAGES"),]
    tabletype = forms.CharField(widget=forms.Select(choices=choices1))
    meal = forms.CharField(widget=forms.Select(choices=choices2))
    date = forms.DateField()
    class Meta:
        model = Reservation
        fields = ["phone", "personnumber", "tabletype", "meal", "date"]