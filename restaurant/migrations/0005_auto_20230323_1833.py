# Generated by Django 2.2.28 on 2023-03-23 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20230323_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media\\menu_item_images'),
        ),
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media\review_images'),
        ),
    ]
