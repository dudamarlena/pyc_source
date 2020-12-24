# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/get_podcast_data.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 1574 bytes
from hoerapi.lowlevel import call_api
from hoerapi.parser import parser_object
from hoerapi.util import parse_bool, CommonEqualityMixin

class PodcastDataContact(CommonEqualityMixin):

    def __init__(self, data):
        if isinstance(data, list):
            return
        self.twitter = data.get('twitter', None)
        self.adn = data.get('adn', None)
        self.email = data.get('email', None)


class PodcastData(CommonEqualityMixin):

    def __init__(self, data):
        self.id = int(data['ID'])
        self.title = data['title']
        self.description = data['description']
        self.url = data['url']
        self.feedurl = data['feedurl']
        self.imageurl = data['imageurl']
        self.slug = data['slug']
        self.recension = data['recension']
        self.cluster = data['cluster']
        self.rec_pos = data['rec_pos']
        self.rec_neg = data['rec_neg']
        self.chat_server = data['chat_server']
        self.chat_channel = data['chat_channel']
        self.chat_url = data['chat_url']
        self.obsolete = parse_bool(data['obsolete'])
        self.freeze = parse_bool(data['freeze'])
        self.otitle = data['otitle']
        self.feature = parse_bool(data['feature'])
        self.contact = PodcastDataContact(data['contact'])
        self.rundfunk = parse_bool(data['rundfunk'])


def get_podcast_data(podcast):
    return parser_object(PodcastData, call_api('getPodcastData', {'podcast': podcast}))