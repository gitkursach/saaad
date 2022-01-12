import os
from datetime import datetime

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.fields import TreeManyToManyField
from mptt.models import MPTTModel, TreeForeignKey

from localhost.formatChecker import ContentTypeRestrictedFileField


class UserData(MPTTModel, AbstractUser, models.Model):
    patronymic = models.CharField(max_length=128, db_index=True, verbose_name="Отчество")
    department = models.CharField(max_length=128, db_index=True,null=True, verbose_name="Отдел")
    year = models.DateField(null=True, verbose_name="Дата рождения")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона необходимо вводить в формате: '+7999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    is_clients = models.BooleanField(default=True, verbose_name="Упр Клиентами")
    is_workers = models.BooleanField(default=True, verbose_name="Упр Сотруднкками")
    is_password = models.BooleanField(default=True, verbose_name="Упр Паролями")
    is_images = models.BooleanField(default=True, verbose_name="Упр Изображениями")
    is_document = models.BooleanField(default=True, verbose_name="Упр Документами")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    posts = models.ForeignKey(
        'Posts',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Должность_id")
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Закреплен_за_id",
        related_name="Закреплен_за")

    objects = UserManager()


    class MPTTMeta:
        order_insertion_by = ['username']



    # def get_absolute_url(self):
    #     return reverse('parent', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'
        ordering = ['time_create', ]

# class Department(models.Model):
#     name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
#     user_depart = models.ForeignKey(
#         'UserData',
#         on_delete=models.PROTECT,
#         null=True,
#         blank=True,
#         verbose_name="user_depart_id")
def file_size_img(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Ваше изображение больше 10 Mb.')

def directory_path(instance, filename):
    return 'users_photo/{0}/{1}'.format(instance.pk, filename)
class Output_v9(models.Model):
    department = models.CharField(max_length=128, db_index=True, null=True, verbose_name="Отдел")
    login = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, db_index=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=128, db_index=True, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, db_index=True, verbose_name="Отчество")
    posts = models.CharField(max_length=128)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    is_workers = models.BooleanField(default=True, verbose_name="Упр Сотруднкками")
    is_images = models.BooleanField(default=True, verbose_name="Упр Изображениями")
    is_document = models.BooleanField(default=True, verbose_name="Упр Документами")
class Output_v17(models.Model):
    department = models.CharField(max_length=128, db_index=True, null=True, verbose_name="Отдел")
    filesize = models.CharField(max_length=100)
    count_files = models.IntegerField()
    year = models.FloatField()
class Output_v15(models.Model):
    department = models.CharField(max_length=128, db_index=True, null=True, verbose_name="Отдел")
    filesize = models.FloatField()
    count_workers = models.IntegerField()
class Images(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Заголовок")
    images = models.FileField(upload_to='users_photo/%Y/%m/%d/', validators=[file_size_img, validators.FileExtensionValidator(['jpeg', 'png', 'bmp', 'gif'], message='Ваше изображение должен быть jpeg, png, bmp, gif')])
    filesize = models.CharField(editable=False, max_length=100)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    user_images = models.ForeignKey(
        'UserData',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="user_document_id")



    def save(self, *args, **kwargs):
        super(Images, self).save()
        fullpath = os.path.join(settings.MEDIA_ROOT, self.images.field.upload_to, self.images.path)
        self.filesize = os.path.getsize(fullpath)
        super(Images, self).save()
def file_size_doc(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Ваш документ привысил лимит 5 Mb.')
class Document(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Заголовок")
    content = models.TextField(db_index=True, verbose_name="Контент файла")
    file = models.FileField(upload_to="%Y/%m/%d/", validators=[file_size_doc, validators.FileExtensionValidator(['txt', 'pdf', 'docx', 'doc'], message='Ваш файл должен быть txt, pdf, docx, doc')])
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    user_document = models.ForeignKey(
        'UserData',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="user_document_id")


class UserIMG(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    img = models.ImageField(upload_to='user_img/', db_index=True, verbose_name="img")
    size = models.SmallIntegerField(verbose_name="Размер")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    user_img = models.ForeignKey(
        'UserData',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="user_img_id")
    # def clean_file(self):
    #     CONTENT_TYPES = ['image']
    #     MAX_UPLOAD_PHOTO_SIZE = "2621440"
    #     content = self.cleaned_data['file']
    #     content_type = content.content_type.split('/')[0]
    #     if content_type in CONTENT_TYPES:
    #         if content._size > MAX_UPLOAD_PHOTO_SIZE:
    #             msg = 'Keep your file size under %s. actual size %s' \
    #                   % (filesizeformat(settings.MAX_UPLOAD_PHOTO_SIZE), filesizeformat(content._size))
    #             raise forms.ValidationError(msg)
    #
    #         if not content.name.endswith('.jpg'):
    #             msg = 'Your file is not jpg'
    #             raise forms.ValidationError(msg)
    #     else:
    #         raise forms.ValidationError('File not supported')
    #     return content
class Posts(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Должность")
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    #
    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('name',),
        )
        verbose_name = 'Должность'
        verbose_name_plural = 'Должность'
        ordering = ['id']


class Container(models.Model):
    url = models.CharField(max_length=100, db_index=True, verbose_name="URL")
    name = models.CharField(max_length=30, db_index=True, verbose_name="Название")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    usercontainer = models.ForeignKey(
        'UserData',
        on_delete=models.PROTECT,
        verbose_name="User_Container_id")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__is_active = self.active

    # def save(self, *args, **kwargs):
    #     self.time_update = datetime.now()
    #     print(datetime.now())
    #     super().save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_slug': self.slug})

    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = 'Контейнер паролей'
        verbose_name_plural = 'Контейнер паролей'
        ordering = ['id']


class Client(models.Model):
    last_name = models.CharField(max_length=128, db_index=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=128, db_index=True, verbose_name="Имя")
    year = models.DateField(null=True, verbose_name="Дата рождения")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Номер телефона необходимо вводить в формате: '+7999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    user_client = models.ForeignKey(
        'UserData',
        # null=True,
        # blank=True,
        on_delete=models.PROTECT,
        verbose_name="User_Client_id")

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_slug': self.slug})

    # def __str__(self):
    #     return self.last_name

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']


class Cards(models.Model):
    number = models.CharField(max_length=16, db_index=True, verbose_name="Номер")
    credit = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Сумма")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    client_cards = models.ForeignKey(
        'Client',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Client_Cards_id")
    #
    # def __str__(self):
    #     return self.client_cards.user_client.last_name

    class Meta:
        verbose_name = 'Карты Клиента'
        verbose_name_plural = 'Карты Клиента'
        ordering = ['id']

class Operation(models.Model):
    key = models.CharField(max_length=128, db_index=True, verbose_name="Ключь")
    credit = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Сумма")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    operation_cards = models.ForeignKey(
        'Cards',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="OperationCards_id")

    # def __str__(self):
    #      return self.operation_cards.client_cards.

    class Meta:
        verbose_name = 'Операции'
        verbose_name_plural = 'Операции'
        ordering = ['id']


