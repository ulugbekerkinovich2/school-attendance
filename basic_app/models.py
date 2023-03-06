import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from davomat_ import daily


class Sinf(models.Model):
    group = models.CharField(max_length=20, default='mavjud emas', unique=True)

    def __str__(self):
        return str(self.group)

    class Meta:
        db_table = 'sinf'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError(_('Iltimos, foydalanuvchi nomini kiriting'))

        # username_validator = UnicodeUsernameValidator(min_length=5)
        # username_validator(username)
        # if len(username) < 5:
        #     raise ValueError(_('Ism 5 ta belgidan kam bo\'lmasligi kerak'))
        # if len(password) < 8:
        #     raise ValueError(_('Parol 8 ta belgidan kam bo\'lmasligi kerak'))
        if password:
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, username, **extra_fields):

        extra_fields.setdefault('is_staff', True)

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username=username, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Name'), max_length=50, unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


def __str__(self):
    return f'{self.username}'


class Student(models.Model):
    full_name = models.CharField(max_length=60, null=False, unique=True)
    sinf = models.ForeignKey(Sinf, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}, {self.sinf}'

    class Meta:
        db_table = 'student'


class DataStudentsManager(models.Manager):
    def get_queryset(self, request=None):
        queryset = super().get_queryset()
        current_date = datetime.now().date()
        if request and request.query_params.get('weekly') == 'weekly':
            week_number = current_date.isocalendar()[1]
            queryset = queryset.filter(created_at__week=week_number, weekday=current_date.strftime('%A'))
            # print(queryset, '-------')
        return queryset


class DataStudents(models.Model):
    created_at = models.DateField(auto_created=True)
    class_group = models.ForeignKey(Sinf, on_delete=models.CASCADE)
    students_information = models.JSONField(default=None)
    weekday = models.CharField(max_length=30, default='Monday')

    def __str__(self):
        return str(self.class_group)

    class Meta:
        db_table = 'data_students'


# @receiver(post_save, sender=DataStudents)
# def update_stock(sender, instance, **kwargs):
#     daily()
#     instance.DataStudents.save()


class ByDay(models.Model):
    student_object = models.JSONField()
    created_at = models.DateField(auto_created=True)
    weekday = models.CharField(max_length=20, default='none')
    class_group = models.ForeignKey(Sinf, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_object

    class Meta:
        db_table = 'daily'
