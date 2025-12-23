import urllib.request
import base64
import re
import csv


url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)

response = urllib.request.urlopen(req)
html_content = response.read().decode('utf-8')

widgets = html_content.split('<div class="widgets-list__item">')

cleaned_matches = []

name_pattern = r'class="org-widget-header__title-link">([^<]+)</a>'
addr_pattern = r'class="org-widget-header__meta org-widget-header__meta--location">\s*([^<]+)\s*</span>'
phone_pattern = r'Телефон.*?class="spec__value">([^<]+)</dd>'
time_pattern = r'Часы работы.*?class="spec__value">([^<]+)</dd>'
url_encoded_pattern = r'data-url="([^"]+)"'
review_pattern = r'class="org-widget-feedback__comment">\s*<p>\s*(.*?)\s*</p>'

for widget in widgets:
    if 'class="org-widget "' not in widget:
        continue

    match = re.search(name_pattern, widget)
    name = match.group(1).strip() if match else '-'

    match = re.search(addr_pattern, widget)
    address = match.group(1).strip() if match else '-'

    match = re.search(phone_pattern, widget, re.S)
    phone = match.group(1).strip() if match else '-'

    match = re.search(time_pattern, widget, re.S)
    hours = match.group(1).strip() if match else '-'

    match = re.search(url_encoded_pattern, widget)
    if match:
        encoded_url = match.group(1)
        try:
            decoded_bytes = base64.b64decode(encoded_url)
            site_url = decoded_bytes.decode('utf-8')
        except:
            site_url = '-'
    else:
        site_url = '-'

    stars = re.findall(r'rating-stars__item--active', widget)
    rating = str(len(stars)) + ".0" if len(stars) > 0 else "0.0"

    match = re.search(review_pattern, widget, re.S)
    if match:
        review = match.group(1).strip().replace('\n', ' ').replace('\r', '')
    else:
        review = '-'

    cleaned_matches.append([name, address, phone, hours, site_url, rating, review])

with open('avtoservis.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    
    writer.writerow(['Название', 'Адрес', 'Телефоны', 'Часы работы', 'Сайт', 'Рейтинг', 'Отзыв'])
    writer.writerows(cleaned_matches)

print(f"Готово! Обработано {len(cleaned_matches)} записей. Результат в avtoservis.csv")
