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
    dups  = []
    with open(file_path, 'r', encoding='utf-8') as file:
        all_ = file.readlines()
        links0 = [i[i.find('"')+1:i.find('" A')] for i in all_ if '<A' in i and "<H3" not in i]

        for line in all_:
            if "<H3" in line:
                folder = line[line.find("\">")+2:line.find("</")]
            elif '<A' in line:
                addr = line[line.find('"')+1:line.find('" A')]
                if addr not in links.keys():
                    links[addr] = []
                elif addr not in dups:
                    dups.append(addr)

                links[addr].append(folder)
    
    # dups0 = []
    # for pos_1, lnk_1 in enumerate(links0):
    #     for pos_2, lnk_2 in enumerate(links0):
    #         if pos_1 != pos_2 and lnk_1 == lnk_2 and lnk_1 not in dups0:
    #             dups0.append(lnk_1)

    # if dups0 != dups:
    #     print("ERROR!!!")
    #     if len(dups0) > len(dups):
    #         for i in dups0:
    #             if i not in dups:
    #                 print(i)
    #     else:
    #         for i in dups:
    #             if i not in dups0:
    #                 print(i)
        print("all links:", len(links0))
        
        print("duplicates:", len(dups))
        dups2 = []
        for i in links.values():
            if len(i) > 1:
                dups2.append(i)
        print("duplicates2:", len(dups2))
        print(len(links.keys()))
        for i in links0:
            if i not in links.keys():
                print(i)
    # for i in sorted(dups):
    #     print(i, links[i])

    # with open("dup.txt", 'w') as file:
    #     file.write('\n'.join(dup))


if len(sys.argv) > 1:
    file = os.path.join(os.getcwd(), sys.argv[2])
else:
    htmls = [i for i in os.listdir() if i.endswith(".html") and "firefox" in i]
    if len(htmls) == 1:
        file = os.path.join(os.getcwd(), htmls[0])
    else:
        print("Error: Specify file.")
        exit(1)

if sys.argv[1] == "-s":
    stripe_images(file)
elif sys.argv[1] == "-d":
    find_duplicates(file)
