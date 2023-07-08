import json
import math
import os

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prepare_page(book_descriptions, counter, page_count):
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    for book in book_descriptions:
        book['address'] = f'../books/{book["title"]}.txt'
        pic_name = os.path.basename(book['img_address'])
        book['img_address'] = f'../media/images/{pic_name}'

    books_description_by_2 = list(chunked(book_descriptions, 2))

    rendered_page = template.render(
        books_description=books_description_by_2,
        page_count=page_count,
        page_number=counter,
        first_page=bool(counter == 1),
        last_page=bool(counter == page_count)
    )

    with open(f'{folder}/index{counter}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def prepare_html():
    with open('books_description.json', 'r') as file:
        books_description_content = json.load(file)

    page_count = math.ceil(len(books_description_content) / 10)

    books_description_by_10 = list(chunked(books_description_content, 10))
    for counter, book_descriptions in enumerate(books_description_by_10, 1):
        prepare_page(book_descriptions, counter, page_count)


def main():
    prepare_html()

    server = Server()
    server.watch('template.html', prepare_html)
    server.serve(root='.')


if __name__ == '__main__':
    main()
