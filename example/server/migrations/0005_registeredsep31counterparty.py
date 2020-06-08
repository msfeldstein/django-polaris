# Generated by Django 2.2.12 on 2020-05-28 23:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20200427_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredSEP31Counterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=56, validators=[django.core.validators.MinLengthValidator(56)])),
                ('organization_name', models.TextField()),
            ],
        ),
    ]