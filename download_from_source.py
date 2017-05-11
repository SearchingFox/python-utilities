# Downloading pics from html code of web-page
import re
import requests
from bs4 import BeautifulSoup

with open("C:\\Users\\Ant\\Desktop\\kod.txt") as html_file:
    line = html_file.readline()
    j = 0
    while line:
        if ".jpg" or ".jpeg" in line:
                urls = re.findall('(?:ftp[s]?|http[s]?://)?(?:www.)?(?:[\w$-@.&+!*(),?\[\];#]|(?:%[0-9a-zA-Z]{2,63}))+',
                                  line)
                print(urls)
                for url in urls:
                    pic = requests.get(url)
                    j += 1
                    file_name = "C:\\Users\\Ant\\Desktop\\download\\" + str(j) + ".jpeg"
                    print("Saving" + file_name + "...")
                    with open(file_name, "wb") as file:
                        file.write(pic.content)
                urls = ""
        line = html_file.readline()