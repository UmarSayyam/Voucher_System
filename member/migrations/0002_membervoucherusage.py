# Generated by Django 5.1.1 on 2024-10-07 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberVoucherUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_count', models.IntegerField(default=0)),
                ('is_expired', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.member')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vouchers.voucher')),
            ],
            options={
                'unique_together': {('member', 'voucher')},
            },
        ),
    ]
