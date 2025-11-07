import sys
import os

import pytest


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import get_book_data, scrape_books


def test_book_data_dict():
    """Проверяет, что данные о книге возвращаются в виде словаря"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert isinstance(result, dict), f'Полученные данные не в виде словаря, а типа {type(result)}'


def test_book_data_has_all_keys():
    """Проверяет, что словарь имеет нужные ключи"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    all_keys = ['name', 'price', 'rating', 'quantity_in_stock', 'description', 'extra_feature']
    out_keys = [key for key in all_keys if key not in result]
    assert len(out_keys) == 0, f'В словаре отсутствуют ключи: {out_keys}'


def test_book_data_name_correct():
    """Проверяет, что значение поля name корректно"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert result['name'] is not None, "Название книги не должно быть None"
    assert len(result['name']) > 0, "Название книги не должно быть пустым"
    assert "A Light in the Attic" in result['name'], (
        f"Должно быть название: 'A Light in the Attic', получено: {result['name']}"
    )


def test_book_data_price_correct():
    """Проверяет, что значение поля price корректно"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert result['price'] is not None, "Цена не должна быть None"


def test_get_book_data_rating_correct():
    """Проверяет, что значение поля rating корректно"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    ratings_correct = ['One', 'Two', 'Three', 'Four', 'Five', None]
    assert result['rating'] in ratings_correct, (
        f"Рейтинг должен быть одним из {ratings_correct}, получено: {result['rating']}"
    )


def test_book_data_extra_features_correct():
    """Проверяет, что дополнительные характеристики являются словарем и он не пустой"""

    result = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert isinstance(result['extra_feature'], dict), "Дополнительные характеристики должны быть в виде словаря"
    assert len(result['extra_feature']) > 0, "Дополнительные характеристики не должны быть пустыми"


def test_scrape_books_returns_list():
    """Проверяет, что данные обо всех книгах хранятся в списке"""

    result = scrape_books(is_save=False)
    assert isinstance(result, list), f"Ожидался list, получен {type(result)}"


def test_scrape_books_count_correct():
    """Проверяет, что в списке собранных книг нужное количество"""

    result = scrape_books(is_save=False)
    assert len(result) > 0, "Список книг не должен быть пустым"
    assert len(result) == 1000, f"Ожидалась 1000 книг, получено: {len(result)}"
