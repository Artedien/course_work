import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession  
import csv



URL = 'https://www.ozon.ru/category/kofemashiny-dlya-molotogo-kofe-31660/'
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0','accept':'*/*'}
HOST = 'https://www.ozon.ru'

def get_html(url,params = None):  #получение страницы
    r = requests.get(url,headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('a', class_='yq3')
    if pages:
        return int(pages[-2].get_text())
    else:
        return 1
    


def get_content(html):  #создание списка
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="y6h hy7")
    coffe_machine = []
    for item in items:
        coffe_machine.append({
            'title':item.find('a', class_='tile-hover-target w9h').get_text(),
            'link':HOST+item.find('a', class_='tile-hover-target w9h').get('href'),
            'price':item.find('div',class_='ui-q0').get_text().replace('\u2009',' ').replace(' ','').replace('₽','₽ ')
        })
    return coffe_machine


def save_file(items):
    with open('export.csv','w',newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title','link','price'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['price']])

def parse(): #основная функция
    html = get_html(URL)
    coffe_machines= []
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        for page in range (1, pages_count+1):
            print (f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            coffe_machines.extend(get_content(html.text))
        save_file(coffe_machines)
    else:
        print('error')

parse()