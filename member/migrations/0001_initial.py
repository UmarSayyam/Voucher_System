# Generated by Django 5.1.1 on 2024-10-04 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('additional_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('member_source', models.CharField(choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('tiktok', 'TikTok'), ('friend', 'Friend'), ('ads', 'Ads'), ('other', 'Other')], max_length=20)),
                ('address', models.TextField(max_length=250)),
                ('receive_notifications', models.BooleanField(default=True)),
                ('marketing_email_notifications', models.BooleanField(default=True)),
                ('marketing_text_notifications', models.BooleanField(default=True)),
                ('preferred_language', models.CharField(choices=[('english', 'English'), ('arabic', 'Arabic'), ('urdu', 'Urdu'), ('faarsi', 'Faarsi'), ('python', 'Python')], default='faarsi', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
