# Generated by Django 4.2.3 on 2023-07-14 16:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='avaliadores',
            field=models.ManyToManyField(related_name='avaliadores', to=settings.AUTH_USER_MODEL),
        ),
    ]
