# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /0/python/lib/unicodescript/unicodescript/__init__.py
# Compiled at: 2008-12-22 15:45:16
import os, unicodedata, bisect
scriptfile = os.path.dirname(os.path.abspath(__file__)) + '/scripts.txt'
indexes = []
scripts = []

def script(char):
    """
        Gets the Unicode Script property of any character. Based on Scripts.txt from Unicode Consortium.
    """
    global indexes
    global scripts
    if not indexes:
        for line in open(scriptfile).readlines():
            indexes.append(int(line[:5], 16))
            scripts.append(line[6:-1])

    try:
        key = ord(char)
    except:
        key = ord(unicodedata.normalize('NFC', char))

    return scripts[(bisect.bisect_right(indexes, key) - 1)]


def inputloop():
    while True:
        for char in raw_input().decode('utf-8'):
            print script(char)


if __name__ == '__main__':
    inputloop()