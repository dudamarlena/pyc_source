# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/playlist.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 717 bytes
import sys
from prettytable import PrettyTable
from musicbot.helpers import Green, Reset

def print_playlist(tracks, file=None, current_title=None, current_album=None, current_artist=None):
    file = file if file is not None else sys.stdout
    pt = PrettyTable()
    pt.field_names = [
     'Title',
     'Album',
     'Artist']
    for t in tracks:
        title = Green + t['title'] + Reset if t['title'] == current_title else t['title']
        album = Green + t['album'] + Reset if t['album'] == current_album else t['album']
        artist = Green + t['artist'] + Reset if t['artist'] == current_artist else t['artist']
        pt.add_row([title, album, artist])
    else:
        print(pt, file=file)