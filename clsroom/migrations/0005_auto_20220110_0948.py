# Generated by Django 3.2.9 on 2022-01-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0004_auto_20220110_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='cls_id',
            field=models.CharField(default='257585ab90-71fa-11ec-9913-74c63bf6c54228', editable=False, max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.CharField(default='3175843efe-71fa-11ec-9913-74c63bf6c54253', editable=False, max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='mid',
            field=models.CharField(default='94758487d8-71fa-11ec-9913-74c63bf6c54218', editable=False, max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='mid',
            field=models.CharField(default='6575851a04-71fa-11ec-9913-74c63bf6c54224', editable=False, max_length=40, primary_key=True, serialize=False),
        ),
    ]
