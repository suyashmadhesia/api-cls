from django.db.models import fields
from rest_framework import serializers

from clsroom.models import Comment, Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta :
        model = Message
        exclude = ['comment']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'