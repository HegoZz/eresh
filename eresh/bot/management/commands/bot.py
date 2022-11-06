from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import requests

from telegram import (
    Bot, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
)
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, ConversationHandler, Filters,
    MessageHandler, Updater,
)

from bot.models import User


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TOKEN)
user_data = {}

g_email, g_password, check = range(3)
URL = 'https://api.eresh.zemedia.ru/'


def cancel(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Ну отмена так отмена.',
        reply_markup=get_login_reply_keyboard()
    )
    return ConversationHandler.END


def get_inline_keyboard():
    keyboard = [
        [
        InlineKeyboardButton('💰💰💰Проверить балланс💰💰💰',
                             callback_data='check_ballance')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def combine_pair(pair):
    """ Комбинирование емейла и пароля в гет-параметры."""
    return f'/?email={pair[0]}&passwd={pair[1]}'


def go_login(update, context):
    """ Запись пароля в переменную."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_data}\nЩа как войду. Держись там.',
    )
    return ConversationHandler.END


def get_login_reply_keyboard():
    keyboard = [
        [
            KeyboardButton('/login'),
            KeyboardButton('/registration'),
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_email(update, context):
    """ Запись емейла в переменную и запрос пароля."""
    user_id = update.message.from_user.id
    user_email = update.message.text
    user_data[user_id] = [user_email,]
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_data}\nВведите свой пароль.',
    )
    return g_password


def get_password(update, context):
    """ Запись пароля в переменную."""
    user_id = update.message.from_user.id
    user_password = update.message.text
    chat = update.effective_chat
    user_data[user_id].append(user_password)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_data}\nВсё верно?\n/yes\n/cancel',
        #entities=[{'length': 20, 'offset': 1, 'type': 'spoiler'}],
    )
    return check


def go_login(update, context):
    """ Запрос на вход."""
    chat = update.effective_chat
    user_id = update.message.from_user.id
    nickname = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Ну что, {nickname}, держись - я вхожу!\n'
              '(сообщение с паролем стоитудалить)'),
    )
    combined_pair = combine_pair(user_data[user_id])
    url = URL + 'login' + combined_pair
    response = requests.get(url).json()
    status = response.get('status')
    if status == 0:
        error = response.get('error')
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Что-то пошло не так...\n{error}',
        )
        logger.error("Ошибка: %s", error)
    elif status == 1:
        token = response.get('token')
        vk_id = response.get('vkid')
        log_debug = write_to_base(
            token, user_data[user_id][0], vk_id, user_id, nickname
        )
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Вход осуществлён.\nТеперь можно проверить балланс.',
            reply_markup=get_inline_keyboard(),
        )
        logger.debug("Данные: %s", log_debug)
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Вообще лажа какая-то...',
        )
    return ConversationHandler.END


def go_reg(update, context):
    """ Запрос на регистрацию."""
    chat = update.effective_chat
    user_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_data}\nЩа зарегаю.',
    )
    combined_pair = combine_pair(user_data[user_id])
    url = URL + 'reg' + combined_pair
    response = requests.get(url).json()
    status = response.get('status')
    if status == 0:
        error = response.get('error')
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Что-то пошло не так...\n{error}',
        )
        logger.error("Ошибка: %s", error)
    elif status == 1:
        token = response.get('token')
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Подтвердите почту.',
            reply_markup=get_login_reply_keyboard(),
        )
        log_debug = token
        logger.debug("Данные: %s", log_debug)
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Вообще лажа какая-то...',
        )
    return ConversationHandler.END


def inline_keyboard_handler(update, context, *args, **kwargs):
    """ Обработка запросов инлайн-кнопок."""
    query = update.callback_query
    data = query.data
    chat_id = update.effective_message.chat_id
    user = User.objects.get(tg_user_id=chat_id)
    token = user.eresh_token
    if data == 'check_ballance':
        url = URL + 'user/getbalance/?token=' + token
        response = requests.get(url).json()
        status = response.get('status')
        if status == 1:
            balance = response.get('balance')
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Ваш балланс -- военная тайна.',
            )
        query.edit_message_text(
            text=f'Ваш балланс = {balance}',
            reply_markup=get_inline_keyboard()
        )



def login(update, context):
    """ Запрос емейла для входа."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите свой емейл.\n /cancel для отмены.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return g_email


def wake_up(update, context):
    """ Начало работы. Запуск бота."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Здравствуйте, войдите в аккаунт ERESH или зарегистрируйтесь.',
        reply_markup=get_login_reply_keyboard()
    )


def write_to_base(token, mail, vk_id, tg_id, tg_nickname):
    """ Запись в базу данных."""
    User.objects.update_or_create(
        eresh_token=token,
        eresh_email=mail,
        eresh_id=vk_id,
        tg_user_id=tg_id,
        tg_nickname=tg_nickname,
    )


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        button_handler = CallbackQueryHandler(callback=inline_keyboard_handler)
        login_handler = ConversationHandler(
            entry_points=[CommandHandler('login', login)],
            states={
                g_email: [MessageHandler(Filters.text, get_email)],
                g_password: [MessageHandler(Filters.text, get_password)],
                check:[CommandHandler('yes', go_login)]
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        registration_handler = ConversationHandler(
            entry_points=[CommandHandler('registration', login)],
            states={
                g_email: [MessageHandler(Filters.text, get_email)],
                g_password: [MessageHandler(Filters.text, get_password)],
                check:[CommandHandler('yes', go_reg)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        start = CommandHandler('start', wake_up)

        dp = updater.dispatcher
        dp.add_handler(start)
        dp.add_handler(login_handler)
        dp.add_handler(registration_handler)
        dp.add_handler(button_handler)

        updater.start_polling(poll_interval=10)
        updater.idle()