import requests as rq
from bs4 import BeautifulSoup

next_page = "https://pinboard.in/u:jcrites"
# next_page = "https://pinboard.in/u:ianchanning"
name = next_page[next_page.find('u:')+2:]
bookmarks = ''
# num_of_pages = 0

while len(bookmarks) <= 3631: # and num_of_pages != 1:
    html = BeautifulSoup(rq.get(next_page).content, "html.parser")
    next_page = 'https://pinboard.in' + html.find('a', {'class':"next_prev"})["href"]
    

    for i in html.find('div', {'id': "bookmarks"}).find_all('a', {"class": "bookmark_title"}):
        bookmarks += str(i["href"]) + '\n'

    for i in html.find_all('p'):
        if "No bookmarks saved." in i:
            next_page = "no"
            break
    # num_of_pages += 1
    print(len(bookmarks))
print(next_page)
with open("C:\\Users\\Ant\\Desktop\\" + name + ".txt", 'w') as file:
    file.write(bookmarks)

print("All bookmarks are downloaded.")
