from django.contrib import admin
from .models import Menu, Gallery, Reservation, Comment, Newsletter, SpecialFood, Blog
from django.core.mail import send_mail
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "is_superuser"]
    search_fields = ["username"]
    list_filter = ["date_joined"]
    readonly_fields = ["username", "email", "password", "first_name", "last_name"]

    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["email", "date", "acceptance", "phone"]
    list_filter = ["date", "meal"]
    search_fields = ["email"]
    readonly_fields = ["email", "phone", "date"]

    def has_add_permission(self, request, obj=None):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ["title", "star"]
    list_filter = ["star"]
    search_fields = ["title"]
    readonly_fields = ["title", "star", "message"]

    def has_add_permission(self, request, obj=None):
        return False
    # def has_change_permission(self, request, obj=None):
    #     return False


class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_filter = ["meal", "price"]
    search_fields = ["name"]


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["username", "subscribtion"]
    search_fields = ["username"]
    readonly_field = ["username", "subscribtion"]

    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "views", "date"]
    list_filter = ["views", "date"]
    search_fields = ["title"]
    readonly_fields = ["views", "date"]


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Gallery)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(SpecialFood)
