# Generated by Django 4.1.7 on 2023-03-07 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sinf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='mavjud emas', max_length=20, unique=True)),
            ],
            options={
                'db_table': 'sinf',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=60, unique=True)),
                ('sinf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.sinf')),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='DataStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_created=True)),
                ('students_information', models.JSONField(default=None)),
                ('weekday', models.CharField(default='Monday', max_length=30)),
                ('class_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.sinf')),
            ],
            options={
                'db_table': 'data_students',
            },
        ),
        migrations.CreateModel(
            name='ByDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_created=True)),
                ('student_object', models.JSONField()),
                ('weekday', models.CharField(default='none', max_length=20)),
                ('class_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.sinf')),
            ],
            options={
                'db_table': 'daily',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
