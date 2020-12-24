# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nivekuil/code/amp/python3/amp/main.py
# Compiled at: 2016-10-28 21:42:22
# Size of source mod 2**32: 3106 bytes
import os, sys, argparse, pafy
from .player import Player
from .process import kill_process_tree
from .process import toggle_process_tree
from .util import get_search_results
USAGE = 'Usage: amp [SEARCH TERMS]\nPass search terms to YouTube and play the first result in a background process.\nCall again with no arguments to stop playback.\n'
PIDFILE = '/tmp/amp.pid'
INFOFILE = '/tmp/amp.info'

def main():
    opts = {}
    parser = argparse.ArgumentParser(description='Pass search terms to YouTube\n    and play the first result in a background process.\n    Call again with no arguments to pause or resume playback.', prog='amp')
    parser.add_argument('-v', action='store_true', help='show the video as well')
    parser.add_argument('-i', action='store_true', help='print video info')
    parser.add_argument('-k', action='store_true', help='kill playback process')
    parser.add_argument('--verbose', action='store_true', help='show verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.27-3')
    args = parser.parse_known_args()
    opts['vid'] = 'auto' if args[0].v else 'no'
    if args[0].i:
        try:
            with open(INFOFILE, 'r') as (f):
                print(f.read())
        except OSError:
            print('No info found.')

        sys.exit(0)
    if len(args[1]) == 0:
        try:
            with open(PIDFILE, 'r') as (f):
                pid = int(f.read().strip())
                if args[0].k:
                    kill_process_tree(pid)
                    os.remove(PIDFILE)
                    print('Killed playback process.')
                    return
                try:
                    toggle_process_tree(pid)
                except:
                    print('pidfile invalid; was amp killed uncleanly?')

        except OSError:
            parser.print_help()

        sys.exit(0)
    if args[1]:
        input = ' '.join(args[1])
    else:
        parser.print_help()
        sys.exit(0)
    search_results = get_search_results(input)
    url = 'https://www.youtube.com/watch?v=' + search_results[0]
    player = Player(url, show_video=args[0].v, verbose=args[0].verbose)
    player.start()


if __name__ == '__main__':
    sys.exit(main())