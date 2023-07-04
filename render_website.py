import json

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prepare_html():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open('books_description.json', 'r') as file:
        books_description = json.load(file)

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
