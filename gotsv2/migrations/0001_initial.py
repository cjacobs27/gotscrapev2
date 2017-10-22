# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-22 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=500)),
                ('page', models.BooleanField()),
                ('infobox', models.TextField()),
                ('created_at', models.DateTimeField(verbose_name='created')),
                ('updated_at', models.DateTimeField(verbose_name='last updated')),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gotsv2.Character')),
            ],
        ),
    ]
