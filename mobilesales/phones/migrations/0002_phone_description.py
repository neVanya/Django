# Generated by Django 4.2.7 on 2023-12-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]