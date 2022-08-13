import telebot
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
import numpy as np
from parser import compute_full_list_of_this_category

# Фильмы
url_armyanskie_filmy = 'https://armfilm.co/armyanskie-filmy/page/'
url_starie_armyanskie_filmi = 'https://armfilm.co/starie-armyanskie-filmi/page/'
url_filmy_na_armyanskom = 'https://armfilm.co/filmy-na-armyanskom/page/'
url_multfilmer = 'https://armfilm.co/multfilmer/page/'
url_hayeren_multer = 'https://armfilm.co/hayeren-multer/page/'

# Сериалы
url_serialy = 'https://armfilm.co/serialy/page/'
url_serialy_na_armyanskom = 'https://armfilm.co/serialy-s-armyanskim-perevodom/page/'
url_armyanskiye_sitkomy = 'https://armfilm.co/armyanskiye-sitkomy/page/'

# ТВ-Шоу
url_armyanskie_tv_shou = 'https://armfilm.co/armyanskie-tv-shou/page/'

# Песни
url_klipner = 'https://armfilm.co/klipner/page/'

# Армянские фильмы
top_div = 'clearfix grid-thumb'
class_div = 'shortstory short-film'
armyanskie_filmy = compute_full_list_of_this_category(url_armyanskie_filmy, top_div, class_div)
# Общий top_div, class_div
# top_div1 = 'main-left'
# class_div1 = 'shortstory'
# # Старые армянские фильмы
# starie_armyanskie_filmi = compute_full_list_of_this_category(url_starie_armyanskie_filmi, top_div1, class_div1)
# # Фильмы на армянском
# filmy_na_armyanskom = compute_full_list_of_this_category(url_filmy_na_armyanskom, top_div1, class_div1)
# # Армянские мультфильмы
# multfilmer = compute_full_list_of_this_category(url_multfilmer, top_div1, class_div1)
# # Мультфильмы на армянском
# hayeren_multer = compute_full_list_of_this_category(url_hayeren_multer, top_div1, class_div1)
# # Все последние сериалы
# serialy = compute_full_list_of_this_category(url_serialy, top_div1, class_div1)
# # Cериалы на армянском
# serialy_na_armyanskom = compute_full_list_of_this_category(url_serialy_na_armyanskom, top_div1, class_div1)
# # Армянские ситкомы
# url_armyanskiye_sitkomy = compute_full_list_of_this_category(url_armyanskiye_sitkomy, top_div1, class_div1)
# # ТВ-Шоу
# url_armyanskie_tv_shou = compute_full_list_of_this_category(url_armyanskie_tv_shou, top_div1, class_div1)
# # Песни
# klipner = compute_full_list_of_this_category(url_klipner, top_div1, class_div1)

# Стартуем бота после того как есть с чем работать, чтобы понимать, если бот подгрузился,
# значит все списки с фильмами готовы без ошибок и бот будет работать исправно
BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)
print('start')
print(armyanskie_filmy)

keyboard = types.ReplyKeyboardMarkup(True, True)
keyboard.row('Фильмы', 'Сериалы', 'ТВ-Шоу', 'Песни')

keyboard_films = types.ReplyKeyboardMarkup(True, True)
keyboard_films.row('Армянские фильмы')
keyboard_films.row('Старые армянские фильмы')
keyboard_films.row('Фильмы на армянском')
keyboard_films.row('Армянские мультфильмы')
keyboard_films.row('Мультфильмы на армянском')
keyboard_films.row('В начало меню')

