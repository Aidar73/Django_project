# Generated by Django 2.2.9 on 2023-01-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20230126_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/%Y/%m/%d/'),
        ),
    ]