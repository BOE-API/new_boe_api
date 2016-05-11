# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Legislatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField()),
                ('final', models.DateField(blank=True, null=True)),
                ('presidente', models.CharField(max_length=300)),
                ('nombre_legislatura', models.CharField(max_length=600)),
            ],
            options={
                'ordering': ['inicio'],
            },
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='legislatura',
            name='partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='state.Partido'),
        ),
    ]
