import os
import sys
import argparse as ap
import datetime as dt

# TODO: add stripe special symbols from names
# TODO: add stripe google bullshit from urls
# TODO: add more reliable arguments parsing
# TODO: add changing http to https if possible
# TODO: delete "m." and "?m=1"

def txt_to_html_file(file_path):
    import time

    timestamp = int(time.time())
    title = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks Menu</H1>

<DL><p>
    <DT><H3 ADD_DATE="{}" LAST_MODIFIED="{}">temp_bookmarks</H3>
    <DL><p>\n""".format(timestamp, timestamp)
    end = """\n    </DL><p>
</DL>"""

    with open(file_path, 'r', encoding='utf-8') as file:
        bookmarks = []
        for line in file:
            if line != '\n':
                bookmarks.append("""        <DT><A HREF="{url}" ADD_DATE="{}" LAST_MODIFIED="{}" ICON_URI="" ICON="">{url}</A>""".format(timestamp, timestamp, url=line[:-1]))
    with open(os.path.join(os.path.dirname(file_path), "temp_bookmarks.html"), 'w', encoding='utf-8') as new_file:
        new_file.write(title + '\n'.join(bookmarks) + end)


def save_links_only(file_path):
    with open(file_path, 'r', encoding='utf-8') as bookmarks_file:
        with open(os.path.join(os.path.dirname(file_path), "links.txt"), 'w', encoding='utf-8') as links_file:
            links = [line[line.find('"')+1:line.find('" A')] for line in bookmarks_file if '<A' in line]
            links_file.write('\n'.join(links))


# stripe favicon images from firefox bookmarks export file
def stripe_images(old_file_path):
    with open(old_file_path, 'r', encoding='utf-8') as old_file:
        with open(old_file_path[:-5] + "_noimgs.html", 'w', encoding='utf-8') as new_file:
            new_html = [line[:line.find("ICON_URI")-1] + line[line.find('">')+1:] for line in old_file]
            new_file.write('\n'.join(new_html))


def find_by_date(file_path, lower_bound, upper_bound):
    lower_bound_ts = int(dt.datetime.strptime(lower_bound, '%d.%m.%y').timestamp())
    upper_bound_ts = int(dt.datetime.strptime(upper_bound, '%d.%m.%y').timestamp())
    results = {}

    with open(file_path, 'r', encoding='utf-8') as bookmarks_file:
        for line in bookmarks_file:
            if '<A' in line:
                add_date = int(line[line.find('" A')+12:line.find('" L')])
                if lower_bound_ts <= add_date <= upper_bound_ts:
                    results[add_date] = line[line.find('"')+1:line.find('" A')]

    for i in sorted(results):
        print(dt.datetime.fromtimestamp(i).strftime('%d.%m.%y %H:%M'), results[i])


# find duplicate bookmarks in firefox export file
def find_duplicates(file_path):
    count = 0
    links = {}
    dupls = set()

    with open(file_path, 'r', encoding='utf-8') as bookmarks_file:
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
        with open(os.path.join(os.path.dirname(file_path), "dupls.txt"), 'w', encoding='utf-8') as dupls_file:
            dupls_file.write('\n'.join(output))
    else:
        print("No duplicates! Yay!")

if len(sys.argv) > 2:
    file = os.path.join(os.getcwd(), sys.argv[2])
else:
    htmls = [i for i in os.listdir() if i.endswith('.html') and i.startswith('bookmarks_firefox')]
    if len(htmls) == 1:
        file = os.path.join(os.getcwd(), htmls[0])
    else:
        print("Error: Specify file.")
        exit(1)

if   sys.argv[1] == "-s":
    stripe_images(file)
elif sys.argv[1] == "-d":
    find_duplicates(file)
elif sys.argv[1] == "-l":
    save_links_only(file)
elif sys.argv[1] == "-f":
    find_by_date(file, sys.argv[3], sys.argv[4])
