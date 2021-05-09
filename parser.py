import re
import requests
import json
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

from converter import convert

URL = "https://lalafo.kg/kyrgyzstan/kvartiry"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "accept": "*/*"
}

driver = webdriver.Firefox()


def clear_phone(num: str):
    for i in num:
        if i in '()-+ Xx':
            num = num.replace(i, '')
    num = num.replace('\n', ' ')
    return num


def get_main_info(url: str):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    try:
        item = soup.find_all('div', class_="details-page__user-info")[0]
    except:
        item = soup.find_all('div', class_="details-page__user-info")

    driver.get(url)

    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="show-button"]')))
        element.click()
    except:
        pass

    try:
        info = item.find('p',class_="Paragraph secondary userStatus responseInfo").get_text().replace('\n', '. '),
    except:
        info = 'Нет информации о пользователе'
    
    try:
        phone = clear_phone(driver.find_element_by_class_name("phone-wrap").text)
    except:
        phone = 'Нет номера'

    result = {
        'Подзаголовок':item.find('span', class_="userName-text").get_text(strip=True),
        'Активность':info,
        'Номер':phone,
    }

    return result


def parse():
    result = []
    for i in range(10):
        html = requests.get(URL + '?page=%s' % i).content
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_="adTile-mainInfo")
        
        for item in items:
            main_info = get_main_info('https://lalafo.kg' + item.get('href'))
            result.append({
                'Заголовок':item.find('span', class_="adTile-title").get_text(strip=True),
                'Стоимость':item.find('p', class_="adTile-price").get_text(strip=True),
                'Подзаголовок':main_info['Подзаголовок'],
                'Активность':main_info['Активность'][0],
                'Номер':main_info['Номер'],
            })
    return result


convert(parse())
driver.close()



# print(parse())
# with open("lalafo_parse.json", "w") as outfile:
#     json.dump({'date':datetime.now().strftime('%Y-%m-%d / %H:%M:%S'), 'data':parse()}, outfile, ensure_ascii=False)
