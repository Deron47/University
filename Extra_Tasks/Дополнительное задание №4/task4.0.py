import urllib.request
import base64
import re
import csv

url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"


headers = {'Banana': 'Mozilla/5.0'}

req = urllib.request.Request(url)

response = urllib.request.urlopen(req)
html_data = response.read().decode('utf-8')

items = html_data.split('<div class="widgets-list__item">')

data_list = []

pattern_name = r'class="org-widget-header__title-link">([^<]+)</a>'
pattern_address = r'class="org-widget-header__meta org-widget-header__meta--location">\s*([^<]+)\s*</span>'
pattern_phone = r'Телефон.*?class="spec__value">([^<]+)</dd>'
pattern_time = r'Часы работы.*?class="spec__value">([^<]+)</dd>'
pattern_site = r'data-url="([^"]+)"'
pattern_review = r'class="org-widget-feedback__comment">\s*<p>\s*(.*?)\s*</p>'

for item in items:
    if 'class="org-widget "' not in item:
        continue

    match = re.search(pattern_name, item)
    if match:
        name = match.group(1).strip()
    else:
        name = '-'

    match = re.search(pattern_address, item)
    if match:
        address = match.group(1).strip()
    else:
        address = '-'

    match = re.search(pattern_phone, item, re.DOTALL)
    if match:
        phone = match.group(1).strip()
    else:
        phone = '-'

    match = re.search(pattern_time, item, re.DOTALL)
    if match:
        hours = match.group(1).strip()
    else:
        hours = '-'

    match = re.search(pattern_site, item)
    if match:
        code = match.group(1)
        try:
            decoded = base64.b64decode(code)
            site = decoded.decode('utf-8')
        except:
            site = '-'
    else:
        site = '-'

    stars = re.findall(r'rating-stars__item--active', item)
    if len(stars) > 0:
        rating = str(len(stars)) + ".0"
    else:
        rating = "0.0"

    match = re.search(pattern_review, item, re.DOTALL)
    if match:
        review = match.group(1).strip()
        review = review.replace('\n', ' ')
    else:
        review = '-'

    data_list.append([name, address, phone, hours, site, rating, review])

with open('avtoservis.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    writer.writerow(['Название', 'Адрес', 'Телефоны', 'Часы работы', 'Сайт', 'Рейтинг', 'Отзыв'])
    
    writer.writerows(data_list)

print("Все готово. Файл avtoservis.csv создан.")
