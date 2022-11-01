from tabnanny import verbose
from django.db import models

class User(models.Model):
    eresh_token = models.TextField(
        verbose_name='Токен в ERESH',
        unique=True,
    )
    eresh_token_expires = models.DateTimeField(
        verbose_name='Время смерти токена'
    )
    eresh_email = models.EmailField(
        verbose_name='Почта',
        unique=True,
    )
    eresh_id = models.PositiveIntegerField(
        verbose_name='ID в ERESH',
        unique=True,
    )
    tg_user_id = models.PositiveIntegerField(
        verbose_name='ID в телеге',
        unique=True,
    )
    tg_nickname = models.TextField(
        verbose_name='Логин в телеге',
        unique=True,
    )
    balance = models.FloatField(
        verbose_name='Балланс',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.tg_nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

