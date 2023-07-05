import json

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prepare_html():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open('books_description.json', 'r') as file:
        books_description = json.load(file)

    for book in books_description:
        book['address'] = f'books/{book["title"]}.txt'

    books_description = list(chunked(books_description, 2))


    rendered_page = template.render(books_description=books_description)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    prepare_html()

    server = Server()
    server.watch('template.html', prepare_html)
    server.serve(root='.')


if __name__ == '__main__':
    main()
