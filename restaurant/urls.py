from django.urls import path
from .views import indexPage, CreateAccountView, deleteAccountView, showSampleView, commentView, subscribtionView, reservationView
urlpatterns = [
    path("index", indexPage, name="indexPage"),
    path("createAccount", CreateAccountView, name="createAccount"),
    path("deleteAccount", deleteAccountView, name="deleteAccount"),
    path("index/<int:id>", showSampleView, name="showSample"),
    path("comment", commentView, name="comment"),
    path("subscribtion", subscribtionView, name="subscribtion"),
    path("reservation", reservationView, name="reservation")
]
