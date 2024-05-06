# Generated by Django 5.0 on 2024-05-05 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_group_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Members', to='blog.group'),
        ),
    ]