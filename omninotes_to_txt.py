import os
import sys
import sqlite3


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
in_folder   = "C:\\Users\\Ant\\Desktop\\"
out_folder  = "C:\\Users\\Ant\\Desktop\\notes1\\"
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

connection = sqlite3.connect(in_folder + "omni-notes")
cursor = connection.cursor()
notes = cursor.execute("SELECT title, content FROM notes WHERE trashed <> 1;")

i, j = 0, 0
for header, content in notes:
    try:
        if not header:
            header = "New_Note_" + str(i)
            i += 1

        note_path = out_folder + header.translate(str.maketrans("<>:\"/\|?*\r\n", "___________")) + ".txt"

        if os.path.exists(note_path):
            print("Note \"" + header + "\" already exists")
            note_path = note_path[:-4] + '_' + str(j) + ".txt"
            j += 1

        with open(note_path, 'a', encoding='utf-8') as note_file:
            note_file.write(content)
    except Exception as e:
        print("Error:", e)

connection.close()
