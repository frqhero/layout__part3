import argparse
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
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    for book in book_descriptions:
        book['address'] = f'../media/books/{book["title"]}.txt'
        pic_name = os.path.basename(book['img_address'])
        book['img_address'] = f'../media/images/{pic_name}'

    books_in_row = 2
    books_description_row_chunked = list(
        chunked(book_descriptions, books_in_row)
    )

    rendered_page = template.render(
        books_description=books_description_row_chunked,
        page_count=page_count,
        page_number=counter,
        first_page=bool(counter == 1),
        last_page=bool(counter == page_count),
    )

    with open(f'{folder}/index{counter}.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def prepare_html():
    parser = create_parser()
    args = parser.parse_args()
    with open(args.description_path, 'r') as file:
        books_description_content = json.load(file)

    books_on_page = 10
    page_count = math.ceil(len(books_description_content) / books_on_page)

    books_description_page_chunked = list(
        chunked(books_description_content, books_on_page)
    )
    for counter, book_descriptions in enumerate(
        books_description_page_chunked, 1
    ):
        prepare_page(book_descriptions, counter, page_count)


def is_file(filename):
    if os.path.isfile(filename):
        return filename
    else:
        raise argparse.ArgumentTypeError(f'{filename} is not a valid filename')


def create_parser():
    parser = argparse.ArgumentParser(
        description='This script is used for '
        'create and serve web pages with parsed books'
    )
    parser.add_argument(
        '--description_path',
        default='books_description.json',
        type=is_file,
        help='Set books_description file',
    )
    return parser


def main():
    prepare_html()

    server = Server()
    server.watch('template.html', prepare_html)
    server.serve(root='.')


if __name__ == '__main__':
    main()
