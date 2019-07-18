import os
import sys
import os.path as pt
import argparse as ap
import datetime as dt

# TODO: add stripe special symbols from names
# TODO: add stripe google bullshit from urls
# TODO: add more reliable arguments parsing
# TODO: add changing http to https if possible
# TODO: delete "m." and "?m=1"

def org_to_html_file(bookmarks_file_path, file_path):
    creation_time = dt.datetime.now().strftime("%y%m%d_%H%M")
    blob_head = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks Menu</H1>

<DL><p>
    <DT><H3>smartphone_{}</H3>\n    <DL><p>\n""".format(creation_time)
    blob_last = "\n    </DL><p>\n</DL>"

    with open(file_path, encoding='utf-8') as file:
        new_links = file.read().split('\n\n')

    bookmarks = []
    added_links = []
    links = get_links_only(bookmarks_file_path)
    
    for line in new_links:
        if line:
            title, link = line.split('\n')

            if link not in links and link not in added_links:
                tags = ''
                t = title.split(' ')[-1]
                if t[0] == t[-1] == ':':
                    tags = ' TAGS="{}"'.format(t[1:-1])
                    title = title.rsplit(' ', 1)[0]

                bookmarks.append('        <DT><A HREF="{}"{}>{}</A>'.format(link, tags, title[2:]))
                added_links.append(link)

    new_file_name = pt.join(pt.dirname(file_path), "smartphone_{}.html".format(creation_time))
    with open(new_file_name, 'w', encoding='utf8') as new_file:
        new_file.write(blob_head + '\n'.join(bookmarks) + blob_last)


def get_links_only(file_path):
    with open(file_path, encoding='utf8') as bookmarks_file:
        return [line[line.find('"')+1:line.find('" A')] for line in bookmarks_file if '<A' in line]


def strip_favicon_images(old_file_path):
    with open(old_file_path, encoding='utf8') as old_file:
        with open(old_file_path[:-5] + "_noicons.html", 'w', encoding='utf8') as new_file:
            new_html = [line[:line.find("ICON_URI")-1] + line[line.find('">')+1:] if line.find("ICON_URI") > 0 else line for line in old_file]
            new_file.write(''.join(new_html))


def find_by_date(file_path, lower_bound, upper_bound):
    lower_bound_ts = int(dt.datetime.strptime(lower_bound, '%d.%m.%y').timestamp())
    upper_bound_ts = int(dt.datetime.strptime(upper_bound, '%d.%m.%y').timestamp())
    results = {}

    with open(file_path, encoding='utf8') as bookmarks_file:
        for line in bookmarks_file:
            if '<A' in line:
                add_date = int(line[line.find('" A')+12:line.find('" L')])
                if lower_bound_ts <= add_date <= upper_bound_ts:
                    results[add_date] = line[line.find('"')+1:line.find('" A')]

    for i in sorted(results):
        print(dt.datetime.fromtimestamp(i).strftime('%d.%m.%y %H:%M'), results[i])


def find_duplicates(file_path):
    count = 0
    links = {}
    dupls = set()

    with open(file_path, encoding='utf8') as bookmarks_file:
        for line in bookmarks_file:
            if '<H3' in line:
                folder = line[line.find('">')+2:line.find('</')]
            elif '<A' in line:
                count += 1
                url  = line[line.find('"')+1:line.find('" A')]
                link = url.split('/', 2)[2] if url.startswith('http') else url

                if link not in links:
                    links[link] = []
                else:
                    dupls.add(link)

                links[link].append(folder)

    print("all links:", count)

    if dupls:
        print("duplicates:", len(dupls))
        output = [i + '\t' + ' '.join(links[i]) for i in sorted(dupls)]
        with open(pt.join(pt.dirname(file_path), "dupls.txt"), 'w', encoding='utf-8') as dupls_file:
            dupls_file.write('\n'.join(output))
    else:
        print("No duplicates! Yay!")


if   sys.argv[1] == "-s":
    strip_favicon_images(sys.argv[2])
elif sys.argv[1] == "-d":
    find_duplicates(sys.argv[2])
elif sys.argv[1] == "-l":
    with open(pt.join(pt.dirname(sys.argv[2]), "firefox_links.txt"), 'w', encoding='utf-8') as links_file:
        links_file.write('\n'.join(get_links_only(sys.argv[2])))
    print("Saved firefox_links.txt")
elif sys.argv[1] == "-f":
    find_by_date(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == "-c":
    org_to_html_file(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "-v":
    print("0.4.181021")
else: # if sys.argv[1] == "-h":
    print("""
-s    strip favicons
-d    list duplicates
-l    list only links
-f    find by date
-c    convert Orgzly export file to html
-h    show this help
-v    show version""")
