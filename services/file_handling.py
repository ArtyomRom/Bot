import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    dict_page_book = {
        1: ''
    }
    punctuation_marks = ['.', ',', '!', ':', ';', '?']
    letters_ru = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                  'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    page = 0
    for letter in text[start:]:
        if letter in punctuation_marks:
            try:
                if page + 1 <= PAGE_SIZE and text[start + page + 1] not in punctuation_marks and text[
                    start + page + 1].lower() not in letters_ru:
                    dict_page_book[1] = text[start: start + page + 1]
                    page += 1
                else:
                    page += 1
                    continue
            except IndexError:
                dict_page_book[1] = text[start:]

        else:
            page += 1
            continue
    return dict_page_book[1], len(dict_page_book[1])


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        book_str = f.read()

    start_symbol = 0
    page = 1

    while True:
        string_book, string_length = _get_part_text(book_str[start_symbol: start_symbol + PAGE_SIZE], 0, PAGE_SIZE)
        if len(string_book) == 0:
            break
        book[page] = string_book.lstrip()
        start_symbol += string_length
        page += 1


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
# prepare_book('boo')

