# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_translate_cli/cli.py
# Compiled at: 2014-04-17 10:10:31
# Size of source mod 2**32: 570 bytes
import requests, sys, re

def translate(text):
    url = 'http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8&sl=en&tl=zh-CN&text=' + text
    page = requests.get(url)
    prog = re.compile('\\[\\[\\["(\\w+)"')
    result = prog.match(page.text).group(1)
    return result


def help():
    print('Usage: tl TEXT1 TEXT2')


def main():
    if len(sys.argv) < 2:
        help()
        sys.exit()
    words = translate(' '.join(sys.argv[1:]))
    print(words)


if __name__ == '__main__':
    main()