import re

import requests
from bs4 import BeautifulSoup

from typing import List, Dict, Any


def get_book_data(book_url: str) -> dict:
    """
    Получает данные о книге с веб-страницы:
    название, цену, рейтинг, наличие, описание и дополнительные характеристики из таблицы.

    Args:
        book_url (str): URL страницы книги

    Returns:
        dict: Словарь с данными о книге. Структура:
            - 'name' (str): Название книги
            - 'price' (str): Цена книги
            - 'rating' (str): Рейтинг книги
            - 'quantity_in_stock' (str): Информация о наличии
            - 'description' (str): Описание книги
            - 'extra_feature' (dict): Дополнительные характеристики
    Raises:
        requests.RequestException: При ошибках сетевого запроса.
    """

    try:
        response = requests.get(book_url, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        all_feat = {}
        soup = BeautifulSoup(response.text, 'html.parser')

        # Название книги
        name_el = soup.find('h1')
        all_feat['name'] = name_el.get_text().strip() if name_el else None

        # Цена
        price_el = soup.find('p', {'class': "price_color"})
        all_feat['price'] = price_el.get_text() if price_el else None

        # Рейтинг
        rating_el = soup.find('p', {'class': "star-rating"})
        all_feat['rating'] = rating_el.get('class')[-1] if rating_el else None

        # Количество в наличии
        qt = re.compile(r'\d+')
        availability_el = soup.find('p', {'class': "instock availability"})

        if availability_el:
            availability = availability_el.get_text()
            all_feat['quantity_in_stock'] = re.search(qt, availability).group()
        else:
            all_feat['quantity_in_stock'] = None

        # Описание
        description_header = soup.find('div', {'id': 'product_description'})

        if description_header:
            description_el = description_header.find_next_sibling('p')
            all_feat['description'] = description_el.get_text() if description_el else None
        else:
            all_feat['description'] = None

        # Дополнительные характеристики из таблицы
        features = soup.find('table', {'class': 'table'}).find_all('tr')
        extra_feat = {}

        if features:
            for feature in features:
                th_el = feature.find('th')
                td_el = feature.find('td')
                extra_feat[th_el.get_text().strip().lower()] = td_el.get_text().strip() if th_el and td_el else None

        all_feat['extra_feature'] = extra_feat

        return all_feat

    except requests.RequestException as e:
        print(f'Ошибка при сетевом запросе: {e}')
        return {}

    except Exception as e:
        print(f'Ошибка при парсинге: {e}')
        return {}


def scrape_books(is_save: bool = False) -> List[Dict[str, Any]]:
    """
    Осуществлять парсинг всех страниц

    Args:
        is_save (bool): Аргумент-флаг, отвечающий за сохранение данных книг в файл

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о книгах
    """

    num_page = 1
    ref_book = []
    all_books = []

    while True:
        base_url = f'https://books.toscrape.com/catalogue/page-{num_page}.html'

        try:
            response = requests.get(base_url, timeout=10)

            if response.status_code == 404:
                break

            response.raise_for_status()
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            books_page = soup.find_all('article', {'class': 'product_pod'})

            # Формируем список ссылок на книги
            if books_page:
                for book in books_page:
                    link = book.find('a')
                    if link and link.get('href'):
                        ref_book.append(link['href'])
                    else:
                        continue
            else:
                continue

            num_page += 1

        except requests.RequestException as e:
            print(f'Ошибка при запросе страницы {num_page}: {e}')
            break

    # Получаем данные для каждой книги
    for ref in ref_book:
        book_url = 'http://books.toscrape.com/catalogue/' + ref
        book_data = get_book_data(book_url)
        if book_data:
            all_books.append(book_data)

    # Сохранение результата в файл
    if is_save:
        with open('../artifacts/books_data.txt', 'w', encoding='utf-8') as file:
            for book in all_books:
                file.write(f'{book}\n')

    return all_books