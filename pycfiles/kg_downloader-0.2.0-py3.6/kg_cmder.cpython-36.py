# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kg_downloader\kg_cmder.py
# Compiled at: 2019-11-25 14:25:34
# Size of source mod 2**32: 1307 bytes
from getopt import getopt, GetoptError
import sys
from os import getenv
VERSION = 'kg_downloader: 0.1.3 Written by Justin13\nBug report: justin13wyx@gmail.com'
help_info = {'kg_downloader [-l|--location] url':'Let kg_downloader analyse the given url and download songs.', 
 'kg_downloader -l|--location':'Specify the download path.[default: HOME]', 
 'kg_downloader -v|--version':'Display version information.', 
 'kg_downloader -h|--help':'Print this help information.'}

def usage():
    m = max(map(len, help_info.keys()))
    print('Usage:')
    for k in help_info:
        print('\t', k.ljust(m), '\t', help_info[k])


def version():
    print(VERSION)


def parse_cmd():
    location = getenv('HOME')
    try:
        opts, args = getopt(sys.argv[1:], 'vhls', ['version', 'help', 'location', 'speed'])
    except GetoptError:
        print('Bad parameter.\n')
        usage()
        exit(3)

    for val in opts:
        val = val[0]
        if val in ('-v', '--version'):
            version()
            exit(0)
        else:
            if val in ('-h', '--help'):
                usage()
                exit(0)
            else:
                if val in ('-l', '--location'):
                    location = args[0]

    if not args:
        print('You miss your url.')
        usage()
        exit(3)
    return (
     args[(-1)], location)