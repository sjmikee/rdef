# Generated by Django 3.0.6 on 2020-05-30 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdef_web', '0002_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='urls',
            name='protocol',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='urls',
            name='time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='urls',
            name='user',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
