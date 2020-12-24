# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/android.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 920 bytes
from re import sub
from subprocess import run

def adbenter():
    adb = '/usr/bin/adb'
    run(('%s shell input keyevent 66' % adb), shell=True)


def adbout(text, enter=None):
    adb = '/usr/bin/adb'
    text = sub('(\\s|\\$|\\%|\\&|\\(|\\)|\\=|\\?|\\-|\\!|\\+|\\.)', '\\\\\\1', text)
    text = sub('"', '\\\\\\\\\\"', text)
    text = sub("'", "\\'", text)
    run(('%s shell input text "%s"' % (adb, '%s' % text)), shell=True)
    if enter:
        adbenter()