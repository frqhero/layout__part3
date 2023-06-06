from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def parse_books_by_page_link(netloc, link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', {'id': 'content'})
    links = [
        urljoin(netloc, x.find('a')['href'])
        for x in content.find_all('table')
    ]
    return links


def main():
    netloc = 'https://tululu.org/'
    for counter in range(1, 11):
        sci_fi_page_address = urljoin(netloc, f'l55/{counter}')
        links = parse_books_by_page_link(netloc, sci_fi_page_address)
        print("\n".join(links))


if __name__ == '__main__':
    main()
