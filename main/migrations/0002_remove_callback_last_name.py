# Generated by Django 4.1 on 2023-01-19 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callback',
            name='last_name',
        ),
    ]
