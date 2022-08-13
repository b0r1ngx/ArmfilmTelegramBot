import telebot
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
import requests
import numpy as np
from bs4 import BeautifulSoup

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

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
    elif message.text.lower() == 'армянские фильмы':
        # current_page = 1
        url = url_armyanskie_filmy
        topn = 'clearfix grid-thumb'
        classn = 'shortstory short-film'
        # names, links, pages = big_work(url+str(current_page), topn, classn)
        keyboard_armyan = send_character_page(url, topn, classn)
        # for i in range(2, pages + 1):
        #     text = get_text('https://armfilm.co/armyanskie-filmy/page/{}/'.format(i))
        #     dirty_list = get_dirty_items_and_max_pages(text, topn, classn)
        #     local_names, local_links = get_items(dirty_list, find_name_from, end_name_find, find_url_from, end_url_find)
        #
        #     if i != pages:
        #         keyboard_armyan = primary_inline_keyboard(local_names, local_links, i, pages)
        #     else:
        #         keyboard_armyan = end_inline_keyboard(local_names, local_links, pages)
        bot.send_message(message.chat.id, 'Армянские фильмы', reply_markup=keyboard_armyan)

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
        bot.send_message(message.chat.id, 'фильмы на армянском', reply_markup=keyboard_translated_armyan)

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
        topn = 'main-left'
        classn = 'shortstory'
        names, links, pages = big_work(url + current_page, topn, classn)
        keyboard_sitcome = start_inline_keyboard(names, links, pages)
        bot.send_message(message.chat.id, 'Армянские ситкомы', reply_markup=keyboard_sitcome)

    else:
        bot.send_message(message.chat.id, 'Такой команды нет.\nВведите /start , чтобы начать работу с ботом заного')


@bot.callback_query_handler(func=lambda call: True)
# call.data это callback_data, которую мы указали при объявлении кнопки,
# сюда будет стекаться и обрабатываться все от InlineKeyboardButtons.
def callback_workers(call):
    # обработка срабатываний на нажатий клавиш лисита:
    if call.data == "-":
        print(0)
    elif call.data == "armyan_forward":
        url = url_armyanskie_filmy
        top_class_name_div = 'clearfix grid-thumb'
        deep_class_name_div = 'shortstory short-film'
        current_page, max_pages = '1', 8
        current_page = str(int(current_page) + 1)
        k_armyan = send_character_page(url, top_class_name_div, deep_class_name_div)
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=k_armyan)
    # elif call.data == "armyan_back":
    #     current_page -= 1
    #     names2, links2, p2 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
    #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names2, links2, current_page, max_pages))
    # elif call.data == "armyan_forward2":
    #
    #     current_page += str(int(current_page) + 10)
    #     names3, links3, p3 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
    #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names3, links3, current_page, max_pages))
    # elif call.data == "armyan_back2":
    #     current_page -= 10
    #     names4, links4, p4 = big_work(url + current_page, top_class_name_div, deep_class_name_div)
    #     bot.edit_message_text(reply_markup=primary_inline_keyboard(names4, links4, current_page, max_pages))


def send_character_page(url, top, deep, current_page=1):
    n1, l1, max_pages = big_work(url + str(current_page), top, deep)
    if current_page == 1 and max_pages - current_page != 0:
        keyboard = start_inline_keyboard(n1, l1, max_pages)
        return keyboard
    elif current_page == max_pages:
        keyboard = end_inline_keyboard(n1, l1, max_pages)
        return keyboard
    elif current_page != 1:
        keyboard = primary_inline_keyboard(n1, l1, current_page, max_pages)
        return keyboard


# sticker react
# @bot.message_handler(content_types=['sticker'])
# def sticker_id(message):
#     print(message)
#

def get_text(url):
    r = requests.get(url)
    t = r.text
    return t


def max_pages(text):
    soup = BeautifulSoup(text, "lxml")
    # ищем сколько страниц по конкретной категории
    max_pages = str(soup.find('div', {'class': 'pages'}))
    find_beg = max_pages.rfind('">')
    find_end = max_pages.rfind('</a>')
    max_pages = int(max_pages[find_beg + 2:find_end])
    return max_pages


