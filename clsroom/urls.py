from accounts.views import *
from faculty.views import *
from student.views import *
from django.urls import path

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('reset-password', ResetPassword.as_view(), name='reset password'),
    path('create-class', ClassRoomView.as_view(), name='create class'),
    path('join-class', JoinClassRoom.as_view(), name='join class'),
    path('leave-class', LeaveClassView.as_view(), name='leave class')
]

