from os.path import join
from urllib.parse import urljoin, urlsplit, unquote
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


def download_image(img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    os.makedirs('images', exist_ok=True)
    filename = urlsplit(unquote(img_url)).path.split('/')[-1]
    with open(f'images/{filename}', 'wb') as file:
        file.write(response.content)


def parse_comments(soup):
    comments = [
        x.find(class_='black').text
        for x in soup.find_all(class_='texts')
    ]
    [print(comment) for comment in comments]
    print()


def parse_genres(soup):
    genres = [
        x.text
        for x in soup.find('span', class_='d_book').find_all('a')
    ]
    print(genres)
    print()


def download_txt(url, filename, folder='books/'):
    folder = sanitize_filepath(folder)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(filename)
    file_path = join(folder, f'{filename}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    for counter in range(1, 11):
        try:
            base = 'https://tululu.org/'
            book_url = urljoin(base, f'b{counter}')
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response.url, base)

            soup = BeautifulSoup(response.text, 'lxml')
            title, author = parse_title_author(soup)
            print(title)
            # img_path = parse_book_image_link(soup)
            # parse_comments(soup)
            parse_genres(soup)

            # img_url = urljoin(base, img_path)
            # download_image(img_url)

            # book_url = urljoin(base, f'txt.php?id={counter}')
            # download_txt(book_url, title)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
