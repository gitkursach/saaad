import io
import os
import zipfile
from io import StringIO

from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.db.models.functions import Length
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


# from .forms import *
from .forms import *
from .models import *

#  from .utils import *
from localhost.utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'}]

LeftMenu = [{'title': "Сотрудники", 'url_name': 'workers'},
            {'title': "PassContainer", 'url_name': 'passcontainer'},
            {'title': "Клиенты", 'url_name': 'clients'},
            {'title': "Документы", 'url_name': 'documentation'},
            {'title': "Изображения", 'url_name': 'images'},
            {'title': "Выгрузка", 'url_name': 'output'}]


def output(request):
    results = "Error"
    var_15 = False
    var_17 = False
    if 'var' in request.GET:
        var = request.GET.get('var')
        if var == 'var_15':
            departments = UserData.objects.filter(department__isnull=False)
            sum_filesize = 0
            sum_workers = 0
            sum_workers_list = []
            Output_v15.objects.all().delete()

            for department in departments:
                if department.level == 0:
                    tree_id = department.tree_id
                    users = UserData.objects.filter(tree_id=tree_id)
                    sum_filesize = 0
                    for user in users:
                        sum_workers = sum_workers + 1

                        images = Images.objects.filter(user_images_id=user.pk)
                        for image in images:
                            sum_filesize = sum_filesize + int(image.filesize)
                        try:
                            sum_filesize = sum_filesize // int(images.count())
                            print(sum_filesize)
                        except ZeroDivisionError:
                            print(ZeroDivisionError)
                    count_workers = int(users.count())

                    Output_v15(department=department.department, filesize=sum_filesize, count_workers=count_workers).save()

            var_15 = True
            results = Output_v15.objects.all()
        if var == 'var_17':

            departments = UserData.objects.filter(department__isnull=False)

            sum_workers = 0
            sum_workers_list = []
            Output_v17.objects.all().delete()

            for department in departments:
                if department.level == 0:
                    tree_id = department.tree_id
                    users = UserData.objects.filter(tree_id=tree_id)

                    all_year = 0
                    count_year = 0
                    average_year = 0
                    sum_filesize = 0
                    count_files = 0
                    for user in users:
                        sum_workers = sum_workers + 1


                        if user.year != None:
                            yar_now = datetime.now().date().year

                            year_workers = int(yar_now) - int(user.year.year)
                            all_year = all_year + year_workers
                           # year = year + user.year.year
                            count_year += 1
                        images = Images.objects.filter(user_images_id=user.pk)
                        for image in images:
                            sum_filesize = sum_filesize + int(image.filesize)

                        count_files = count_files + int(images.count())
                    try:
                        average_year = all_year / count_year
                    except ZeroDivisionError:
                            print(ZeroDivisionError)
                    Output_v17(department=department.department, filesize=sum_filesize,
                               count_files=count_files, year=average_year).save()

            var_17 = True
            results = Output_v17.objects.all()
    context = {
        'var_15': var_15,
        'var_17': var_17,
        'results': results,
        'title': "Выгрузка по вариантам",
        'menu': menu,
        'leftmenu': LeftMenu,

    }
    return render(request, 'localhost/output.html', context=context)
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def delete_workers(request, id):
    try:
        person = UserData.objects.get(id=id)
        if request.user.is_authenticated and (request.user.level == 0 or person.parent.level >= request.user.pk or request.user.level <= person.parent.level or request.user.pk == person.pk):
            print(1)
            person.delete()
            return HttpResponseRedirect(reverse_lazy("workers"))
        else:
            return HttpResponseNotFound("<h1>Страница не найдена</h1>")
    except Container.DoesNotExist:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def delete_clients(request, id):
    try:
        person = Client.objects.get(id=id)
        if request.user.is_authenticated and (request.user.pk == person.user_client.pk or request.user.level == 0):
            person.delete()
            return HttpResponseRedirect(reverse_lazy("clients"))
        else:
            return HttpResponseNotFound("<h1>Страница не найдена</h1>")
    except Container.DoesNotExist:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def delete_pass(request, id):
    try:
        person = Container.objects.get(id=id)
        print(request.user.pk)
        print(person.usercontainer.pk)
        if request.user.is_authenticated and (request.user.pk == person.usercontainer.pk or request.user.level ==0) :
            person.delete()
            return HttpResponseRedirect(reverse_lazy("passcontainer"))
        else:
            return HttpResponseNotFound("<h1>Страница не найдена</h1>")
    except Container.DoesNotExist:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def editpass(request, id):
    try:
        person = Container.objects.get(id=id)
        if request.method == "POST":
            person.url = request.POST.get("url")
            person.name = request.POST.get("name")
            person.password = request.POST.get("password")

            person.save()

            return HttpResponseRedirect(reverse_lazy("passcontainer"))
        else:
            context = {
                'title': "Обновить данные",
                'menu': menu,
                'leftmenu': LeftMenu,
                "person": person,
            }
            return render(request, 'localhost/edit_pass.html', context=context)
    except Container.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
