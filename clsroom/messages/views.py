import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from clsroom.messages.serializes import CommentSerializer, MessageSerializer
from clsroom.models import Comment, Message


class MessageView(APIView):
    
    def post (self, request):
        data : dict = json.loads(request.body)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            Message.objects.create(**serializer.validated_data)
            return Response({"message" : "successfull"}, status=status.HTTP_201_CREATED)
        return Response({"error" : "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class CommentView(APIView):
    
    def post(self, request):
        data: dict = json.loads(request.body)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            Comment.objects.create(**serializer.validated_data)
            return Response({"message": "successfull"}, status=status.HTTP_201_CREATED)
        return Response({"error" : "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)


    def get(self, request):
        pass
            

