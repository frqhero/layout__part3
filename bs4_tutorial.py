from bs4 import BeautifulSoup
import requests


def get_html_response_text():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def main():
    response_text = get_html_response_text()
    soup = BeautifulSoup(response_text, 'lxml')
    post_title = soup.find('main').find('article').find('h1').text
    post_image = soup.find('img', class_='attachment-post-image')['src']
    post_text = soup.find(class_='entry-content').text


if __name__ == '__main__':
    main()
