import os
import sys

# stripe images from firefox bookmarks export file
def stripe_images(old_file_path):
    with open(old_file_path, 'r', encoding='UTF-8') as old_file:
        with open(old_file_path[:-5] + "_noimgs.html", 'w', encoding='UTF-8') as new_file:
            html = ""
            for i in old_file.readlines():
                html += i[:i.find("ICON_URI")-1] + i[i.find('">')+1:] + '\n'
            new_file.write(html)


# find duplicate bookmarks in firefox export file
def find_duplicates(file_path):
    links = {}
    dupls = []
    count = 0

    with open(file_path, 'r', encoding='utf-8') as bookmarks_file:
        for line in bookmarks_file.readlines():
            if "<H3" in line:
                folder = line[line.find("\">")+2:line.find("</")]
            elif '<A' in line:
                count += 1
                addr = '/'.join(line[line.find('"')+1:line.find('" A')].split('/')[2:]) if line.startswith("http") else line[line.find('"')+1:line.find('" A')]

                if addr not in links:
                    links[addr] = []
                elif addr not in dupls:
                    dupls.append(addr)

                links[addr].append(folder)

    print("all links:", count)
    print("duplicates:", len(dupls))
    # for i in sorted(dupls):
    #     print(i, links[i])
    
    with open("dupls.txt", 'w') as dupls_file:
        dupls_file.write('\n'.join(sorted(dupls)))


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
