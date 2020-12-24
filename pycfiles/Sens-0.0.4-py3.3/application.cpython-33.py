# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sens/application.py
# Compiled at: 2013-10-13 11:26:06
# Size of source mod 2**32: 860 bytes
import argparse, sys, sens.image, sens.status

def main():
    parser = argparse.ArgumentParser(description='Generate twitch status image')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser.add_argument('channel_name', metavar='channel-name', help='Channel to pull data from')
    parser.add_argument('file', help='File to write image to')
    args = parser.parse_args()
    try:
        img = build_image(args.channel_name)
        img.save(args.file, format='png')
    except sens.status.TwitchError as e:
        print('Error retrieving channel data from Twitch.tv', file=sys.stderr)
        if args.verbose:
            print('Response: {json}'.format(json=e.json), file=sys.stderr)


def build_image(channel_name):
    s = sens.status.get_status(channel_name)
    return sens.image.build_image(s)