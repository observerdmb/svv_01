# Generated by Django 2.0.5 on 2018-05-29 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180529_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nick_name',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Ник'),
        ),
    ]
