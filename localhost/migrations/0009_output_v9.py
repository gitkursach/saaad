# Generated by Django 3.2.7 on 2022-01-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localhost', '0008_auto_20220111_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Output_v9',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(db_index=True, max_length=128, null=True, verbose_name='Отдел')),
                ('login', models.CharField(max_length=128)),
                ('last_name', models.CharField(db_index=True, max_length=128, verbose_name='Фамилия')),
                ('first_name', models.CharField(db_index=True, max_length=128, verbose_name='Имя')),
                ('patronymic', models.CharField(db_index=True, max_length=128, verbose_name='Отчество')),
                ('posts', models.CharField(max_length=128)),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('is_workers', models.BooleanField(default=True, verbose_name='Упр Сотруднкками')),
                ('is_images', models.BooleanField(default=True, verbose_name='Упр Изображениями')),
                ('is_document', models.BooleanField(default=True, verbose_name='Упр Документами')),
            ],
        ),
    ]