keyboard_ser = types.ReplyKeyboardMarkup(True, True)
keyboard_ser.row('Все последние сериалы')
keyboard_ser.row('Сериалы на армянском')
keyboard_ser.row('Армянские ситкомы')
keyboard_ser.row('В начало меню')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Перейдите в удобное контекстное меню, или введите нужную категорию вручную',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_command(message):
    # keyboard = telebot.types.InlineKeyboardMarkup()
    # keyboard.add(
    #     telebot.types.InlineKeyboardButton(
    #         'Message the developer', url='telegram.me/artiomtb'
    #     )
    # )
    bot.send_message(
        message.chat.id,
        'ARMFilmbot - Мониторинг армянского Онлайн-ТВ, с возможностью отслеживания выбранных сериалов.\n' +
        '1) Чтобы начать пользоваться напишите /start в чат.\n' +
        '2) За более подробной информацией работы бота: githubcom//')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'фильмы':
        bot.send_message(message.chat.id, 'Фильмы', reply_markup=keyboard_films)
    elif message.text.lower() == 'сериалы':
        bot.send_message(message.chat.id, 'Сериалы', reply_markup=keyboard_ser)
    elif message.text.lower() == 'тв-шоу':
        current_page = '1'
        url = url_tv_shows
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_tv_shows = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'ТВ-Шоу', reply_markup=keyboard_tv_shows)

    elif message.text.lower() == 'песни':
        current_page = '1'
        url = url_songs
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_songs = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Песни', reply_markup=keyboard_songs)

    elif message.text.lower() == 'в начало меню':
        bot.send_message(message.chat.id, 'Вы вернулись в начальное меню', reply_markup=keyboard)
    elif message.text.split('\n')[0].lower() == 'армянские фильмы':
        send_page_armyanskie_filmy(message)

    elif message.text.lower() == 'старые армянские фильмы':
        current_page = '1'
        url = url_starie_armyanskie_filmi
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_star_armyan = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Старые армянские фильмы', reply_markup=keyboard_star_armyan)

    elif message.text.lower() == 'фильмы на армянском':
        current_page = '1'
        url = url_filmy_na_armyanskom
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_translated_armyan = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Фильмы на армянском', reply_markup=keyboard_translated_armyan)

    elif message.text.lower() == 'армянские мультфильмы':
        current_page = '1'
        url = url_multfilmer
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_multarmyan = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Армянские мультфильмы', reply_markup=keyboard_multarmyan)

    elif message.text.lower() == 'мультфильмы на армянском':
        current_page = '1'
        url = url_hayeren_multer
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_translated_multarmyan = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Мультфильмы на армянском', reply_markup=keyboard_translated_multarmyan)

    elif message.text.lower() == 'все последние сериалы':
        current_page = '1'
        url = url_serialy
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_serials = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Все последние сериалы', reply_markup=keyboard_serials)

    elif message.text.lower() == 'сериалы на армянском':
        current_page = '1'
        url = url_serialy_na_armyanskom
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_serialarmyan = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Cериалы на армянском', reply_markup=keyboard_serialarmyan)

    elif message.text.lower() == 'армянские ситкомы':
        current_page = '1'
        url = url_armyanskiye_sitkomy

        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_sitcome = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Армянские ситкомы', reply_markup=keyboard_sitcome)

    else:
        bot.send_message(message.chat.id, 'Такой команды нет.\nВведите /start , чтобы начать работу с ботом заного')


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'character')
def characters_page_callback(call):
    if call.data.count('#') == 1:
        page = int(call.data.split('#')[1])
        edit_page_armyanskie_filmy(call.message, page)


def send_page_armyanskie_filmy(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(armyanskie_filmy),
        current_page=page,
        data_pattern='character#{page}')

    bot.send_message(message.chat.id,
                     armyanskie_filmy[page - 1],
                     reply_markup=paginator.markup)


def edit_page_armyanskie_filmy(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(armyanskie_filmy),
        current_page=page,
        data_pattern='character#{page}')

    bot.edit_message_text(armyanskie_filmy[page - 1],
                          message.chat.id,
                          message.message_id,
                          reply_markup=paginator.markup)


