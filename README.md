pip install psycopg2       2.9.1    2.9.1
pip install Django         3.2.6    3.2.7
pip install Pillow         8.3.1    8.3.2
pip install django-mptt    0.13.2    0.13.2

passcontrolsystem -> settings.py --> 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'passcontrol',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

1)python manage.py makemigrations - создать миграции
2)python manage.py migrate - выполнить миграции
3)python manage.py createsuperuser - создать админа
