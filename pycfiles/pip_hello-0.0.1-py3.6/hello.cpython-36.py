# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pip-hello\hello.py
# Compiled at: 2018-08-21 03:37:12
# Size of source mod 2**32: 209 bytes


class Hello:

    def __init__(self, name):
        self.name = name

    def say(self):
        print('Hello %s!' % self.name)


if __name__ == '__main__':
    hello = Hello('YY')
    hello.say()