# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spotify_to_google/command_line.py
# Compiled at: 2017-07-09 12:20:45
import getpass, argparse
from spotify_to_google import import_all_playlists

def main():
    parser = argparse.ArgumentParser(description='Imports playlists from ')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('-g', '--google', type=str, required=True, help='Google username')
    parser.add_argument('-s', '--spotify', type=str, required=True, help='Spotify username')
    parser.add_argument('-v', '--verbose', action='count', help='Output verbosity level')
    args = parser.parse_args()
    password = getpass.getpass('Enter password for user %s:\n' % args.google)
    import_all_playlists(args.spotify, args.google, password)