# Generated by Django 3.2.9 on 2021-11-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0016_auto_20211127_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='cls_id',
            field=models.CharField(default='13c0fa56-4f93-11ec-ae97-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.CharField(default='13bec72c-4f93-11ec-ae97-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='cls_id',
            field=models.CharField(max_length=36),
        ),
        migrations.AlterField(
            model_name='message',
            name='mid',
            field=models.CharField(default='13c01d0c-4f93-11ec-ae97-74c63bf6c542', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]
