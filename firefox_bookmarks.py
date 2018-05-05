import os
import sys

# TODO: add stripe special symbols from names

def save_links_only(file_path):
    with open(file_path, 'r', encoding="utf-8") as bookmarks_file:
        s = ""
        for line in bookmarks_file:
            if '<A' in line:
                s += line[line.find('"')+1:line.find('" A')] + '\n'
        with open("\\".join(file_path.split('\\')[:-1])+"\\links.txt", 'w', encoding="utf-8") as links_file:
            links_file.write(s)


# stripe images from firefox bookmarks export file
def stripe_images(old_file_path):
    with open(old_file_path, 'r', encoding='UTF-8') as old_file:
        with open(old_file_path[:-5] + "_noimgs.html", 'w', encoding='UTF-8') as new_file:
            new_html = ""
            for line in old_file:
                new_html += line[:line.find("ICON_URI")-1] + line[line.find('">')+1:] + '\n'
            new_file.write(new_html)


# find duplicate bookmarks in firefox export file
def find_duplicates(file_path):
    links = {}
    dupls = set()
    count = 0

    with open(file_path, 'r', encoding='utf-8') as bookmarks_file:
        for line in bookmarks_file:
            if "<H3" in line:
                folder = line[line.find("\">")+2:line.find("</")]
            elif '<A' in line:
                count += 1
                url = line[line.find('"')+1:line.find('" A')]
                link = url.split('/', 2)[2] if url.startswith("http") else url

                if link not in links:
                    links[link] = []
                else:
                    dupls.add(link)

                links[link].append(folder)

    print("all links:", count)
    print("duplicates:", len(dupls))

    output = ""
    for i in sorted(dupls):
        output += i + "    " + ' '.join(links[i]) + '\n'
    with open("dupls.txt", 'w', encoding='utf-8') as dupls_file:
        dupls_file.write(output)

if len(sys.argv) > 1:
    file = os.path.join(os.getcwd(), sys.argv[2])
else:
    htmls = [i for i in os.listdir() if i.endswith(".html") and i.startswith("bookmarks_firefox")]
    if len(htmls) == 1:
        file = os.path.join(os.getcwd(), htmls[0])
    else:
        print("Error: Specify file.")
        exit(1)

if sys.argv[1] == "-s":
    stripe_images(file)
elif sys.argv[1] == "-d":
    find_duplicates(file)
elif sys.argv[1] == "-l":
    save_links_only(file)
