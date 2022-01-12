from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.views.generic.edit import BaseCreateView
from django.views.generic.list import BaseListView
from mptt.forms import TreeNodeChoiceField

from .models import *


class AddUserForm(UserCreationForm, forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    year = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'tel'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['posts'].empty_label = "Должность не выбрана"

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 20:
    #         raise ValidationError('Длина привышает 200 слов')
    #     return title
    # parent = UserData.objects.get(id=request.user.id)
    # category = TreeNodeChoiceField(queryset=parent.get_descendants(),
    #                                start_level=parent.level)

    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'patronymic', 'last_name',
                  'year', 'phone', 'email', 'password1',
                  'password2', 'is_clients', 'is_workers', 'is_images', 'is_document',
                  'is_password', 'posts']
        widgets = {
            # 'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

# class EditForm(forms.ModelForm):
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.fields['cat'].empty_label = "Категория не выбрана"
#
#     class Meta:
#         model = Container
#         fields = ['url', 'name', 'password']
#         widgets = {
#             # 'title': forms.TextInput(attrs={'class': 'form-input'}),
#             'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
#         }


class ClientForm(forms.ModelForm):
    year = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input', 'type': 'tel'}))
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'year', 'phone']
        widgets = {
            # 'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class PassContForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Container
        fields = ['url', 'name', 'password']
        widgets = {
            # 'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class AddPostsForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Posts
        fields = ['name']
        widgets = {
            # 'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


# class AddUserForm(forms.ModelForm):
#
#         # def __init__(self, *args, **kwargs):
#         #     super().__init__(*args, **kwargs)
#         #     self.fields['cat'].empty_label = "Категория не выбрана"
#
#     class Meta:
#         model = UserData
#         fields = ['year', 'phone', 'is_clients', 'is_workers']
#         widgets = {
#             # 'title': forms.TextInput(attrs={'class': 'form-input'}),
#             'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
#         }
# def clean_title(self):
#     title = self.cleaned_data['title']
#     if len(title) > 20:
#         raise ValidationError('Длина привышает 200 слов')
#     return title

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = "__all__"

class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': "name@example.com"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input-login'}))


    class Meta:
        model = UserData
        fields = ('username', 'password')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input-reg'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input-reg', 'placeholder': "name@example.com"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input-reg'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input-reg'}))
    department = forms.CharField(label='Название отдела', widget=forms.TextInput(attrs={'class': 'form-input-reg'}))

    class Meta:
        model = UserData

        fields = ('username', 'email', 'password1', 'password2', 'department')

