# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jikkensol/hello.py
# Compiled at: 2017-12-10 23:48:06
# Size of source mod 2**32: 625 bytes
import sys, os

class Hello:

    def __init__(self, name):
        self._name = name

    def say(self):
        print('{}さん、こんにちは。'.format(self._name))

    def song(self):
        print('バージョン 0.0.10')
        song_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'files' + os.sep + 'songs.txt'
        with open(song_file, 'rt') as (f):
            while True:
                line = f.readline()
                if not line:
                    break
                print(line, end='')


if __name__ == '__main__':
    h = Hello('太郎')
    h.say()
    h.song()