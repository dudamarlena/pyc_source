# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\playlist_dl\standalone.py
# Compiled at: 2015-11-01 13:23:54
# Size of source mod 2**32: 288 bytes
from pathlib import Path

def run():
    print('Running' if __name__ == '__main__' else 'Imported', Path(__file__).name)
    print(Path(__file__))
    with open('playlist_dl.py') as (f):
        code = compile(f.read(), 'playlist_dl.py', 'exec')
        exec(code)


if __name__ == '__main__':
    run()