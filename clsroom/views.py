from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
import json
import uuid
from rest_framework.decorators import api_view, permission_classes

from clsroom.models import Account, Classroom
from clsroom.serializers import ClassRoomSerializer

# FIXME put filtering query in try block to avoid errors

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data: dict = json.loads(request.body)
        accounts: QuerySet = Account.objects.filter(
            account_id=data['account_id'])
        if not accounts.exists():
            return Response({'error': 'No Account Found'}, status=status.HTTP_404_NOT_FOUND)
        account: Account = accounts.first()

        if not account.check_password(data['password']):
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token: Token = Token.objects.get(user=account)
        return Response({'token': token.key, 'name': account.name, 'account_id': account.account_id, 'is_faculty': account.is_faculty}, status=status.HTTP_200_OK)
        e


@api_view(['GET'])
@permission_classes([AllowAny])
def email_available(request):
    result = False
    email = request.GET['email']
    accounts = Account.objects.filter(email=email)
    if not accounts.exists():
        return Response({'available': 1}, status=status.HTTP_200_OK)
    else:
        return Response({'available': 0}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data: dict = json.loads(request.body)
        # print(data['password'])
        try:
            assert data['account_id'] and data['email'] and data['password'], KeyError()
            accounts = Account.objects.filter(account_id=data['account_id'])
            acc_email = Account.objects.filter(email=data['email'])
            if accounts.exists():
                return Response({'error': 'account already exist'}, status=status.HTTP_403_FORBIDDEN)
            if acc_email.exists():
                return Response({'error': 'email is already used'}, status=status.HTTP_403_FORBIDDEN)
            password = data['password']
            del data['password']
            data['account_id'] = data['account_id'].strip()
            data['email'] = data['email'].strip()
            account = Account.objects.create(**data)
            account.set_password(password)
            account.is_active = True
            account.save()
            token = Token.objects.create(user=account)
            return Response({'token': token.key, 'name': account.name, 'account_id': account.account_id, 'is_faculty': account.is_faculty},
                            status=status.HTTP_201_CREATED)
        except KeyError as key_error:
            print(key_error)
            return Response({"error": "Invalid Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        if 'token' not in data or 'password' not in data:
            return Response({"error": "Invalid Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        token_key = data['token']
        tokens: QuerySet = Token.objects.filter(key=token_key)
        if not tokens.exists():
            return Response({"error": "Invalid Credential"}, status=status.HTTP_404_NOT_FOUND)
        token: Token = tokens.first()
        user: Account = token.user
        token.delete()
        user.set_password(data['password'])
        user.save()
        token: Token = Token.objects.create(user=user)
        return Response({"message": "successfull"}, status=status.HTTP_202_ACCEPTED)


class UpdateProfile(APIView):

    def post(self, request):
        pass


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


class JoinClassRoom(APIView):
    # TODO Leave class room code for students
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
            # print("error")
            # if data['join'] == False:
            #     print("error")
                # user.cls_room_id.remove(data['cls_id'])
                # user.save()
                # classroom.students.remove(user)
                # return Response({"message" : "successful"}, status=status.HTTP_200_OK)

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
        
