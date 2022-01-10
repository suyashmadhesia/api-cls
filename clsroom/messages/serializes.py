from django.db.models import fields
from rest_framework import serializers

from clsroom.models import Comment, MediaFile, Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta :
        model = Message
        exclude = ['comment']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class MediaFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaFile
        fields = '__all__'