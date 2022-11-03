#'C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt', encoding='utf8'
#Search for ***** LOG FILE OPENING *****
import os


fh = open('C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/b.txt', encoding='utf8')
fh.seek(0, os.SEEK_END)
size = fh.tell()
print(size)
fh.seek(size-200)
print(fh.read())
