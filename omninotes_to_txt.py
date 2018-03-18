import os
import sys
import sqlite3


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
in_folder = 'C:\\Users\\Ant\\Desktop\\2017.08.24-17.34\\'
out_folder = 'C:\\Users\\Ant\\Desktop\\notes1\\'
if not os.path.exists(out_folder):
    os.mkdir(out_folder)

connection = sqlite3.connect(in_folder + 'omni-notes')
cursor = connection.cursor() 
notes = cursor.execute('SELECT title, content FROM notes WHERE trashed <> 1;')

c = 0
for note in notes:
    try:
        header = note[0]
        content = note[1]

        if header == '':
            header = 'New_Note_' + str(c)
            c += 1

        notepath = out_folder + header.translate(str.maketrans('', '', '<>:"/\|?*\r\n')) + '.txt'

        if os.path.exists(notepath):
            print('Note "' + header + '" already exists')
            content = '\n\n' + '-'*22 + '\n\n' + content

        with open(notepath, 'ab') as note_file:
            note_file.write(content.encode())
    except Exception as e:
        print('Error:', e)

connection.close()
