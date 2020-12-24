# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/xmpp/ejabberdauth.py
# Compiled at: 2010-12-12 04:36:57
"""Script for ejabberd's external authentication mode."""
import sys, struct

def from_ejabberd():
    input_length = sys.stdin.read(2)
    (size,) = struct.unpack('>h', input_length)
    return sys.stdin.read(size).split(':')


def to_ejabberd(bool):
    answer = 0
    if bool:
        answer = 1
    token = struct.pack('>hh', 2, answer)
    sys.stdout.write(token)
    sys.stdout.flush()


def auth(username, server, password):
    return True


def isuser(username, server):
    return True


def setpass(username, server, password):
    return True


def main():
    while True:
        data = from_ejabberd()
        success = False
        if data[0] == 'auth':
            success = auth(data[1], data[2], data[3])
        elif data[0] == 'isuser':
            success = isuser(data[1], data[2])
        elif data[0] == 'setpass':
            success = setpass(data[1], data[2], data[3])
        to_ejabberd(success)