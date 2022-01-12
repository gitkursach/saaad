from django.urls import path

from .views import *

urlpatterns = [
    path('', MainList, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('workers/', workers.as_view(), name='workers'),
    path('passcontainer/', passcontainer.as_view(), name='passcontainer'),
    path('passcontainer/delete/<int:id>/', delete_pass),
    path('workers/delete/<int:id>/', delete_workers),
    path('clients/delete/<int:id>/', delete_clients),
    path('workers/edit-workers/<int:id>/', editworkers),
    path('clients/edit-client/<int:id>/', editclient),
    path('passcontainer/editpass/<int:id>/', editpass),
    path('clients/', Clients.as_view(), name='clients'),
    path('adduser/', AddUser.as_view(), name='adduser'),
    path('addposts/', AddPosts.as_view(), name='addposts'),
    path('documentation/', documentation.as_view(), name='documentation'),
    path('images/', images.as_view(), name='images'),
    path('images/delite/img/<int:id>/', delete_img),
    path('images/download_img/<int:id>/', download_img, name='download_img'),
    path('register/visitor/', visitor, name='visitor'),
    path('images/download_all/<str:filse>/', download_all, name='download_all'),
    path('output/', output, name='output'),
    # path('post/<int:post_id>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]