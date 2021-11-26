from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
import json
from rest_framework.decorators import api_view, permission_classes

from clsroom.models import Account, Classroom
from clsroom.serializers import ClassRoomSerializer

# FIXME put filtering query in try block to avoid errors


class JoinClassRoom(APIView):
    # TODO Paginated message, media files and people
    def post(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        data = json.loads(request.body)
        try:
            token_key = token_key[6:]
            tokens: Token = Token.objects.filter(key=token_key)
            token = tokens.first()
            user: Account = token.user
            if data['cls_id'] in user.cls_room_id and user.is_faculty:
                print(True)
                return Response({"error" : "enable to join already member"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            data['students'] = str(user)
        except:
            return Response({'error': 'Invalid Credential'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            assert data['cls_id'], KeyError()
            classroom = Classroom.objects.filter(cls_id=data['cls_id'])[0]
            # Joining the class room
            if user.account_id in classroom.blocked_accounts:
                return Response({"error" : "not allowed!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer = ClassRoomSerializer(classroom)
            if len(classroom.students.filter(account_id=user.account_id)) > 0:
                return Response({"error" : "already joined"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user.cls_room_id.append(data['cls_id'])
            user.save()
            classroom.students.add(user)
            return Response({"message" : "successful","data" : serializer.data}, status=status.HTTP_202_ACCEPTED)

        except KeyError as key_error:
            print(key_error)
            return Response({"error": "Invalid Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LeaveClassView(APIView):
    
    def post(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        data = json.loads(request.body)
        try:
            token_key = token_key[6:]
            tokens: Token = Token.objects.filter(key=token_key)
            token = tokens.first()
            user: Account = token.user
        except:
            return Response({'error': 'Invalid Credential'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            assert data['cls_id'], KeyError()
            classroom = Classroom.objects.filter(cls_id=data['cls_id'])[0]
            try:
                user.cls_room_id.remove(data['cls_id'])
                user.save()
                classroom.students.remove(user)
                return Response({"message" : "successful"}, status=status.HTTP_200_OK)
            except:
                return Response({"error" : "id not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as key_error:
            print(key_error)
            return Response({"error": "Invalid Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)