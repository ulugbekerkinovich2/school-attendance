# Generated by Django 4.1.7 on 2023-03-06 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0008_alter_byday_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='byday',
            name='class_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.sinf', unique=True),
        ),
        migrations.AlterField(
            model_name='byday',
            name='created_at',
            field=models.DateField(auto_created=True, unique=True),
        ),
    ]
