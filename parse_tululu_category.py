from urllib.parse import urljoin, urlsplit
import argparse
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
    table_selector = 'div#content table'
    tables = soup.select(table_selector)
    anchor_selector = 'a'
    links = [
        urljoin(netloc, table.select_one(anchor_selector)['href'].rstrip('/'))
        for table in tables
    ]
    return links


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
        default=701,
        type=int,
        help='Set second ID the script will work with',
    )
    args = parser.parse_args()
    netloc = 'https://tululu.org/'
    links = []
    for counter in range(args.start_id, args.end_id + 1):
        sci_fi_page_address = urljoin(netloc, f'l55/{counter}')
        links += parse_books_by_page_link(netloc, sci_fi_page_address)

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
