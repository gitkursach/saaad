# Generated by Django 3.2.7 on 2022-01-10 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localhost', '0007_output_v17'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output_v15',
            name='filesize',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='output_v17',
            name='year',
            field=models.FloatField(),
        ),
    ]
