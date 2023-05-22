from os.path import join
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import os
import time

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename
import requests


def check_for_redirect(response_url):
    if response_url == urljoin(response_url, '/'):
        raise requests.exceptions.HTTPError('Книга не найдена')


def parse_title_author(soup):
    post_title = soup.find('h1').text
    title, author = [word.strip() for word in post_title.split('::')]
    return title, author


def parse_book_image_link(soup):
    return soup.find(class_='bookimage').find('a').find('img').attrs['src']


def download_image(book_url, img_address):
    img_url = urljoin(book_url, img_address)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response.url)
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
    img_address = parse_book_image_link(soup)
    comments = parse_comments(soup)
    genres = parse_genres(soup)
    return {
        'title': title,
        'author': author,
        'img_address': img_address,
        'comments': comments,
        'genres': genres,
    }


def download_txt(book_url, counter, filename, folder='books/'):
    book_file_url = urljoin(book_url, 'txt.php')
    params = {'id': counter}
    response = requests.get(book_file_url, params=params)
    response.raise_for_status()
    check_for_redirect(response.url)

    folder = sanitize_filepath(folder)
    os.makedirs(folder, exist_ok=True)
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
    netloc = 'https://tululu.org/gg'
    for counter in range(args.start_id, args.end_id + 1):
        try:
            book_url = urljoin(netloc, f'bh{counter}')
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response.url)

            parsed_book_page = parse_book_page(response.text)

            download_image(book_url, parsed_book_page['img_address'])

            download_txt(book_url, counter, parsed_book_page['title'])
        except requests.exceptions.HTTPError as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    main()
