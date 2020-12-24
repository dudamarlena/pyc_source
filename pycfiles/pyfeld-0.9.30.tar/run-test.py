# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/run-test.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import re, subprocess, sys
from time import sleep
from pyfeld.dirBrowse import DirBrowse

def retrieve(cmd):
    command = b'pyfeld ' + cmd
    print command
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        return 0

    lines = b''
    while True:
        nextline = process.stdout.readline()
        if len(nextline) == 0 and process.poll() != None:
            break
        lines += nextline.decode(b'utf-8')

    return lines


def show_dir(dir_browser):
    for i in range(0, dir_browser.max_entries_on_level() - 1):
        print dir_browser.get_friendly_name(i)


def info():
    print b'This is a simple info'
    print retrieve(b'--discover info')
    print b'This is an extended info'
    print retrieve(b'--discover -v -v info')
    dir_browser = DirBrowse()
    print b'Feching containers and items'
    for i in [1, 1, 0]:
        dir_browser.enter(i)
        print b'Friendly path: ' + dir_browser.get_friendly_path_name(b' -> ')
        print b'Friendly name of item: ' + dir_browser.get_friendly_name(0)
        print b'Path: ' + dir_browser.get_path_for_index(0)
        print b'Info on item:' + retrieve(b'--json browseinfo "' + dir_browser.get_path_for_index(0) + b'"')


def rooms():
    print b'This is a list of the rooms'
    rooms = retrieve(b'--discover rooms')
    room_list = rooms.splitlines(False)
    print room_list
    print b'Going to remove all rooms from zones, say bye bye'
    for room in room_list:
        retrieve(b'drop ' + room)

    retrieve(b'--discover')
    print b'This is a simple info'
    print retrieve(b'--discover info')
    zonecmd = b'createzone '
    for room in room_list:
        zonecmd += b"'" + room + b"' "

    retrieve(zonecmd)
    print b'This is an updated list of the zone (should be one big only)'
    print retrieve(b'--discover zones')


def browse():
    print b'Going to browse the root folder'
    dir_browser = DirBrowse()
    show_dir(dir_browser)
    print b'Going to enter the second folder'
    dir_browser.enter(1)
    show_dir(dir_browser)
    print b'Going to enter the next folder'
    dir_browser.enter(1)
    print dir_browser.path
    show_dir(dir_browser)
    print b'Going to enter the next folder'
    dir_browser.enter(1)
    print dir_browser.path
    show_dir(dir_browser)
    retrieve(b'--discover rooms')
    dir_browser.leave()
    print dir_browser.path
    show_dir(dir_browser)
    retrieve(b'--discover zones')
    dir_browser.leave()
    print dir_browser.path
    show_dir(dir_browser)


def play():
    print b'fetching rooms'
    rooms = retrieve(b'--discover rooms')
    room_list = rooms.splitlines(False)
    dir_browser = DirBrowse()
    dir_browser.enter(1)
    dir_browser.enter(1)
    path = dir_browser.get_path_for_index(2)
    retrieve(b'--zonewithroom ' + room_list[0] + b' play "' + path + b'"')
    print b'waiting a moment, then we will look at some track info'
    sleep(10)
    print retrieve(b'--zonewithroom ' + room_list[0] + b' zoneinfo')
    print b'seeking to 02:00 and again we will look at some track info'
    print retrieve(b'--zonewithroom ' + room_list[0] + b' seek 00:01:34')
    sleep(2)
    print retrieve(b'--zonewithroom ' + room_list[0] + b' zoneinfo')
    print b"Let's play with volume"
    print retrieve(b'--zonewithroom ' + room_list[0] + b' setvolume 30')
    print retrieve(b'--zonewithroom ' + room_list[0] + b' getvolume')
    sleep(2)
    print retrieve(b'--zonewithroom ' + room_list[0] + b' setvolume 40')
    print retrieve(b'--zonewithroom ' + room_list[0] + b' getvolume')
    sleep(2)
    print retrieve(b'--zonewithroom ' + room_list[0] + b' setvolume 20')
    print retrieve(b'--zonewithroom ' + room_list[0] + b' getvolume')


def usage(argv):
    print (
     b'Usage: {0} [test]', argv[0])
    print b'  browse'
    print b'  play'
    print b'  rooms'
    print b'  info'


if __name__ == b'__main__':
    if len(sys.argv) == 1:
        usage(sys.argv)
    elif sys.argv[1] == b'browse':
        browse()
    elif sys.argv[1] == b'play':
        play()
    elif sys.argv[1] == b'rooms':
        rooms()
    elif sys.argv[1] == b'info':
        info()
    elif sys.argv[1] == b'all':
        browse()
        play()
        rooms()
        info()
    else:
        print (b'command {0} not found!').format(sys.argv[1])
        usage(sys.argv)