import os.path
import sqlite3
import sys


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
folder = 'C:\\Users\\Ant\\Desktop\\notes1\\'

connection = sqlite3.connect('omni-notes')
cursor = connection.cursor() 
notes = cursor.execute('SELECT title, content FROM notes WHERE trashed <> 1;')

c = 0
for note in notes:
    header = note[0]
    content = note[1]

    if header == '':
        header = 'New_Note_' + str(c)
        c += 1

    notepath = folder + header.translate(str.maketrans('', '', '<>:"/\|?*')) + '.txt'

    if os.path.exists(notepath):
        print('Note', header, 'already exists')
        content = '\n\n' + '-'*22 + '\n\n' + content

    with open(notepath, 'ab') as note_file:
        note_file.write(content.encode())

connection.close()
