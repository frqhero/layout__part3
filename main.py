import requests


def download_book_by_id(id):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    file_name = dict(response.headers)['Content-Disposition']
    quote = file_name.find('"')
    file_name = file_name[quote + 1:-1]
    with open(file_name, 'wb') as file:
        file.write(response.content)


def main():
    a


if __name__ == '__main__':
    main()
