# Generated by Django 5.0 on 2024-05-05 07:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_groupmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='time'),
            preserve_default=False,
        ),
    ]
