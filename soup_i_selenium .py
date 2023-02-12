import re
import time
import requests
import lxml
from bs4 import BeautifulSoup as bs
import codecs
import html5lib
import html
import attr
from selenium import webdriver



# _____________________  parsing privat site clouse code_______
# потребовался headers чтобы не получить банан но он прилетал
# если не менялся валя на пк
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;\
 Intel Mac OS X 10.15; rv:76.1) Gecko/20100101 Firefox/76.1'}

# адрес состоит из несколько из базы url_strnica_1\
#     и присоеденямого доп адрес
url_strnica_1 =\
        "https://www.transfermarkt.com"#
url_strnica_2 = \
        "/detailsuche/spielerdetail/suche/39920876"
        # "/detailsuche/spielerdetail/suche/39920876/page/1"

# применяем библиотеку requests.get и собираем все данные
# с сайта в атрибуты вставляем сайт и данные кто мы для сайта
html_2 = requests.get\
        (url_strnica_1+url_strnica_2, headers=headers)
html_izmen_headers = html_2.text
# подключаем билиотеку BeautifulSoup as bs
html_izmen_headers_bs =bs\
        (html_izmen_headers, "html.parser")

gamer_goal={}
# если лист одно значегие применять только find

# функция для принятия урл адреса и поиск данных на нем
def href_gemers_list(div_class="columns",\
                in_dex=1,\
                teg_2 ="td",\
                teg_class ="hauptlink"):
    html_2 = requests.get \
        (url_strnica_1 + url_strnica_2, headers=headers)
    html_izmen_headers = html_2.text
    html_izmen_headers_bs = bs \
        (html_izmen_headers, "html.parser")
 # Ищем нужный тег и вписываем в атрибуты для поиска
    div = html_izmen_headers_bs.find_all\
        ("div", class_=div_class)[in_dex]
# требуется более глубокий поиск открываем \
#     еще атрибуты для поиска
    td_alls = div.find_all("td", class_=teg_class)
    # print(td_alls)
# полученые данные прогоняем через список и получаем индексы
# чтобы примеить к нужным нам тегам и далее достать через get
    for number in range(0, len(td_alls)):
        if number%3 == 0:
            # print(td_alls[number])
            url_gamer = td_alls[number].find("a").get("href")
            name_gamer = td_alls[number].find("a").get("title")
            # print(url_strnica_1 + url_gamer)
# Здесь столкнулся с проблемой достать определеный тег не отображал
# bs и за быстрого открывания страницы или блок самого сайта
# что пришлось применить библиотеку selenium import webdriver
# что потребовалось поставить в один репозиторий гугол дравейров
# не старше версии устоновленой на пк.
# все заработоло но удлиниля время парсинга -
            driver = webdriver.Chrome()#+
            driver.get(url_strnica_1 + url_gamer)#+
            html_3_gamer_headers_bs = bs(driver.page_source, "html.parser")#+

            # Исключить ошибку индекса стали возникать ошибки\
            # некоторые данные по голам игроков нет  if не помог
            # отловить все ошибки по этому пришлось применять исключения
            try:

                ht_ga_hed_bs = html_3_gamer_headers_bs.find_all \
                    ("a", class_="tm-player-performance__stats-list-item-value svelte-xwa5ea")[1].text#work -5 balov
                # print(ht_ga_hed_bs)
                if ht_ga_hed_bs == "-" or ht_ga_hed_bs == [] or ht_ga_hed_bs == None or ht_ga_hed_bs == False:
                    ht_ga_hed_bs=0
                gamer_goal.setdefault(name_gamer, int(ht_ga_hed_bs))
                print(gamer_goal)
            except :
                # сробатывает если есть ошибка и вкладывает количество голов
                # в словарь где имя игрока ключь данные голы
                ht_ga_hed_bs = 0
                gamer_goal.setdefault(name_gamer, int(ht_ga_hed_bs))
                print(gamer_goal)  # , len(ht_ga_hed_bs))

    print(gamer_goal)

# пришлось запускать функцию не помню перичный \
    # адрес до перебора педжинатора не нашел

td_all = href_gemers_list(div_class="large-12 columns",\
                in_dex=0,\
                teg_2 ="td",\
                teg_class ="hauptlink")

# print(gamer_goal, len(gamer_goal))

# определяем flag если ложь остонавливаем перебор он
# служит для работы while flag: метода и после когда \
#     закончатся подгружаемые педжинаторы будет окончание\
#     для перебора
flag=True
while flag:
    html_2 = requests.get\
        (url_strnica_1+url_strnica_2, headers=headers)
    html_izmen_headers = html_2.text
    html_izmen_headers_bs =bs\
        (html_izmen_headers, "html.parser")
    # ищем педжинаторы в сайте и вытаскиваем "href" работает без
    # билиотеки selenium что горазда ускоряет
    next_page_ = html_izmen_headers_bs.find\
    ("li", class_="tm-pagination__list-item--icon-next-page")\
    .find("a").get("href")
    # сравниваем ноый урл если есть то метод работает
    if next_page_ != None:
        # полученый href делаем для второй части адреса урл
        # и парсинга страницы
        url_strnica_2 = next_page_
    else:
        flag = False
    # применяем ранее сделаную функцию для
    # постояного парсинга данных самого игрока

    td_all = href_gemers_list(div_class="large-12 columns", \
                              in_dex=0, \
                              teg_2="td", \
                              teg_class="hauptlink")

# возникающие проблемы при скрабинге слетает
# парсер из за расоеденения через некоторок время






