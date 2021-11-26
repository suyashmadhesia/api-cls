# Generated by Django 3.2.9 on 2021-11-25 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('clsroom', '0003_alter_account_cls_room_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('cls_id', models.CharField(max_length=16)),
                ('mid', models.CharField(max_length=16)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('publiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpublisher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('mid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('cls_id', models.CharField(max_length=16)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ManyToManyField(default=None, related_name='classCommentM', to='clsroom.Comment')),
                ('publiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mpublisher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('m_url', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ManyToManyField(default=None, related_name='classCommentF', to='clsroom.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('cls_id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('media_files', models.ManyToManyField(default=None, related_name='mediaFiles', to='clsroom.MediaFile')),
                ('messages', models.ManyToManyField(default=None, related_name='classMessage', to='clsroom.Message')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classOwner', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(default=None, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
