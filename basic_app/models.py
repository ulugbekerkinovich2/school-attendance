import datetime
import json
import sqlite3

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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


# class DataStudentsManager(models.Manager):
# def get_queryset(self, request=None):
#     queryset = super().get_queryset()
#     current_date = datetime.now().date()
#     if request and request.query_params.get('weekly') == 'weekly':
#         week_number = current_date.isocalendar()[1]
#         queryset = queryset.filter(created_at__week=week_number, weekday=current_date.strftime('%A'))
#         # print(queryset, '-------')
#     return queryset


class DataStudents(models.Model):
    created_at = models.DateField(auto_created=True)
    class_group = models.ForeignKey(Sinf, on_delete=models.CASCADE)
    students_information = models.JSONField(default=None)
    weekday = models.CharField(max_length=30, default='Monday')

    def formatted_date(self):
        return self.created_at.strftime('%Y.%m.%d')

    def __str__(self):
        return str(self.class_group)

    class Meta:
        db_table = 'data_students'

    @staticmethod
    def process_data_students():
        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM data_students ORDER BY created_at DESC LIMIT 1')
        row = cursor.fetchone()

        if row is not None:
            # Extract the necessary information from the record
            created_at, record_id, students_info_json, week, class_id = row
            print(created_at, 'bu yaratildi')
            created_at_parts = created_at.split('-')
            print(created_at_parts, 'shu')
            year, month, day = int(created_at_parts[0]), int(created_at_parts[1]), int(created_at_parts[2])
            print(year, month, day)
            # Convert the students information from JSON to Python objects
            students_info = json.loads(students_info_json)

            results = []
            week_names = []
            for student_info in students_info:
                name = student_info['name']
                absent = student_info['absent']
                cleanly = student_info['cleanly']
                uniform = student_info['uniform']

                absent_ball = 5 if absent else 0
                jami_ball = absent_ball + cleanly + uniform
                weekday_name = datetime.date(year, month, day).strftime("%A")
                week_names.append(weekday_name)
                # Create a dictionary representing the result for this student
                result = {'name': name, 'overall': jami_ball}
                results.append(result)

            # Convert the results to JSON
            results_json = json.dumps(results)
            print(results_json)

            # Insert the results into the daily table
            cursor.execute(
                "INSERT OR IGNORE INTO daily (student_object, created_at, weekday, class_group_id) VALUES (?, ?, ?, ?)",
                (results_json, created_at, week_names[0], class_id))
            connect.commit()
            cursor.execute("UPDATE data_students SET weekday = ? WHERE id = ?", (week_names[0], record_id))
            connect.commit()

        else:
            print("No records found in data_students table.")

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
