# Generated by Django 4.2.7 on 2023-11-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoupload',
            name='file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]