from django.db import models

class User(models.Model):
    eresh_token = models.TextField(
        verbose_name='Токен в ERESH',
        unique=True,
    )
    eresh_email = models.EmailField(
        verbose_name='Почта',
    )
    eresh_id = models.PositiveIntegerField(
        verbose_name='ID в ERESH',
        null = True,
        blank = True,
    )
    tg_user_id = models.PositiveIntegerField(
        verbose_name='ID в телеге',
    )
    tg_nickname = models.TextField(
        verbose_name='Логин в телеге',
    )
    registration_date = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )
    last_activity = models.DateTimeField(
        verbose_name='Последняя активность',
        auto_now=True
    )

    def __str__(self):
        return f'{self.tg_nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

