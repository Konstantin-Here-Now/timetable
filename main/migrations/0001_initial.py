# Generated by Django 4.2 on 2023-04-26 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_lesson', models.DateField(verbose_name='Дата занятия')),
                ('time_lesson', models.TimeField(verbose_name='Время занятия')),
                ('desc', models.TextField(blank=True, verbose_name='Описание')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('approved', models.BooleanField(default=False, verbose_name='Одобрено?')),
                ('pupil_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
                'ordering': ['date_lesson', 'pupil_name'],
            },
        ),
    ]