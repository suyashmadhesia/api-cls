# Generated by Django 3.2.9 on 2021-11-25 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0007_remove_classroom_class_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='cls_id',
            field=models.CharField(default='<function uuid1 at 0x7fc6aa802310>', editable=False, max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.CharField(default='<function uuid1 at 0x7fc6aa802310>', editable=False, max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='mid',
            field=models.CharField(default='<function uuid1 at 0x7fc6aa802310>', editable=False, max_length=30, primary_key=True, serialize=False),
        ),
    ]