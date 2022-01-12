from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'}]

LeftMenu = [{'title': "Сотрудники", 'url_name': 'workers'},
            {'title': "PassContainer", 'url_name': 'passcontainer'},
            {'title': "Клиенты", 'url_name': 'clients'},
            {'title': "Документы", 'url_name': 'documentation'},
            {'title': "Изображения", 'url_name': 'images'},
            {'title': "Выгрузка", 'url_name': 'output'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['leftmenu'] = LeftMenu
        return context
