import os
import re
import requests as rq
DESKTOP = os.path.join(os.path.expanduser('~'), "Desktop")


def download_link(link, folder, ext="", headers={}):
    file_path = os.path.join(DESKTOP, folder, link.split('/')[-1] + ext)
    try:
        c = 1
        while os.path.exists(file_path):
            print("Exists", file_path)
            file_path += str(c)
            c += 1

        with open(file_path.replace('\n', ''), 'wb') as file:
            file.write(rq.get(link, headers=headers).content)

        print("Saved", file_path)
    except Exception as e:
        print("Exception while saving:", e, file_path)


def download_list(links, folder, ext=""):
    if not os.path.exists(os.path.join(DESKTOP, folder)):
        os.mkdir(os.path.join(DESKTOP, folder))

    if type(links) is str:
        links = links.split('\n')

    for i in links:
        download_link(i, folder, ext)


def gen_nums(init_str, start, end, leadz=False):
    links = []
    for i in range(start, end+1):
        if leadz and i < 10:
            links.append(init_str.format("0" + str(i)))
        else:
            links.append(init_str.format(str(i)))

    return links

with open(os.path.join(DESKTOP, "links.txt"), 'r') as input_file:
    download_list(input_file.read().splitlines(), '29102')
