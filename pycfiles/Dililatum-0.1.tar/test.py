# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niels/Programming/questy/debugtests/test.py
# Compiled at: 2010-07-03 14:08:33


def extra1(event):
    print event.args[0].debugargs


def extra2(event):
    print event


def extra3(event):
    char = event.args[0]
    verb = event.uargs[0]
    print char.id + ' ' + verb + ' the name..'


def main():
    action('beforesystemstart', extra1)
    action('beforegamestart', extra2)
    action('beforecharacteradd', extra3, 'is')


print dir(super)