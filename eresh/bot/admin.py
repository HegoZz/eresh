from django.contrib import admin

from .models import User


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('eresh_token',
                    'eresh_token_expires',
                    'eresh_email',
                    'eresh_id',
                    'tg_user_id',
                    'tg_nickname',
                    'registration_date',
                    'last_activity',
                    )
