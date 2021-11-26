from . models import *
from rest_framework import serializers

class ClassRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = '__all__'