# Generated by Django 4.2.11 on 2024-06-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_alter_realization_image_realizationimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realization',
            name='content',
            field=models.CharField(max_length=1000, verbose_name='Opis'),
        ),
    ]
