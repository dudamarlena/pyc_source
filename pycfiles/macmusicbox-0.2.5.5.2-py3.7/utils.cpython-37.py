# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/utils.py
# Compiled at: 2020-03-16 06:23:11
# Size of source mod 2**32: 1797 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import platform, subprocess, os
from collections import OrderedDict
from copy import deepcopy
from future.builtins import str
__all__ = [
 'utf8_data_to_file', 'notify', 'uniq', 'create_dir', 'create_file']

def mkdir(path):
    try:
        os.mkdir(path)
        return True
    except OSError:
        return False


def create_dir(path):
    if not os.path.exists(path):
        return mkdir(path)
    if os.path.isdir(path):
        return True
    os.remove(path)
    return mkdir(path)


def create_file(path, default='\n'):
    if not os.path.exists(path):
        with open(path, 'w') as (f):
            f.write(default)


def uniq(arr):
    return list(OrderedDict.fromkeys(arr).keys())


def utf8_data_to_file(f, data):
    if hasattr(data, 'decode'):
        f.write(data.decode('utf-8'))
    else:
        f.write(data)


def notify(msg, msg_type=0, t=None):
    msg = msg.replace('"', '\\"')
    command = ['/usr/bin/osascript', '-e']
    tpl = 'display notification "{}" {} with title "musicbox"'
    sound = 'sound name "/System/Library/Sounds/Ping.aiff"' if msg_type else ''
    command.append(tpl.format(msg, sound).encode('utf-8'))
    try:
        subprocess.call(command)
        return True
    except OSError as e:
        try:
            return False
        finally:
            e = None
            del e


if __name__ == '__main__':
    notify('I\'m test ""quote', msg_type=1, t=1000)
    notify("I'm test 1", msg_type=1, t=1000)
    notify("I'm test 2", msg_type=0, t=1000)
    print(parse_keylist([48, 49, 55, 91]))