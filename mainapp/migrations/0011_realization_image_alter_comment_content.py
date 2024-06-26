# Generated by Django 4.2.11 on 2024-06-16 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_alter_realization_options_alter_realization_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='realization',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='realization_images/', verbose_name='Zdjęcie'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=200, verbose_name=''),
        ),
    ]
