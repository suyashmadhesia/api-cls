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

class ClassRoomView(APIView):

    def post(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        data = json.loads(request.body)
        try:
            token_key = token_key[6:]
            tokens: Token = Token.objects.filter(key=token_key)
            token = tokens.first()
            user: Account = token.user
            data['owner'] = str(user.account_id)
            if not user.is_faculty:
                return Response({'error': 'Rejected! Non Faculty Member'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
             return Response({'error': 'Invalid Credential'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ClassRoomSerializer(data=data)
        if serializer.is_valid():
            classroom = Classroom.objects.create(**serializer.validated_data)
            user.cls_room_id.append(classroom.cls_id)
            user.save()
            return Response({
                "message": "successfull",
                "data": {
                    "class_id": classroom.cls_id,
                }, }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        return Response({"msg" : "success"})