# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 01:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(help_text='oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.CharField(help_text='^!command$', max_length=400)),
                ('response', models.CharField(max_length=400)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitch.Bot')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="streamer's username, usually.", max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitch.Room'),
        ),
    ]
