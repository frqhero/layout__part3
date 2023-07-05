import json
import os

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prepare_html(books_description, counter):
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    for book in books_description:
        book['address'] = f'../books/{book["title"]}.txt'

    books_description_by_2 = list(chunked(books_description, 2))

    rendered_page = template.render(books_description=books_description_by_2)

    with open(f'{folder}/index{counter}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    with open('books_description.json', 'r') as file:
        books_description_content = json.load(file)

    books_description_by_10 = list(chunked(books_description_content, 10))
    for counter, books_description in enumerate(books_description_by_10, 1):
        prepare_html(books_description, counter)

    server = Server()
    server.watch('template.html', prepare_html)
    server.serve(root='.')


if __name__ == '__main__':
    main()
