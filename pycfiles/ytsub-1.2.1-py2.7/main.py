# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ytsub/main.py
# Compiled at: 2013-01-12 09:59:31
import argparse, sys, httplib2, api, logging, fileinput, re, pprint
from __init__ import __version__
from apiclient.discovery import build
from credentials import acquire_credentials
from argparse_util import ListOrStdinAction
from argparse_util import MaxCountAction
__VID_REGEX = re.compile('^(?:(?:(?:http://)?www\\.)?youtube\\.com/watch\\?\\S*?v=)?([a-zA-Z0-9_-]{11})\\S*$')
__LOG_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')

def _days(strin):
    try:
        ret = int(strin)
    except ValueError:
        raise argparse.ArgumentTypeError('Days must be an integer. Given: ' + strin)

    if ret < 0:
        raise argparse.ArgumentTypeError('Days must be greater than or equal to 0. Given: ' + strin)
    return ret


def _vid_count(strin):
    try:
        ret = int(strin)
    except ValueError:
        raise argparse.ArgumentTypeError('Video count must be an integer.')

    if ret < 0:
        raise argparse.ArgumentTypeError('Days must be greater than or equal to 0.')
    return ret


def _videoID(url_or_id):
    match = __VID_REGEX.match(url_or_id)
    if not match:
        raise ValueError('Value must be a youtube video id or the watch url.')
    return match.group(1)


def _format_vid(format_string, vid):
    return format_string.format(vid=vid.id, date=vid.date, title=vid.title, author=vid.author)


def _setup():
    SCOPES = 'https://www.googleapis.com/auth/youtube'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    logging.basicConfig()
    credentials = acquire_credentials(SCOPES)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))
    return (
     youtube, credentials)


def _list(args):
    youtube, credentials = _setup()
    watched = api.get_watched_ids(youtube, credentials)
    new = api.get_sub_vids(youtube, credentials, args.max_vids_per_sub, args.age_max)
    unwatched_new = filter(lambda x: x.id not in watched, new)
    unwatched_new.sort(reverse=True)
    for v in unwatched_new:
        print _format_vid('{vid}\t{date}\t{author}\t{title}', v)


def _mark_watched(args):
    youtube, credentials = _setup()
    api.mark_watched(youtube, credentials, args.ids)


def main():
    parser = argparse.ArgumentParser(description='Perform useful tasks on your Youtube video subscriptions.')
    parser.add_argument('-v', '--verbose', action=MaxCountAction, default=0, max_count=len(__LOG_LEVELS) - 1, max_exceeded_msg='flag included too many times; {count} out of range of ' + str(__LOG_LEVELS), help=('Increases verbosity level.  Use multiple times to max of {maxl}.').format(maxl=len(__LOG_LEVELS) - 1))
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title='subcommands')
    list_parser = subparsers.add_parser('list', description='List your new Youtube subscription videos.')
    list_parser.add_argument('-t', '--upload-time', help='Limit to videos no older than N days. If option present with no argument, not limited.', type=_days, default=5, const=-1, nargs='?', metavar='N', dest='age_max')
    list_parser.add_argument('-c', '--vid-count', help='Limit to N videos from each subscription. If option present with no argument, not limited.', type=_vid_count, default=50, const=-1, nargs='?', metavar='N', dest='max_vids_per_sub')
    list_parser.set_defaults(func=_list)
    mark_watched_parser = subparsers.add_parser('mark-watched', description='Mark video ids as watched.')
    mark_watched_parser.add_argument('ids', type=_videoID, action=ListOrStdinAction, metavar='Video ID')
    mark_watched_parser.set_defaults(func=_mark_watched)
    args = parser.parse_args()
    logging.getLogger().setLevel(__LOG_LEVELS[args.verbose])
    args.func(args)