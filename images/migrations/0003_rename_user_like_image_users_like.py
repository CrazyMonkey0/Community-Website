# Generated by Django 4.2.4 on 2023-09-20 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_rename_descripton_image_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='user_like',
            new_name='users_like',
        ),
    ]