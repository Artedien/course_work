from attr import fields
import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://www.wildberries.ru'

def get_html(url):
    try:
        results = requests.get(url)
        results.raise_for_status()
        return results.text
    except(requests.RequestException, ValueError,):
        print('Сетевая ошибка')
        return False

def get_coffeemachines():
    html = get_html('https://www.wildberries.ru/catalog/elektronika/tehnika-dlya-kuhni/prigotovlenie-napitkov?sort=popular&page=1&xsubject=1188#c6993633')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_coffeemachines = soup.findAll('div', class_="product-card j-card-item")
        result_coffeemachines = []
        
        for coffeemachines in all_coffeemachines:
            brand = coffeemachines.find('strong','span', class_="brand-name").text
            title = coffeemachines.find('span', class_="goods-name").text
            url = HOST + coffeemachines.find(class_="product-card__main j-open-full-product-card")['href']
            price = coffeemachines.find('span', class_="price").text.replace(' ','').replace('\xa0', ' ')
            
            result_coffeemachines.append({
                'brand': brand,
                'title': title,
                'url': url,
                'price': price
            })
            with open ('WB_coffeemachines.csv', 'w', encoding='utf-8') as file:
                fields = ['brand', 'title', 'url', 'price']
                writer = csv.DictWriter(file, fields, delimiter=';')
                writer.writeheader()
                for user in result_coffeemachines:
                    writer.writerow(user)
        return result_coffeemachines      
    return False
get_coffeemachines()





        
