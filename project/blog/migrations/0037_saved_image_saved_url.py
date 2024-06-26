# Generated by Django 5.0 on 2024-05-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_group_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='saved',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='saved', verbose_name='image'),
        ),
        migrations.AddField(
            model_name='saved',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
