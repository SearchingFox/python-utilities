import os
import requests as rq
DESKTOP = os.path.expanduser("~") + "\\Desktop\\"


def download_link(link, folder, ext=""):
    try:
        file_name = os.path.join(DESKTOP, folder, link.split('/')[-1])
        # lnk.headers['ETag'][1:-1] + ext
        while os.path.exists(file_name):
            print("Exists", file_name)
            return
            # file_name = os.path.join(DESKTOP, folder, "".join(random.choices(string.ascii_letters + string.digits, k=9)) + ext)

        with open(file_name, "wb") as file:
            file.write(rq.get(link).content)

        print("Saved", file_name)
    except Exception as e:
        print("Exception while saving:", e)


def download_list(links, folder, ext=""):
    if not os.path.exists(DESKTOP + folder):
        os.mkdir(DESKTOP + folder)

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
