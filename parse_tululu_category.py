from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def main():
    netloc = 'https://tululu.org/'
    sci_fi_page_address = urljoin(netloc, 'l55')
    response = requests.get(sci_fi_page_address)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', {'id': 'content'})
    links = [
        urljoin(netloc, x.find('a')['href'])
        for x in content.find_all('table')
    ]
    print("\n".join(links))


if __name__ == '__main__':
    main()
