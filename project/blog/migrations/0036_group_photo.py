# Generated by Django 5.0 on 2024-05-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_groupmessage_is_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='GroupPhoto', verbose_name='photo'),
        ),
    ]
