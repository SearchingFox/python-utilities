import os
import sys
import sqlite3


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

if sys.platform.startswith("win32"):
    inp_file   = os.path.expanduser('~') + "Desktop\\omni-notes"
    out_folder = os.path.expanduser('~') + "Desktop\\notes1\\"
elif sys.platform.startswith("linux"):
    inp_file   = "/storage/emulated/0/documents/omni-notes"
    out_folder = "/storage/emulated/0/documents/notes1/"
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

connection = sqlite3.connect(inp_file)
cursor = connection.cursor()
notes = cursor.execute("SELECT title, content FROM notes WHERE trashed <> 1;")

i, j = 1, 1
for title, content in notes:
    try:
        if not title:
            title = "New_Note_" + str(i)
            i += 1

        note_path = os.path.join(out_folder, title.translate(str.maketrans("<>:\"/\|?*\r\n", "_"*11)) + ".txt")

        if os.path.exists(note_path):
            print("Note \"" + title + "\" already exists.")
            note_path = note_path[:-4] + '_' + str(j) + ".txt"
            j += 1

        with open(note_path, 'a', encoding='utf-8') as note_file:
            note_file.write(content)
    except Exception as e:
        print("Error:", e)

connection.close()
