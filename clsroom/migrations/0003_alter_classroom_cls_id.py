# Generated by Django 4.1 on 2022-08-20 20:37

import clsroom.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0002_alter_classroom_cls_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='cls_id',
            field=models.CharField(default=clsroom.utils.generate_uid, editable=False, max_length=40, primary_key=True, serialize=False),
        ),
    ]
