# Generated by Django 3.0.6 on 2020-08-16 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdef_web', '0005_auto_20200530_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='blacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='whitelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
