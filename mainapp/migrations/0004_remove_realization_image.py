# Generated by Django 4.2.11 on 2024-05-13 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_remove_message_appointment_delete_appointment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realization',
            name='image',
        ),
    ]
