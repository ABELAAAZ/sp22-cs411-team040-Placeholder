# Generated by Django 3.2.5 on 2022-03-26 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pokemon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blindbox',
            name='b_pic',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='blindbox',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
