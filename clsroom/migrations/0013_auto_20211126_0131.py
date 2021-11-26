# Generated by Django 3.2.9 on 2021-11-26 01:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0012_auto_20211126_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='blocked_accounts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=36), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='cls_id',
            field=models.CharField(default='8d4f7988-4e58-11ec-9fde-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.CharField(default='8d4e5ba2-4e58-11ec-9fde-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='mid',
            field=models.CharField(default='8d4f0354-4e58-11ec-9fde-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]