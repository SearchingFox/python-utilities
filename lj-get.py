import requests as rq
from bs4 import BeautifulSoup
import re

posts = ['1']
page = 0
c = 1
while posts != []:
    # next_page = 'http://deni-ok.livejournal.com/?skip=' + str(page)
    next_page = 'http://argonov.livejournal.com/?skip=' + str(page)
    page += 10
    html = BeautifulSoup(rq.get(next_page).content, 'html.parser')
    
    posts = html.find_all('div', {'class': re.compile('.*entry.*')})
    
    name = 'page_' + str(c) + '.txt'
    c += 1
    
    with open('C:\\Users\\Ant\\Desktop\\LiveJournal2\\' + name, 'ab') as file:
        for post in posts:
            file.write(str(post.text).encode())
            delimiter = '\n\n' + '-'*22 + '\n\n'
            file.write(delimiter.encode())

