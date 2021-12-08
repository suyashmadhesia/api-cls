from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
import uuid

from clsroom.utils import generate_uid


class AccountManager(BaseUserManager):

    def create_user(self, account_id, password, **extra_fields):
        if not account_id:
            raise ValueError("Users must have an account id")
        if not password:
            raise ValueError("Users must have an password")
        account = self.model(account_id, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, account_id, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(account_id, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    account_id = models.CharField(max_length=10, primary_key=True)
    branch = models.CharField(max_length=2, default='', blank=True, null=True)
    name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, blank=False)
    is_faculty = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    cls_room_id = ArrayField(models.CharField(
        max_length=40, blank=True), default=list)

    objects = AccountManager()
    USERNAME_FIELD = 'account_id'
    REQUIRED_FIELD = ('email')

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_satff


# FIXME setup uuid unique for every time

class Comment(models.Model):
    cid = models.CharField(
        max_length=40,
        primary_key=True, default=generate_uid(), editable=False)
    mid = models.CharField(max_length=40, blank=False)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    publiser = models.ForeignKey(
        Account, related_name='cpublisher', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.cid)


class MediaFile(models.Model):
    mid = models.CharField(
        max_length=40,
        primary_key=True, default=generate_uid(), editable=False)
    m_url = models.CharField(max_length=200, blank=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(
        Comment, related_name='classCommentF', default=None)

    def __str__(self) -> str:
        return self.m_url


class Message(models.Model):
    mid = models.CharField(
        max_length=40,
        primary_key=True, default=generate_uid(), editable=False)
    cls_id = models.CharField(max_length=40, blank=False)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    publiser = models.ForeignKey(
        Account, related_name='mpublisher', on_delete=models.CASCADE)
    comment = models.ManyToManyField(
        Comment, related_name='classCommentM', default=None)

    def __str__(self) -> str:
        return str(self.mid)


class Classroom(models.Model):
    cls_id = models.CharField(
        max_length=40,
        primary_key=True, default=generate_uid(), editable=False)
    name = models.CharField(max_length=30, blank=False)
    owner = models.ForeignKey(
        Account, related_name='classOwner', on_delete=models.CASCADE, blank=False)
    students = models.ManyToManyField(
        Account, related_name='students', blank=True)
    is_active = models.BooleanField(default=True)
    media_files = models.ManyToManyField(
        MediaFile, related_name='mediaFiles', blank=True)
    messages = models.ManyToManyField(
        Message, related_name='classMessage', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    blocked_accounts = ArrayField(models.CharField(max_length=len(
        generate_uid()), default=None, blank=True), default=list, blank=True)

    def __str__(self) -> str:
        return str(self.cls_id) + " <==NAME==> " + self.name
