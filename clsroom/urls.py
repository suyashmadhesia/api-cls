from django.urls import path

from clsroom.accounts.views import LoginView, RegistrationView, ResetPassword
from clsroom.faculty.views import ClassRoomView
from clsroom.messages.views import CommentView, MessageView
from clsroom.student.views import JoinClassRoom, LeaveClassView

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('reset-password', ResetPassword.as_view(), name='reset password'),
    path('create-class', ClassRoomView.as_view(), name='create class'),
    path('join-class', JoinClassRoom.as_view(), name='join class'),
    path('leave-class', LeaveClassView.as_view(), name='leave class'),
    path('post-message', MessageView.as_view(), name='post message'),
    path('comment', CommentView.as_view(), name='commets')
]

