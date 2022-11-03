from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot, CallbackQuery
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler, CommandHandler
from telegram.ext import ConversationHandler, Filters
from telegram.ext import MessageHandler, Updater


bot = Bot(token=settings.TOKEN)

EMAIL, PASSWORD = range(2)

# waiting_for_email = set()
# waiting_for_password = set()
# waiting_for_reg = set()
# waiting_for_log_in = set()

# CALLBACK_BUTTON_HAVE_REG = 'callback_button_have_reg'
# CALLBACK_BUTTON_NO_REG = 'callback_button_no_reg'

# TITLES = {
#    CALLBACK_BUTTON_HAVE_REG: 'Есть. Войти',
#    CALLBACK_BUTTON_NO_REG: 'Нет. Зарегистрироваться',
# }


def cancel(update, _):
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


# def get_question_registration_keyboard():
#     """ Клавиатура с кнопками есть-нет."""
#     keyboard = [
#         [InlineKeyboardButton(TITLES[CALLBACK_BUTTON_HAVE_REG],
#                               callback_data=CALLBACK_BUTTON_HAVE_REG),
#         InlineKeyboardButton(TITLES[CALLBACK_BUTTON_NO_REG],
#                               callback_data=CALLBACK_BUTTON_NO_REG)]
#     ]
#     return InlineKeyboardMarkup(keyboard)


# def keyboard_callback_handler(update, chat_data=None, **kwargs):
#     """ Обработчик всех кнопок со всех клавиатур."""
#     query = update.callback_query
#     data = query.data

#     chat_id = update.effective_message.chat_id
#     current_text = update.effective_message.text

#     if data == CALLBACK_BUTTON_HAVE_REG:
#         query.edit_message_text(
#             text=current_text
#         )
#         bot.send_message(
#             chat_id=chat_id,
#             text='Мы рады, что Вы уже с нами!\nВведите Ваш емейл.',
#         )
#         waiting_for_email.add(chat_id)
#         waiting_for_log_in.add(chat_id)
#         print('1 --  ', waiting_for_email, waiting_for_log_in)

#     elif data == CALLBACK_BUTTON_NO_REG:
#         query.edit_message_text(
#             text=current_text
#         )
#         bot.send_message(
#             chat_id=chat_id,
#             text='Мы рады, что Вы к нам присоединились!\nВведите Ваш емейл.',
#         )
#         waiting_for_email.add(chat_id)
#         waiting_for_reg.add(chat_id)

def get_email(update, context):
    """ Запись емейла в переменную и запрос пароля."""
    user_id = update.message.from_user.id
    user_email = update.message.text
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_id} -- {user_email}\nВведите свой пароль.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return PASSWORD


def get_password_login(update, context):
    """ Запись пароля в переменную."""
    user_id = update.message.from_user.id
    user_password = update.message.text
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_id} -- {user_password}\nСпасибо.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def get_password_reg(update, context):
    """ Запись пароля в переменную."""
    user_id = update.message.from_user.id
    user_password = update.message.text
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{user_id} -- {user_password}\nЩа как зарегаю.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def login(update, context):
    """ Запрос емейла для входа."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Введите свой емейл.\n /cancel для отмены.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return EMAIL


# def need_password(update, context):
#     """ Запрос пароля."""
#     chat = update.effective_chat
#     current_email = update.effective_message.text


#     if chat in waiting_for_log_in:
#         text = 'Введите пароль'
#     elif chat in waiting_for_reg:
#         text = 'Придумайте пароль'

#     context.bot.send_message(
#         chat_id=chat.id,
#         text=text,
#     )
#     waiting_for_password.add(chat.id)
#     waiting_for_email.discard(chat.id)
 

def wake_up(update, context):
    """ Начало работы. Запуск бота."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Здравствуйте, войдите в аккаунт ERESH или зарегистрируйтесь.',
        reply_markup=get_login_reply_keyboard()
    )


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        start = CommandHandler('start', wake_up)
        # buttons_handler = CallbackQueryHandler(
        #     callback=keyboard_callback_handler,
        #     pass_chat_data=True
        # )
        login_handler = ConversationHandler(
            entry_points=[CommandHandler('login', login)],
            states={
                EMAIL: [MessageHandler(Filters.text, get_email)],
                PASSWORD: [MessageHandler(Filters.text, get_password_login)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        registration_handler = ConversationHandler(
            entry_points=[CommandHandler('registration', login)],
            states={
                EMAIL: [MessageHandler(Filters.text, get_email)],
                PASSWORD: [MessageHandler(Filters.text, get_password_reg)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )

        dp = updater.dispatcher
        dp.add_handler(start)
        # dp.add_handler(buttons_handler)
        dp.add_handler(login_handler)
        dp.add_handler(registration_handler)

        updater.start_polling()
        updater.idle()