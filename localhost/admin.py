from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'year', 'is_workers', 'is_clients', 'is_password', 'posts')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'time_create')
    list_editable = ('is_workers', 'is_clients')
    list_filter = ('parent', 'time_create', 'posts')
    # prepopulated_fields = {"slug": ("title",)}


# class PersonalAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'phone', 'year', 'time_create', 'time_update')
#     list_display_links = ('id', 'first_name', 'phone')
#     search_fields = ('first_name', 'year', 'time_create', 'phone', 'year', 'time_create', 'time_update')
#     # prepopulated_fields = {"slug": ("name",)}


class PostsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    # list_display_links = ('id', 'name')
    search_fields = ('name',)
    # prepopulated_fields = {"slug": ("name",)}


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'password', 'time_create', 'time_update')
    list_display_links = ('name',)
    search_fields = ('name', 'time_create')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'phone', 'year')
    list_display_links = ('last_name',)
    search_fields = ('phone', 'last_name')


class CardsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'credit', 'time_create', 'time_update', 'client_cards')
    list_display_links = ('number',)
    search_fields = ('number', 'client_cards')


class OperationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'key', 'credit', 'time_create', 'operation_cards', 'operation_cards')
    list_display_links = ('key', 'operation_cards')
    search_fields = ('key', 'operation_cards')


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Container, ContainerAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Cards, CardsAdmin)
admin.site.register(Operation, OperationAdmin)

# admin.site.register(Personal, PersonalAdmin)
