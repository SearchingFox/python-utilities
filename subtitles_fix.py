import re


file_path = "D:\\Violet Evergarden [BDRip 1080p x264 FLAC]\ENG Subs\\[Beatrice-Raws] Violet Evergarden 02 [BDRip 1920x1080 x264 FLAC].ENG.[Vivid-Asenshi].ass"
ext = file_path.split('.')[-1]
with open("C:\\Users\\Ant\\Desktop\\count_1w.txt", 'r') as words_file:
    common_words = [i.split()[0] for i in words_file][:4500]


def del_com_words(old_par):
    new_par = []
    for line in old_par:
        new_line = ""
        for word in re.sub("[\-,.?!></'\t\n1-9]+", ' ', line).lower().split():
            if word not in common_words:
                new_line += word + ' '
        if new_line:
            new_par.append(new_line[:-1])

    return new_par


with open(file_path, 'r', encoding="utf-8") as file:
    if ext == "srt":
        paragraphs = [i.split('\n')[2:] for i in ''.join(file.readlines()).split("\n\n")]
        for p in paragraphs:
            print(p, '^^^', del_com_words(p))
    elif ext == "ass":
        paragraphs = [i.split(",,")[-1][:-1].split('\n') for i in file if i.startswith("Dialogue:")]
        for p in paragraphs:
            print(p, '^^^', del_com_words(p))
