# Generated by Django 5.0 on 2024-05-12 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0043_saved_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saved',
            name='text',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Saved Message'),
        ),
    ]
