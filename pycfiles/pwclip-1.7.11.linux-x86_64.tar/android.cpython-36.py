# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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