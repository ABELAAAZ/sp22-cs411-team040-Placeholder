# Generated by Django 3.2.5 on 2022-03-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pokemon', '0002_auto_20220326_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='u_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