# @bot.callback_query_handler(func=lambda call: True)
# # call.data это callback_data, которую мы указали при объявлении кнопки,
# # сюда будет стекаться и обрабатываться все от InlineKeyboardButtons.
# def callback_workers(call):
#     # обработка срабатываний на нажатий клавиш лисита:
#     if call.data == "-":
#         print(0)
#     elif call.data == "armyan_forward":
#         url = url_armyanskie_filmy
#         top_class_name_div = 'clearfix grid-thumb'
#         deep_class_name_div = 'shortstory short-film'
#         current_page, max_pages = '1', 8
#         current_page = str(int(current_page) + 1)
#         k_armyan = send_character_page(url, top_class_name_div, deep_class_name_div)
#         bot.edit_message_reply_markup(
#                             call.message.chat.id,
#                             call.message.message_id,
#                             reply_markup=k_armyan)
#     # elif call.data == "armyan_back":
#     #     current_page -= 1
#     #     names2, links2, p2 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
#     #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names2, links2, current_page, max_pages))
#     # elif call.data == "armyan_forward2":
#     #
#     #     current_page += str(int(current_page) + 10)
#     #     names3, links3, p3 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
#     #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names3, links3, current_page, max_pages))
#     # elif call.data == "armyan_back2":
#     #     current_page -= 10
#     #     names4, links4, p4 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
#     #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names4, links4, current_page, max_pages))
# def send_character_page(url, top, deep, current_page=1):
#     n1, l1, max_pages = big_work(url+str(current_page), top, deep)
#     if current_page == 1 and max_pages-current_page != 0:
#         keyboard = start_inline_keyboard(n1, l1, max_pages)
#         return keyboard
#     elif current_page == max_pages:
#         keyboard = end_inline_keyboard(n1, l1, max_pages)
#         return keyboard
#     elif current_page != 1:
#         keyboard = primary_inline_keyboard(n1, l1, current_page, max_pages)
#         return keyboard


# sticker react
# @bot.message_handler(content_types=['sticker'])
# def sticker_id(message):
#     print(message)
#


# Armyan_film
# def start_inline_keyboard(names, links, pages):
#     inline_k = types.InlineKeyboardMarkup()
#     for i in range(len(names)):
#         inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
#     btn_info = types.InlineKeyboardButton('Стр. {} из {}'.format(1, pages), callback_data='-')
#     btn_forward = types.InlineKeyboardButton('▶', callback_data='armyan_forward')
#     # btn_forward2 = types.InlineKeyboardButton('⏩', callback_data='armyan_forward2')
#     inline_k.add(btn_info, btn_forward)
#     return inline_k
#
#
# def primary_inline_keyboard(names, links, current, pages):
#     inline_k = types.InlineKeyboardMarkup(row_width=5)
#     for i in range(len(names)):
#         inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
#     # btn_back2 = types.InlineKeyboardButton('⏪', callback_data='armyan_back2')
#     btn_back = types.InlineKeyboardButton('◀', callback_data='armyan_back')
#     btn_info = types.InlineKeyboardButton('{} из {}'.format(current, pages), callback_data='-')
#     btn_forward = types.InlineKeyboardButton('▶', callback_data='armyan_forward')
#     # btn_forward2 = types.InlineKeyboardButton('⏩', callback_data='armyan_forward2')
#     inline_k.add(btn_back, btn_info, btn_forward)
#     return inline_k
#
#
# def end_inline_keyboard(names, links, pages):
#     inline_k = types.InlineKeyboardMarkup()
#     for i in range(len(names)):
#         inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
#     # btn_back2 = types.InlineKeyboardButton('⏪', callback_data='armyan_back2')
#     btn_back = types.InlineKeyboardButton('◀', callback_data='armyan_back')
#     btn_info = types.InlineKeyboardButton('Стр. {} из {}'.format(pages, pages), callback_data='-')
#     inline_k.add(btn_back, btn_info)
#     return inline_k


# Thread(Поток) для бота, непосредственно запуск бота
# с постоянным опросом и поддержкой в Телеграме
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
