from telebot import TeleBot
from telegram_bot_pagination import InlineKeyboardPaginator
from data import character_pages

BOT_TOKEN = ''
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def get_character(message):
    send_character_page(message)

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'character')
def characters_page_callback(call):
    page = int(call.data.split('#')[1])

    send_character_page_(call.message, page)

def send_character_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(character_pages),
        current_page=page,
        data_pattern='character#{page}')

    bot.send_message(message.chat.id,
                     character_pages[page - 1],
                     reply_markup=paginator.markup)

def send_character_page_(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(character_pages),
        current_page=page,
        data_pattern='character#{page}')

    bot.edit_message_text(character_pages[page-1],
                          message.chat.id,
                          message.message_id,
                          reply_markup=paginator.markup)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)

