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
    pages = soup.find_all('a', class_='z2r')
    if pages:
        return int(pages[-2].get_text())
    else:
        return 1
    
def get_content(html):  #создание списка
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="li6 l6i")
    coffe_machine = []
    for item in items:
        coffe_machine.append({
            'name':item.find('a', class_='tile-hover-target ji9').get_text().replace('Автоматическая кофемашина ',''),
            'model':item.find('a', class_='tile-hover-target ji9').get_text().replace('Автоматическая кофемашина ','').split(' ')[0],
            'link':HOST+item.find('a', class_='tile-hover-target ji9').get('href'),
            'price':item.find('div',class_='ui-n6').get_text().replace('\u2009','').split("₽")[0]})
    return coffe_machine

def save_file(items):
    with open('export.csv','w',newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name','model','link','price'])
        for item in items:
            writer.writerow([item['name'],item['model'],item['link'],item['price']])

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
        return coffe_machines
    else:
        print('error')

if __name__ == "__main__":
    parse()