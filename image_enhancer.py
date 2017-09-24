# Enhance image resolution by downloading from iqdb.org image search (and analogues)
import requests
import os
from bs4 import BeautifulSoup


def send_image(file):
    request = requests.post('http://iqdb.org/', files={'file': open(file, 'rb')})
    return request.text


def download(*urls):
    for i in urls:
        new_img_html = requests.get(i)
        soup_new = BeautifulSoup(new_img_html, 'html.parser')


def yandere(url):
    soup = BeautifulSoup(rq.get(url).content, 'html.parser')
    pic = soup.find('a', {'class': "highres-show"})['href'].split('.')

    with open('C:\\Users\\Ant\\Desktop\\' + pic[-2][3:].replace('%20', '_') + '.' + pic[-1], 'wb') as f:
        f.write(rq.get(pic).content)

# def get_google():
# def get_tineye():
# def get_zerochan():
def get_danbooru(url):
    soup = BeautifulSoup(rq.get(url).content, 'html.parser')
    pic = soup.find('a', {'class': "highres-show"})['href'].split('.')

    with open('C:\\Users\\Ant\\Desktop\\' + pic[-2][3:].replace('%20', '_') + '.' + pic[-1], 'wb') as f:
        f.write(rq.get(pic).content)


source_folder = 'C:\\Users\\Ant\\Desktop\\test\\'

for image_file in os.listdir(source_folder):
    print(image_file)
    html_doc = send_image(source_folder + image_file)

    soup = BeautifulSoup(html_doc, 'html.parser')
    global_div = soup.find('div', {'class': 'pages'})
    data = []
    links = []
    for nested_div in global_div.children:
        for tag in BeautifulSoup(str(nested_div), 'html.parser').find_all(['th', 'td', 'a']):
            if tag.name == 'a':
                links.append(tag['href'] if 'http:' in tag['href'] else 'http:' + tag['href'])
            else:
                data.append(tag.string)

    data = data[3:] # delete info about old picture
    print(links)

    with open(source_folder + image_file + '.html', 'wb') as html_doc_new:
        html_doc_new.write(soup.prettify().encode('utf-8'))
