# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/raony/dev/venv/lib/python3.5/site-packages/sudden/main.py
# Compiled at: 2017-12-16 21:02:54
# Size of source mod 2**32: 403 bytes
from subprocess import call

class Sudden:

    def __init__(self):
        pass

    def main(self):
        print('Main Hello World!')

    def update(self):
        call('sudo apt update', shell=True)
        call('sudo apt upgrade', shell=True)

    def install(self, tools):
        print('install {}'.format(tools))
        for tool in tools:
            print(tool)


if __name__ == '__main__':
    sudden = Sudden()
    sudden.main()