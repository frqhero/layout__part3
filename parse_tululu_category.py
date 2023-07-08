from pathlib import Path
from urllib.parse import urljoin, urlsplit
import argparse
import json
import os
import time

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
    check_for_redirect(response.url)
    soup = BeautifulSoup(response.text, 'lxml')
    table_selector = 'div#content table'
    tables = soup.select(table_selector)
    anchor_selector = 'a'
    links = [
        urljoin(netloc, table.select_one(anchor_selector)['href'].rstrip('/'))
        for table in tables
    ]
    return links


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f'readable_dir:{path} is not a valid path'
        )


def create_parser():
    parser = argparse.ArgumentParser(
        description='This script is used for '
        'downloading books and related materials'
    )
    parser.add_argument(
        '--start_page',
        default=1,
        type=int,
        help='Set first page the script will work with',
    )
    parser.add_argument(
        '--end_page',
        default=701,
        type=int,
        help='Set end page the script will work with',
    )
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument(
        '--dest_folder',
        default=base_dir,
        type=dir_path,
        help='Set destination folder path',
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Should images be downloaded',
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Should textbooks be downloaded',
    )
    parser.add_argument(
        '--json_path',
        default=base_dir,
        type=dir_path,
        help='Set json description path',
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    netloc = 'https://tululu.org/'
    links = []

    for counter in range(args.start_page, args.end_page + 1):
        try:
            sci_fi_page_address = urljoin(netloc, f'l55/{counter}')
            links += parse_books_by_page_link(netloc, sci_fi_page_address)
        except requests.exceptions.HTTPError as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(10)

    book_descriptions = []

    for book_url in links:
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response.url)

            parsed_book_page = parse_book_page(response.text)
            book_id = urlsplit(book_url).path.replace('/', '').replace('b', '')

            books_folder = Path(args.dest_folder).joinpath('media/books')
            if not args.skip_txt:
                download_txt(
                    book_url,
                    book_id,
                    parsed_book_page['title'],
                    str(books_folder),
                )
            images_folder = Path(args.dest_folder).joinpath('media/images')
            if not args.skip_imgs:
                download_image(
                    book_url,
                    parsed_book_page['img_address'],
                    str(images_folder),
                )
            book_descriptions.append(parsed_book_page)
        except requests.exceptions.HTTPError as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(10)

    json_path = (
        args.json_path
        if args.dest_folder != args.json_path
        else args.dest_folder
    )
    json_path = Path(json_path).joinpath('books_description.json')
    with open(str(json_path), 'w', encoding='utf8') as json_file:
        json.dump(book_descriptions, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
