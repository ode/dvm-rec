# Generated by Django 3.2.9 on 2021-12-13 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20211213_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='com_cod',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
