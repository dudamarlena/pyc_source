# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neil/Scripts/tweetcal/build/lib/tweetcal/read_archive.py
# Compiled at: 2015-10-02 19:17:09
# Size of source mod 2**32: 2435 bytes
import re, time, logging
from datetime import datetime
from email.utils import formatdate
from tweepy import API, Status
from twitter_bot_utils import archive
from . import tweetcal
iso8601 = re.compile('(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) ?(\\+\\d{4})?')

def fix_timeformat(string):
    match = iso8601.match(string)
    if match:
        dt = datetime.strptime(match.groups()[0], '%Y-%m-%d %H:%M:%S')
        string = formatdate(time.mktime(dt.timetuple()))
    return string


def read_as_status(archivepath, since_id=None, max_id=None):
    api = API()
    since_id = since_id or 1
    max_id = max_id or float('inf')
    for tweet in archive.read_json(archivepath):
        tweet['created_at'] = fix_timeformat(tweet['created_at'])
        if tweet.get('retweeted_status'):
            tweet['retweeted_status']['created_at'] = fix_timeformat(tweet['retweeted_status']['created_at'])
        i = int(tweet['id'])
        if i > since_id and i < max_id:
            yield Status.parse(api, tweet)


def to_cal(archivepath, output, dry_run=None, **kwargs):
    """Read an archive into a calendar"""
    logger = logging.getLogger('tweetcal')
    max_id = kwargs.get('max_id', float('inf'))
    since_id = kwargs.get('since_id', 1)
    generator = lambda x: read_as_status(archivepath, max_id=max_id, since_id=since_id)
    cal = tweetcal.new_calendar()
    logger.info('Reading archive.')
    tweetcal.add_to_calendar(cal, generator)
    logger.info('Added {} tweets to calendar.'.format(len(cal)))
    if not dry_run:
        tweetcal.write_calendar(cal, output)
        logger.info('Wrote {}.'.format(output))


def to_cal_args(path, output, **kwargs):
    tweetcal.setup_logger(kwargs.get('verbose'))
    to_cal(path, output, dry_run=kwargs.get('dry_run'), since_id=kwargs.get('since_id'), max_id=kwargs.get('max_id'))