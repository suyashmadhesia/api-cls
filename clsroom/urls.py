from .views import *
from django.urls import path

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('reset-password', ResetPassword.as_view(), name='reset password')
]

