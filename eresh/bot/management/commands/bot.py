from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, ParseMode, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Здравствуйте, у Вас регистрация в сервисе ERESH?\n/yes\n/no',
        reply_markup=button
    )


def registering(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Придумайте имя пользователя',
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Придумайте пароль',
    )


def log_in(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите имя пользователя',
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите пароль',
    )



class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN)
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', wake_up))
        dp.add_handler(CommandHandler('yes', log_in))
        dp.add_handler(CommandHandler('no', registering))

        updater.start_polling()
        updater.idle()