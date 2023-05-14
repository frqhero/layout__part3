from os.path import join
import os

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename
import requests


def check_for_redirect(response):
    index_page = 'https://tululu.org/'
    if response.url == index_page:
        raise requests.exceptions.HTTPError('Книга не найдена')


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


def get_title_author(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    html_page_content = response.text
    soup = BeautifulSoup(html_page_content, 'lxml')
    post_title = soup.find('h1').text
    title, author = [word.strip() for word in post_title.split('::')]
    return title, author


def main():
    for counter in range(1, 11):
        try:
            page_url = f'https://tululu.org/b{counter}/'
            title, author = get_title_author(page_url)
            book_url = f'http://tululu.org/txt.php?id={counter}'
            download_txt(book_url, title)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
