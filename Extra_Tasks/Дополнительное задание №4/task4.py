import re
import csv

with open('html.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

widgets = html_content.split('<div class="widgets-list__item">')

cleaned_matches = []

# Паттерны для поиска
name_pattern = r'class="org-widget-header__title-link">([^<]+)</a>'
addr_pattern = r'class="org-widget-header__meta org-widget-header__meta--location">\s*([^<]+)\s*</span>'
phone_pattern = r'Телефон.*?class="spec__value">([^<]+)</dd>'
time_pattern = r'Часы работы.*?class="spec__value">([^<]+)</dd>'
review_pattern = r'class="org-widget-feedback__comment">\s*<p>\s*(.*?)\s*</p>'

for widget in widgets:
    if 'class="org-widget "' not in widget:
        continue

    # Название
    match = re.search(name_pattern, widget)
    name = match.group(1).strip() if match else '-'

    # Адрес
    match = re.search(addr_pattern, widget)
    address = match.group(1).strip() if match else '-'

    # Телефон
    match = re.search(phone_pattern, widget, re.S)
    phone = match.group(1).strip() if match else '-'

    # Часы работы
    match = re.search(time_pattern, widget, re.S)
    hours = match.group(1).strip() if match else '-'

    # Рейтинг
    stars = re.findall(r'rating-stars__item--active', widget)
    rating = str(len(stars)) + ".0" if len(stars) > 0 else "0.0"

    # Текст отзыва
    match = re.search(review_pattern, widget, re.S)
    if match:
        review = match.group(1).strip().replace('\n', ' ').replace('\r', '')
    else:
        review = '-'

    cleaned_matches.append([name, address, phone, hours, rating, review])

with open('avtoservis.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',') 
    
    writer.writerow(['Название', 'Адрес', 'Телефоны', 'Часы работы', 'Рейтинг', 'Отзыв'])
    writer.writerows(cleaned_matches)

print("Готово! Данные сохранены в avtoservis.csv")
