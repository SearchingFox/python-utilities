import os
import sys
import sqlite3


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

if sys.platform.startswith("win32"):
    inp_file   = os.path.join(os.path.expanduser('~'), "Desktop", "omni-notes")
    out_folder = os.path.join(os.path.expanduser('~'), "Desktop", "notes1")
elif sys.platform.startswith("linux"):
    inp_file   = "/storage/emulated/0/documents/omni-notes"
    out_folder = "/storage/emulated/0/documents/notes1/"
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

connection = sqlite3.connect(inp_file)
notes = connection.cursor().execute("SELECT title, content, category_id FROM notes WHERE trashed <> 1;")

new_notes_num, existed_notes_num = 1, 1
for title, content, category_id in notes:
    try:
        if not title:
            title = "New_Note_" + str(new_notes_num)
            new_notes_num += 1

        if category_id:
            c = connection.cursor()
            c.execute("SELECT name FROM categories WHERE category_id = ?", (category_id,))
            out_path = os.path.join(out_folder, c.fetchone()[0])
            if not os.path.exists(out_path):
                os.mkdir(out_path)
        else:
            out_path = out_folder

        note_path = os.path.join(out_path, title.translate(str.maketrans("<>:\"/\|?*\r\n", "_"*11)) + ".txt")

        while os.path.exists(note_path):
            print("Note \"" + title + "\" already exists.")
            note_path = note_path[:-4] + '_' + str(existed_notes_num) + ".txt"
            existed_notes_num += 1

        with open(note_path, 'a', encoding='utf-8') as note_file:
            note_file.write(content)
    except Exception as e:
        print("Error:", e)

connection.close()