def save_file(file):
    with open('somefile.txt', 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
def download_all_zip(files):
        zip_io = io.BytesIO()
        filenames = []
        print(files)
        for file in files:
            print(file)
            filenames.append(f'media/{file.images.name}')
            print(filenames)
        with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:

            for filename in filenames:
                backup_zip.write(filename)  # u can also make use of list of filename location
            # and do some iteration over it
        response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'your_zipfilename' + ".zip"
        response['Content-Length'] = zip_io.tell()
        return response
class images(DataMixin, View):
    def get(self, request):
        user_id = self.request.user
        files = Images.objects.filter(user_images_id=user_id)

        if self.request.user.level == 0:
            print('good')
            chief = UserData.objects.get(tree_id=self.request.user.tree_id, level=0)
            print("get", chief)
            users = UserData.objects.filter(tree_id=chief.tree_id)
            for user in users:
                print(users, user)
                user_files = Images.objects.filter(user_images=user.pk)
                files = files | user_files
        else:

            files = Images.objects.filter(user_images=user_id)

        if 'search_name' in request.GET:
            search_name = request.GET.get('search_name')
            files = Images.objects.filter(title__icontains=search_name)
        if 'search_format' in request.GET:
            search_format = request.GET.get('search_format')
            if search_format == '.gif':
                files = files.filter(images__icontains=search_format)
            if search_format == '.jpeg':
                files = files.filter(images__icontains=search_format)
            if search_format == '.png':
                files = files.filter(images__icontains=search_format)
            if search_format == '.bmp':
                files = files.filter(images__icontains=search_format)

        if 'search_size_min' in request.GET:
            search_size_min = request.GET.get('search_size_min')
            if 'search_size_max' in request.GET:
                search_size_max = request.GET.get('search_size_max')
                if search_size_min <= search_size_max:
                    files = files.filter(filesize__gte=search_size_min, filesize__lte=search_size_max)
                    print(search_size_min, search_size_max)

        if 'name' in request.GET:
            if request.GET['name'] == '1':
                files = files.all().order_by('title')
        if 'format' in request.GET:
            if request.GET['format'] == '1':
                files = files.all().order_by('images')
        if 'size' in request.GET:
            if request.GET['size'] == '1':
                files = files.reverse().order_by(Length('images').asc())
        if 'time_create' in request.GET:
            if request.GET['time_create'] == '1':
                files = files.all().order_by('-time_create')

        for file in files:
            if '.jpeg' in file.images.name:
                file.images.temp = 'jpeg'
            if '.png' in file.images.name:
                file.images.temp = 'png'
            if '.bmp' in file.images.name:
                file.images.temp = 'bmp'
            if '.gif' in file.images.name:
                file.images.temp = 'gif'
        if 'download_all_zip' in request.GET:
            if request.user.is_superuser:
                files = Images.objects.all()
                return download_all_zip(files)
            else:
                return download_all_zip(files)
        context = {

            'files': files,
            'title': "Хранилище фото",
            'menu': menu,
            'leftmenu': LeftMenu,

        }
        return render(request, 'localhost/images.html', context=context)


    def post(self, request):
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        # # Получить файлы на стойке регистрации
        # file = request.FILES.get('file')
        # # Сохранить данные в базу данных
        # # После вызова метода article.save () файл будет сохранен в файлах, а путь к этому файлу будет сохранен в базе данных.
        # article = Document(title=title, content=content, file=file)
        errors_form =''

        # def form_valid(self, form):
        #     form.instance.usercontainer = self.request.user
        #     return super(passcontainer, self).form_valid(form)
        form = ImagesForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        user_id = self.request.user
        count = 0
        files = "Тут будут ваши фото jpeg, png, gif, bmp"


        for x in Images.objects.filter(user_images_id=user_id):
            count += 1
        if count < 20:
        # Сохранить данные в базу данных
            if form.is_valid():
                print(request.FILES)
                form.instance.user_images = self.request.user
                form.save()
                successfully_form = "Успешно Сохранен!"




                if user_id:
                    files = Images.objects.filter(user_images_id=user_id)
                    for file in files:
                        if '.jpeg' in file.images.name:
                            file.images.temp = 'jpeg'
                        if '.png' in file.images.name:
                            file.images.temp = 'png'
                        if '.bmp' in file.images.name:
                            file.images.temp = 'bmp'
                        if '.gif' in file.images.name:
                            file.images.temp = 'gif'
                context = {
                    'files': files,
                    'successfully_form': successfully_form,
                    'title': "Хранилище файлов",
                    'menu': menu,
                    'leftmenu': LeftMenu,

                }
                #return HttpResponseRedirect(request.path)
                return render(request, 'localhost/images.html', context=context)
            else:

                print(form.errors.get_json_data())
                # Распечатать сообщение об ошибке
                errors_form = form.errors.get_json_data()
                user_id = self.request.user
                files = "Тут будут ваши фото jpeg, png, gif, bmp"
                if user_id:
                    files = Images.objects.filter(user_images_id=user_id)
                    for file in files:
                        if '.jpeg' in file.images.name:
                            file.images.temp = 'jpeg'
                        if '.png' in file.images.name:
                            file.images.temp = 'png'
                        if '.bmp' in file.images.name:
                            file.images.temp = 'bmp'
                        if '.gif' in file.images.name:
                            file.images.temp = 'gif'
                context = {
                    'files': files,
                    'errors_form': errors_form,
                    'title': "Хранилище файлов",
                    'menu': menu,
                    'leftmenu': LeftMenu,

                }
                return render(request, 'localhost/images.html', context=context)
        else:
            files = "Тут будут ваши фото jpeg, png, gif, bmp"
            errors_count = "Привышен лимит в 20 фото"
            if user_id:
                files = Images.objects.filter(user_images_id=user_id)
            context = {
                'files': files,
                'errors_form': errors_count,
                'title': "Хранилище файлов",
                'menu': menu,
                'leftmenu': LeftMenu,

            }
            return render(request, 'localhost/images.html', context=context)
def delete_img(request, id):
    images = Images.objects.get(id=id)
    images.delete()
    return HttpResponseRedirect(reverse_lazy("images"))

class documentation(DataMixin, View):
# def documentation(request):
#     model = UserData
#     template_name = 'localhost/documentation.html'
#     context_object_name = 'tes'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Файлы")
#         return dict(list(context.items()) + list(c_def.items()))
#     def get(self, request):
#         return render(request, 'localhost/documentation.html')
#     def post(self, request):
#
#
#         # Получить файл с переднего плана, request.POST используется для получения заголовка и содержимого, request.FILES используется для получения файла
#         form = ArticleForm(request.POST, request.FILES)
#         # Сохранить данные в базу данных
#         if form.is_valid():
#             form.save()
#             return HttpResponse("SUCCESS")
#         else:
#             # Распечатать сообщение об ошибке
#             print(form.errors.get_json_data())
#             return HttpResponse("Fail")

        # # Если это запрос GET, визуализируйте прямо на странице загрузки файла
        # def get(self, request):
        #     return render(request, 'localhost/documentation.html')
        #     # Если это запрос POST, будет получено значение файла
        #
        # def post(self, request):
        #     # Получить файлы на стойке регистрации
        #     myfile = request.FILES.get('file')
        #     # Вызовите специальный метод save_file (), чтобы сохранить файл на сервере
        #     save_file(myfile)
        #
        #     return HttpResponse("SUCCESS")


    # Если это запрос GET, визуализируйте прямо на странице загрузки файла




    def get(self, request):
        user_id = self.request.user
        files = "Тут будут ваши файлики PDF, DOC, TXT"
        if user_id:
            files = Document.objects.filter(user_document_id=user_id)

        context = {
            'files': files,
            'title': "Хранилище файлов",
            'menu': menu,
            'leftmenu': LeftMenu,

        }
        return render(request, 'localhost/documentation.html', context=context)


    def post(self, request):
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        # # Получить файлы на стойке регистрации
        # file = request.FILES.get('file')
        # # Сохранить данные в базу данных
        # # После вызова метода article.save () файл будет сохранен в файлах, а путь к этому файлу будет сохранен в базе данных.
        # article = Document(title=title, content=content, file=file)
        errors_form =''

        # def form_valid(self, form):
        #     form.instance.usercontainer = self.request.user
        #     return super(passcontainer, self).form_valid(form)
        form = DocumentForm(request.POST, request.FILES)
        # Сохранить данные в базу данных
        print(request.POST, request.FILES)
        if form.is_valid():

            form.instance.user_document = self.request.user
            form.save()
            successfully_form = "Успешно Сохранен!"
            context = {
                'successfully_form': successfully_form,
                'title': "Хранилище файлов",
                'menu': menu,
                'leftmenu': LeftMenu,

            }
            return render(request, 'localhost/documentation.html', context=context)
        else:
            # Распечатать сообщение об ошибке
            print(form.errors.get_json_data())
            errors_form = form.errors.get_json_data()['file'][0]['message']
            context = {
                'errors_form': errors_form,
                'title': "Хранилище файлов",
                'menu': menu,
                'leftmenu': LeftMenu,

            }
            return render(request, 'localhost/documentation.html', context=context)


    # context = {
    #     'title': "Хранилище файлов",
    #     'menu': menu,
    #     'leftmenu': LeftMenu,
    #
    # }
    # return render(request, 'localhost/documentation.html', context=context)
def editclient(request, id):
    try:
        person = Client.objects.get(id=id)
        if request.method == "POST":
            person.last_name = request.POST.get("last_name")
            person.first_name = request.POST.get("first_name")
            person.year = request.POST.get("year")
            person.phone = request.POST.get("phone")

            person.save()

            return HttpResponseRedirect(reverse_lazy("clients"))
        else:
            context = {
                'title': "Обновить данные",
                'menu': menu,
                'leftmenu': LeftMenu,
                "person": person,
            }
            return render(request, 'localhost/edit_client.html', context=context)

    except Container.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def editworkers(request, id):
    try:
        person = UserData.objects.get(id=id)
        if request.method == "POST":

            person.last_name = request.POST.get("last_name")
            person.first_name = request.POST.get("first_name")
            person.patronymic = request.POST.get("patronymic")
            person.email = request.POST.get("email")
            person.phone = request.POST.get("phone")
            person.year = request.POST.get("year")
            person.is_clients = request.POST.get("is_clients") == 'on'
            person.is_workers = request.POST.get("is_workers") == 'on'
            person.is_password = request.POST.get("is_password") == 'on'
            person.is_document = request.POST.get("is_document") == 'on'
            person.is_images = request.POST.get("is_images") == 'on'

            person.save()

            return HttpResponseRedirect(reverse_lazy("workers"))
        else:
            context = {
                'title': "Обновить данные сотрудника",
                'menu': menu,
                'leftmenu': LeftMenu,
                "person": person,
            }
        return render(request, 'localhost/edit_workers.html', context=context)

    except Container.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def download_all(request, files):
    print(files)
    zip_io = io.BytesIO()
    filenames = []
    for file in files:
        filenames.append(f'media/{file.images.name}')
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        print(filenames)
        for filename in filenames:
            backup_zip.write(filename)  # u can also make use of list of filename location
        # and do some iteration over it
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'your_zipfilename' + ".zip"
    response['Content-Length'] = zip_io.tell()
    return response



class workers(DataMixin, View):
    def get(self, request):
        usersdata = UserData.objects.all()
        if 'search_login' in request.GET:
            search_login = request.GET.get('search_login')
            usersdata = UserData.objects.filter(username__icontains=search_login)
        if 'last_name' in request.GET:
            last_name = request.GET.get('last_name')
            usersdata = UserData.objects.filter(last_name__icontains=last_name)
        if 'first_name' in request.GET:
            first_name = request.GET.get('first_name')
            usersdata = UserData.objects.filter(first_name__icontains=first_name)
        if 'patronymic' in request.GET:
            patronymic = request.GET.get('patronymic')
            usersdata = UserData.objects.filter(patronymic__icontains=patronymic)
        if 'search_phone' in request.GET:
            search_phone = request.GET.get('search_phone')
            print(search_phone)
            usersdata = UserData.objects.filter(phone__icontains=search_phone)
        if 'search_date_min' in request.GET:
            search_date_min = request.GET.get('search_date_min')
            print(search_date_min)
            if 'search_date_max' in request.GET:
                search_date_max = request.GET.get('search_date_max')
                if search_date_min <= search_date_max:
                    print(search_date_max, search_date_min)
                    images = Images.objects.filter(time_create__range=[search_date_min, search_date_max])
                    print(images)
                    for image in images:
                        usersdata = UserData.objects.filter(pk=image.user_images.pk)
        context = {
            'title': "Обновить данные сотрудников",
            'menu': menu,
            'leftmenu': LeftMenu,
            "usersdata": usersdata,
        }
        return render(request, 'localhost/workers.html', context=context)
    # paginate_by = 2  # страници
    # model = UserData
    # template_name = 'localhost/workers.html'
    # context_object_name = 'usersdata'
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Работники")
    #     return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return UserData.objects.filter(is_published=True)


def MainList(request):
    context = {
        'menu': menu,
        'leftmenu': LeftMenu,
        'title': 'Главная',
    }
    return render(request, 'localhost/index.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'leftmenu': LeftMenu,
        'title': 'О сайте',
    }
    return render(request, 'localhost/about.html', context=context)


def contact(request):
    context = {
        'menu': menu,
        'leftmenu': LeftMenu,
        'title': 'Обратная связь',
    }
    return render(request, 'localhost/contact.html', context=context)


# def workers(request):
#     context = {
#         'menu': menu,
#         'leftmenu': LeftMenu,
#         'title': 'Сотрудники',
#     }
#     return render(request, 'localhost/index.html', context=context)
class passcontainer(DataMixin, CreateView, ListView):
    # paginate_by = 2  # страници
    form_class = PassContForm
    model = Container
    template_name = 'localhost/passcontainer.html'
    context_object_name = 'passc'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Контейнер корпоративных паролей")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.usercontainer = self.request.user
        return super(passcontainer, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("passcontainer")


# def passcontainer(request):
#     context = {
#         'menu': menu,
#         'leftmenu': LeftMenu,
#         'title': 'PassContainer',
#     }
#     return render(request, 'localhost/index.html', context=context)


class ClientsAdd(DataMixin, CreateView):
    # paginate_by = 2  # страници
    form_class = ClientForm
    template_name = 'localhost/client_add.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Клиенты организации")
        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):
    #     form.instance.usercontainer = self.request.user
    #     return super(Clients, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("clients")
def download_img(request, id):

    img = Images.objects.get(pk=id)

    return redirect(img.images.url)
class Clients(DataMixin, CreateView, ListView):
    form_class = ClientForm
    model = Operation
    template_name = 'localhost/clients.html'
    context_object_name = 'client'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Клиенты организации")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user_client = self.request.user
        return super(Clients, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("clients")
    # def get_queryset(self):
    #     return UserData.objects.filter(is_published=True)

# def LeftMenuList(request):
#     context = {
#         'leftmenu': LeftMenu,
#         'title': 'Меню управления',
#     }
#     return render(request, 'localhost/index.html', context=context)


# class MainList(ListView):
#     # paginate_by = 2
#     # model = UserData
#     template_name = 'localhost/index.html'
#     # extra_context = {'title': "Главная страница"}
#     # context_object_name = 'posts'
#     # allow_empty = False
#
#    # def get_queryset(self):
#    #     return MainList.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
#         context['title'] = 'Главная страница'
#         context['menu'] = menu
#         # context['cat_selected'] = context['posts'][0].cat_id
#         return context

# def login(request):
#     return HttpResponse("Авторизация")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'localhost/register.html'
    success_url = reverse_lazy('login')



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     form.instance.parent = self.request.user
    #     return super(RegisterUser, self).form_valid(form) + redirect('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

def visitor(request):
    users = UserData.objects.all()
    if request.method == 'POST':
        if 'department' in request.POST:
            add_visitor = request.POST.get('department')
            visitor = UserData.objects.get(username="Гость")
            visitor.parent_id = add_visitor
            visitor.save()
            user = UserData.objects.get(username="Гость")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    context = {
        'users': users,
        'menu': menu,
        'leftmenu': LeftMenu,
        'title': 'Обратная связь',
    }
    return render(request, 'localhost/visitor.html', context=context)
class LoginUser(DataMixin, LoginView):
    from_class = UserLoginForm
    template_name = 'localhost/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("workers")


def logout_user(request):
    logout(request)
    return redirect('login')


class AddUser(DataMixin, CreateView):
    form_class = AddUserForm
    model = UserData
    template_name = 'localhost/formadduser.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить сотрудника")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.parent = self.request.user
        return super(AddUser, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workers")


class AddPosts(DataMixin, CreateView, ListView):
    model = Posts
    form_class = AddPostsForm
    template_name = 'localhost/formaddposts.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить Должности")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("addposts")
