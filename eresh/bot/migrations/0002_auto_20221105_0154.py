# Generated by Django 2.2.19 on 2022-11-04 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='eresh_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ID в ERESH'),
        ),
    ]
