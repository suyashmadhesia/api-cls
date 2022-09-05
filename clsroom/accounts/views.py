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
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        account: Account = accounts.first()
        token: Token = Token.objects.get(user=account)
        if not account.check_password(data['password']) or not token:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'email': account.email, 'token': token.key, 'name': account.name, 'account_id': account.account_id, 'is_faculty': account.is_faculty, 'classrooms': account.cls_room_id}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def username_availability(request):
    account_id = request.GET['account_id']
    accounts = Account.objects.filter(account_id=account_id)
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
            assert data['account_id'] and data['password'] and data['email'], KeyError()
            accounts = Account.objects.filter(account_id=data['account_id'])
            emails = Account.objects.filter(email=data['email'])
            if accounts.exists():
                return Response({'error': 'username is already in use'}, status=status.HTTP_403_FORBIDDEN)
            if emails.exists():
                return Response({'error': 'email is already in use'}, status=status.HTTP_403_FORBIDDEN)
            password = data['password']
            del data['password']
            data['account_id'] = data['account_id'].strip()
            data['email'] = data['email'].strip()
            account = Account.objects.create(**data)
            account.set_password(password)
            account.is_active = True
            account.save()
            token = Token.objects.create(user=account)
            return Response({'token': token.key, 'name': account.name, 'account_id': account.account_id, 'is_faculty': account.is_faculty, 'email': account.email},
                            status=status.HTTP_201_CREATED)
        except KeyError as key_error:
            # print(key_error)
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


class ForgetPassword(APIView):
    pass
