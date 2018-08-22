import os
import sys
from bs4 import BeautifulSoup as BS
DESKTOP = "C:\\Users\\Ant\\Desktop"

out_folder = os.path.join(DESKTOP, sys.argv[1].split('.')[0])
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

with open(os.path.join(DESKTOP, sys.argv[1]), 'r', encoding='utf8') as inp:
    notes = BS(inp, 'html.parser').find_all('note')

    for n in notes:
        title = n.title.text.translate(str.maketrans("<>:\"/\\|?*\r\n", '_'*11)).replace('&apos', "'")
        note_path = os.path.join(out_folder, title + '.txt')

        existed_notes_num = 1
        while os.path.exists(note_path):
            print("Note \"" + title + "\" already exists.")
            note_path = note_path[:-4] + '_' + str(existed_notes_num) + ".txt"
            existed_notes_num += 1

        print(note_path)

        with open(note_path, 'w', encoding='utf8') as out:
            out.write(BS(n.content.text, 'html.parser').get_text(strip=True, separator='\n').replace('&apos', "'"))
