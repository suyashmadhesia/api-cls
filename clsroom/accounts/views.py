from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
import json
from rest_framework.decorators import api_view, permission_classes

from clsroom.models import Account, Classroom


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
        return Response({'token': token.key, 'name': account.name, 'account_id': account.account_id, 'is_faculty': account.is_faculty, 'classrooms': account.cls_room_id}, status=status.HTTP_200_OK)
    
    def get(self, request):
        data :dict = json.loads(request.body)
        res = []
        try:
            assert data['classroom_ids'], KeyError()
            cids = data['classroom_ids']
            for i in range(len(cids)):
                cls_data = {}
                classroom = Classroom.objects.get(cls_id=cids[i].strip())
                cls_data['cls_id'] = classroom.cls_id
                cls_data['name'] = classroom.name
                cls_data['class_teacher'] = classroom.owner.account_id
                cls_data['teacher_name'] = classroom.owner.name
                cls_data['activity'] = classroom.is_active
                cls_data['last_updated'] = classroom.updated_at
                res.append(cls_data)
            return Response({"data" : res}, status=status.HTTP_200_OK)
        except KeyError as key_error:
            print(key_error)
            return Response({"data" : res}, status=status.HTTP_400_BAD_REQUEST)


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
