# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smarty/cmd_line_parser.py
# Compiled at: 2014-01-17 04:54:24
# Size of source mod 2**32: 1094 bytes
import argparse, os
parser = argparse.ArgumentParser(description='Smart playlist generator written in python.')
parser.add_argument('-i', '--ip', help='IP address of mpd server', type=str, metavar='<ip>', default=os.getenv('MPD_HOST', 'localhost'))
parser.add_argument('-p', '--port', help='Port mpd server is listening on', type=int, metavar='<port>', default=6600)
parser.add_argument('--maxnum', help='Maximal number of songs in playlist', type=int, metavar='<num>', dest='max_num', default=50)
parser.add_argument('--dist', help='Add new song if only <x> songs are left to play in current playlist', type=int, metavar='<num>', dest='songs_to_end', default=5)
parser.add_argument('--norepeat', help="Don't add songs which are already in playlist.", action='store_true')
parser.add_argument('-v', '--verbose', help='Print information about running process', action='store_true')
parser.add_argument('--exclude', help='Never add these genres to playlist', nargs='+', metavar='genre', default=[])

def get_args():
    return parser.parse_args()