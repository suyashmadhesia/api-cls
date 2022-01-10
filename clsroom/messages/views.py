import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
# from clsroom.messages.paginator import CommentPaginator

from clsroom.messages.serializes import CommentSerializer, MediaFilesSerializer, MessageSerializer
from clsroom.models import Account, Classroom, Comment, MediaFile, Message


class MessageView(APIView):

    def post(self, request):
        data: dict = json.loads(request.body)
        classroom = Classroom.objects.filter(cls_id=data["cls_id"].strip())
        if not classroom.exists():
            return Response({'error': 'No classroom found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            Message.objects.create(**serializer.validated_data)
            return Response({"message": "successfull"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CommentView(APIView):

    def post(self, request):
        data: dict = json.loads(request.body)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            Comment.objects.create(**serializer.validated_data)
            return Response({"message": "successfull"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request):
        data: dict = json.loads(request.body)
        try:
            assert data['mid'] and data['page'], KeyError()
            page = int(data["page"])
            comments = Comment.objects.filter(mid=data['mid'])
            # first five comments
            if page*5 < len(comments):
                serializer = CommentSerializer(comments[:page*5], many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            # remainig last page comments
            else:
                serializer = CommentSerializer(
                    comments[(page*5)-5:len(comments)], many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except KeyError() as key_error:
            print(key_error)
            return Response({"error": "Incomplete data"}, status=status.HTTP_406_NOT_ACCEPTABLE)


# Faculty can only post assignment and media files.
class MediaFileView(APIView):

    def post(self, request):
        data: dict = json.loads(request.body)
        token_key = request.META.get('HTTP_AUTHORIZATION')
        try:
            token_key = token_key[6:]
            tokens: Token = Token.objects.filter(token_key)
            token = tokens.first()
            user: Account = token.user
            if not user.is_faculty:
                return Response({'error': 'Rejected! Non faculty member'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'error': 'Invalid Credential'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = MediaFilesSerializer(data=data)
        if serializer.is_valid():
            mediafile = MediaFile.objects.create(**serializer.validated_data)
            mediafile.save()
            return Response({"message": "successfull"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_403_FORBIDDEN)
