from os.path import join
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import os

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename
import requests


def check_for_redirect(response_url, base):
    if response_url == base:
        raise requests.exceptions.HTTPError('Книга не найдена')


def parse_title_author(soup):
    post_title = soup.find('h1').text
    title, author = [word.strip() for word in post_title.split('::')]
    return title, author


def parse_book_image_link(soup):
    return soup.find(class_='bookimage').find('a').find('img').attrs['src']


def download_image(base, img_path):
    img_url = urljoin(base, img_path)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response, base)
    os.makedirs('images', exist_ok=True)
    filename = urlsplit(unquote(img_url)).path.split('/')[-1]
    with open(f'images/{filename}', 'wb') as file:
        file.write(response.content)


def parse_comments(soup):
    comments = [
        x.find(class_='black').text for x in soup.find_all(class_='texts')
    ]
    return comments


def parse_genres(soup):
    genres = [x.text for x in soup.find('span', class_='d_book').find_all('a')]
    return genres


def parse_book_page(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    title, author = parse_title_author(soup)
    img_path = parse_book_image_link(soup)
    comments = parse_comments(soup)
    genres = parse_genres(soup)
    return {
        'title': title,
        'author': author,
        'img_path': img_path,
        'comments': comments,
        'genres': genres,
    }


def download_txt(base, url, filename, folder='books/'):
    folder = sanitize_filepath(folder)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response.url, base)
    filename = sanitize_filename(filename)
    file_path = join(folder, f'{filename}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(
        description='This script is used for '
        'downloading books and related materials'
    )
    parser.add_argument(
        '--start_id',
        default=1,
        type=int,
        help='Set first ID the script will work with',
    )
    parser.add_argument(
        '--end_id',
        default=10,
        type=int,
        help='Set second ID the script will work with',
    )
    args = parser.parse_args()
    for counter in range(args.start_id, args.end_id + 1):
        try:
            base = 'https://tululu.org/'
            book_url = urljoin(base, f'b{counter}')
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response.url, base)

            parsed_book_page = parse_book_page(response.text)

            download_image(base, parsed_book_page['img_path'])

            book_url = urljoin(base, f'txt.php?id={counter}')
            download_txt(base, book_url, parsed_book_page['title'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
