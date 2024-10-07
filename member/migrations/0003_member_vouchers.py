# Generated by Django 5.1.1 on 2024-10-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_member_created_by'),
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='vouchers',
            field=models.ManyToManyField(blank=True, related_name='member', to='vouchers.voucher'),
        ),
    ]