def get_dirty_items_and_max_pages(text, top_name, class_name):
    soup = BeautifulSoup(text, "lxml")

    film_list = soup.find('div', {'class': top_name})
    items = film_list.find_all('div', {'class': [class_name]})

    dirty_list = []

    for item in items:
        dirty_list.append(str(item.find('a')))
    return dirty_list


def get_items(dirty_list, start_name, end_name, start_url, end_url):
    # get names and links
    # из "грязной" версии забираем имена и прямые URL-ы
    names = []
    links = []

    for row in dirty_list:
        if row != 'None':
            i_beg_name = row.find(start_name)
            i_end_name = row.rfind(end_name)
            i_beg_url = row.find(start_url)
            i_end_url = row.rfind(end_url)
            if i_beg_url != -1 & i_end_url != -1 \
                    & i_beg_name != -1 & i_end_name != -1:
                names.append(row[i_beg_name + 7:i_end_name])
                links.append(row[i_beg_url:i_end_url])
    return names, links


# Films
url_armyanskie_filmy = 'https://armfilm.co/armyanskie-filmy/page/'
url_starie_armyanskie_filmi = 'https://armfilm.co/starie-armyanskie-filmi/page/'
url_filmy_na_armyanskom = 'https://armfilm.co/filmy-na-armyanskom/page/'
url_multfilmer = 'https://armfilm.co/multfilmer/page/'
url_hayeren_multer = 'https://armfilm.co/hayeren-multer/page/'

# Serial
url_serialy = 'https://armfilm.co/serialy/page/'
url_serialy_na_armyanskom = 'https://armfilm.co/serialy-s-armyanskim-perevodom/page/'
url_armyanskiye_sitkomy = 'https://armfilm.co/armyanskiye-sitkomy/page/'

# TV-Shows
url_tv_shows = 'https://armfilm.co/armyanskie-tv-shou/page/'

# Songs
url_songs = 'https://armfilm.co/klipner/page/'

# ключевые слова для поиска названия и ссылки:
find_url_from = 'armfilm'
end_url_find = '">\n<img'
find_name_from = 'title="'
end_name_find = '"/>\n<span'


def big_work(url, top_class_name_div, deep_class_name_div):
    text = get_text(url)
    dirty_list = get_dirty_items_and_max_pages(text, top_class_name_div, deep_class_name_div)
    pages = max_pages(text)
    names, links = get_items(dirty_list, find_name_from, end_name_find, find_url_from, end_url_find)
    return names, links, pages


# Armyan_film
def start_inline_keyboard(names, links, pages):
    inline_k = types.InlineKeyboardMarkup()
    for i in range(len(names)):
        inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
    btn_info = types.InlineKeyboardButton('Стр. {} из {}'.format(1, pages), callback_data='-')
    btn_forward = types.InlineKeyboardButton('▶', callback_data='armyan_forward')
    # btn_forward2 = types.InlineKeyboardButton('⏩', callback_data='armyan_forward2')
    inline_k.add(btn_info, btn_forward)
    return inline_k


def primary_inline_keyboard(names, links, current, pages):
    inline_k = types.InlineKeyboardMarkup(row_width=5)
    for i in range(len(names)):
        inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
    # btn_back2 = types.InlineKeyboardButton('⏪', callback_data='armyan_back2')
    btn_back = types.InlineKeyboardButton('◀', callback_data='armyan_back')
    btn_info = types.InlineKeyboardButton('{} из {}'.format(current, pages), callback_data='-')
    btn_forward = types.InlineKeyboardButton('▶', callback_data='armyan_forward')
    # btn_forward2 = types.InlineKeyboardButton('⏩', callback_data='armyan_forward2')
    inline_k.add(btn_back, btn_info, btn_forward)
    return inline_k


def end_inline_keyboard(names, links, pages):
    inline_k = types.InlineKeyboardMarkup()
    for i in range(len(names)):
        inline_k.add(types.InlineKeyboardButton('{}'.format(names[i]), url='{}'.format(links[i])))
    # btn_back2 = types.InlineKeyboardButton('⏪', callback_data='armyan_back2')
    btn_back = types.InlineKeyboardButton('◀', callback_data='armyan_back')
    btn_info = types.InlineKeyboardButton('Стр. {} из {}'.format(pages, pages), callback_data='-')
    inline_k.add(btn_back, btn_info)
    return inline_k


# Thread(Поток) для бота, непосредственно запуск бота
# с постоянным опросом и поддержкой в Телеграме
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
