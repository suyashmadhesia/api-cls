import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from clsroom.messages.paginator import CommentPaginator

from clsroom.messages.serializes import CommentSerializer, MessageSerializer
from clsroom.models import Classroom, Comment, Message


class MessageView(APIView):
    
    def post (self, request):
        data : dict = json.loads(request.body)
        classroom = Classroom.objects.filter(cls_id=data["cls_id"].strip())
        if not classroom.exists():
            return Response({'error': 'No classroom found'}, status=status.HTTP_404_NOT_FOUND)
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
        data : dict = json.loads(request.body)
        try:
            assert data['mid'] and data['page'], KeyError()
            page = int(data["page"])
            comments = Comment.objects.filter(mid=data['mid'])
            # first five comments
            if page*5 < len(comments):
                serializer = CommentSerializer(comments[:page*5], many=True)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
            # remainig last page comments
            else:
                serializer = CommentSerializer(comments[(page*5)-5:len(comments)], many=True)
                return Response({"data" : serializer.data}, status=status.HTTP_200_OK)

        except KeyError() as key_error:
            print(key_error)
            return Response({"error" : "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            

