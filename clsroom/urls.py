from django.urls import path

from clsroom.accounts.views import LoginView, RegistrationView, ResetPassword, username_availability
from clsroom.faculty.views import ClassRoomView
from clsroom.messages.views import CommentView, MediaFileView, MessageView
from clsroom.student.views import JoinClassRoom, LeaveClassView
from clsroom.views import *

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('reset-password', ResetPassword.as_view(), name='reset password'),
    path('create-class', ClassRoomView.as_view(), name='create class'),
    path('join-class', JoinClassRoom.as_view(), name='join class'),
    path('leave-class', LeaveClassView.as_view(), name='leave class'),
    path('message', MessageView.as_view(), name='message'),
    path('file', MediaFileView.as_view(), name='media'),
    path('comment', CommentView.as_view(), name='commets'),
    path('u/<str:pk>', get_all_class, name="Get all class"),
    path('m/<str:pk>', get_class_messages, name="Get class Messages"),
    path('f/<str:pk>', get_class_files, name='Get files of the class'),
    path('check_user/<str:pk>', username_availability, name='Check username availability')
]

