# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/get_podcast_live.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 1513 bytes
from hoerapi.lowlevel import call_api
from hoerapi.util import parse_date, parse_bool, CommonEqualityMixin
from hoerapi.parser import parser_list
from hoerapi.errors import InvalidDataError

class PodcastLive(CommonEqualityMixin):

    def __init__(self, data):
        self.id = data['id']
        self.podcast = data['podcast']
        self.state = int(data['state'])
        self.type = int(data['type'])
        self.synced = parse_bool(data['synced'])
        self.title = data['title']
        self.url = data['url']
        self.streamurl = data['streamurl']
        self.livedate = parse_date(data['livedate'])
        self.duration = int(data['duration'])
        self.twittered = parse_bool(data['twittered'])


def get_podcast_live(podcast, count=5):
    return parser_list(PodcastLive, call_api('getPodcastLive', {'podcast': podcast, 
     'count': count}))


def get_live_by_id_parser(data):
    if data is not None and isinstance(data, list) and len(data) == 1:
        return PodcastLive(data[0])
    raise InvalidDataError('not an array')


def get_live_by_id(id):
    return get_live_by_id_parser(call_api('getLiveByID', {'ID': id}))


def get_live(count=5, dateStart=None, dateEnd=None):
    params = {'count': count}
    if dateStart is not None:
        params['dateStart'] = dateStart.strftime('%y-%m-%d')
    if dateEnd is not None:
        params['dateEnd'] = dateEnd.strftime('%y-%m-%d')
    return parser_list(PodcastLive, call_api('getLive', params))