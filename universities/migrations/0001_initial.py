# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('minimal_score', models.IntegerField()),
                ('year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('first_passing_score', models.PositiveIntegerField()),
                ('second_passing_score', models.PositiveIntegerField(blank=True, null=True)),
                ('average_salary', models.FloatField()),
                ('employment_percentage', models.FloatField()),
                ('average_age', models.PositiveIntegerField()),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='universities.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='RequiredExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='universities.Exam')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='universities.Program')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('employment_percentage', models.FloatField()),
                ('average_salary', models.FloatField()),
                ('has_military_department', models.BooleanField(default=False)),
                ('has_dormitory', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='universities.University'),
        ),
    ]