import re
LIMIT_COMMON_WORDS = 4500

file_path = "D:\\Hannibal.S01.Season.1.1080p.Web-DL.ReEnc-DeeJayAhmed\\Hannibal.S01E10.Buffet.Froid.1080p.Web-DL.ReEnc-DeeJayAhmed.srt"
ext = file_path.split('.')[-1]
with open("C:\\Users\\Ant\\Documents\\Python\\count_1w.txt", 'r') as words_file:
    lim = 1
    common_words = []
    for i in words_file:
        if lim <= LIMIT_COMMON_WORDS:
            lim += 1
            common_words.append(i.split()[0])


def del_com_words(old_line):
    new_line = ""
    for word in re.sub("[,.?!;:></'\t\n\-]+", ' ', old_line).lower().split():
        if word and word not in common_words:
            new_line += word + ' '

    return new_line[:-1]


with open(file_path, 'r', encoding="utf-8") as file:
    if ext == "srt":
        new_file_content = ""
        position = 1
        for i in ''.join(file.readlines()).split("\n\n"):
            time, content = i.split('\n')[1], i.split('\n')[2:]

            cont1 = []
            for p in content:
                p1 = del_com_words(p)
                if p1:
                    cont1.append(p1)
            if cont1:
                new_file_content += str(position) + '\n' + '\n'.join(time + cont1) + "\n\n"
                position += 1
    elif ext == "ass":
        paragraphs = [i.split(",,")[-1][:-1].split('\n') for i in file if i.startswith("Dialogue:")]
        for p in paragraphs:
            print(p, '^^^', del_com_words(p))

with open(file_path[:-4]+'new.'+ext, 'w', encoding="utf-8") as new_file:
    new_filee.write(new_file_content)
