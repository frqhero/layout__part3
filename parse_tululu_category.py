from urllib.parse import urljoin, urlsplit
import json

from bs4 import BeautifulSoup
import requests

from main import (
    check_for_redirect,
    parse_book_page,
    download_image,
    download_txt,
)


def parse_books_by_page_link(netloc, link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', {'id': 'content'})
    links = [
        urljoin(netloc, table.find('a')['href']).rstrip('/')
        for table in content.find_all('table')
    ]
    return links


def main():
    netloc = 'https://tululu.org/'
    links = []
    for counter in range(1, 5):
        sci_fi_page_address = urljoin(netloc, f'l55/{counter}')
        links += parse_books_by_page_link(netloc, sci_fi_page_address)

    # print("\n".join(links))
    books_description = []
    for book_url in links:
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response.url)

            parsed_book_page = parse_book_page(response.text)
            book_id = urlsplit(book_url).path.replace('/', '').replace('b', '')

            download_txt(book_url, book_id, parsed_book_page['title'])
            download_image(book_url, parsed_book_page['img_address'])
            books_description.append(parsed_book_page)
        except requests.exceptions.HTTPError as e:
            print(e)
    with open('book_description.json', 'w', encoding='utf8') as json_file:
        json.dump(books_description, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
