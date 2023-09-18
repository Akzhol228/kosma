# Generated by Django 3.2 on 2023-04-15 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(blank=True, max_length=180, null=True)),
                ('speciality', models.CharField(blank=True, max_length=180, null=True)),
                ('university_year_end', models.DateField(blank=True, null=True)),
                ('now_study_university', models.CharField(blank=True, max_length=180, null=True)),
                ('now_study_speciality', models.CharField(blank=True, max_length=180, null=True)),
                ('now_study_university_year_end', models.DateField(blank=True, null=True)),
                ('course', models.CharField(blank=True, max_length=180, null=True)),
                ('current_city', models.CharField(max_length=180)),
                ('date_birth', models.DateField()),
                ('additional_education', models.CharField(blank=True, max_length=180, null=True)),
                ('experience', models.BooleanField(default=False)),
                ('work_type', models.PositiveSmallIntegerField(choices=[(1, 'Подработка'), (2, 'Основной')], default=1)),
                ('subjects', models.CharField(max_length=180)),
                ('languages', models.CharField(max_length=180)),
                ('social_profile_networks', models.CharField(max_length=180)),
                ('support_document', models.FileField(upload_to='support_document/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('languages', models.PositiveSmallIntegerField(choices=[(1, 'Русский'), (2, 'Казахский'), (3, 'Английский')], default=1)),
                ('subjects', models.ManyToManyField(to='directory.Subject')),
                ('type_tasks', models.ManyToManyField(to='directory.TypeTask')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Удовлетворительно'), (4, 'Хорошо'), (5, 'Отлично')], default=1)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_expert', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claim_expert', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
