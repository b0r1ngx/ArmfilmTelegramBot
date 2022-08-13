from bs4 import BeautifulSoup
import requests

find_url_from = 'armfilm'
end_url_find = '">\n<img'
find_name_from = 'title="'
end_name_find = '"/>\n<span'


def get_text(url):
    r = requests.get(url)
    t = r.text
    return t


def max_pages(text):
    soup = BeautifulSoup(text, "lxml")
    # ищем сколько страниц по конкретной категории
    pages = str(soup.find('div', {'class': 'pages'}))
    find_beg = pages.rfind('">')
    find_end = pages.rfind('</a>')
    pages = int(pages[find_beg + 2:find_end])
    return pages


def get_dirty_items(text, top_name, class_name):
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


# def big_work(url, top_class_name_div, deep_class_name_div):
#     text = get_text(url)
#     dirty_list, pages = get_dirty_items(text, top_class_name_div, deep_class_name_div)
#     names, links = get_items(dirty_list, find_name_from, end_name_find, find_url_from, end_url_find)
#     return names, links, pages


def compute_full_list_of_this_category(url, top_n, class_n):
    text = get_text(url + '1')
    pages = max_pages(text)
    final_list = []
    for page in range(1, pages + 1):
        text = get_text(url + str(page))
        dirty_list = get_dirty_items(text, top_n, class_n)
        names, links = get_items(dirty_list, find_name_from, end_name_find, find_url_from, end_url_find)
        final_list.append(names)
    return final_list
