# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sens/status.py
# Compiled at: 2013-10-15 13:25:44
# Size of source mod 2**32: 2077 bytes
import http.client, io, json
HOSTNAME = 'api.twitch.tv'
BASE_PATH = '/kraken'
HEADERS = {'Accept': 'application/vnd.twitchtv.v3+json'}

class TwitchError(Exception):

    def __init__(self, response, json_data, *args, **kwargs):
        super(TwitchError, self).__init__(*args, **kwargs)
        self.response = response
        self.json = json_data


class ChannelNotFoundError(TwitchError):
    pass


def get_twitch_path(path):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request('GET', path, headers=HEADERS)
    resp = conn.getresponse()
    json_data = json.load(io.TextIOWrapper(resp))
    if resp.status == 404:
        raise ChannelNotFoundError(resp, json_data)
    elif resp.status != 200:
        raise TwitchError(resp, json_data)
    return json_data


def get_stream(channel_name):
    path = '{base}/streams/{channel_name}'.format(base=BASE_PATH, channel_name=channel_name)
    return get_twitch_path(path)


def get_channel(channel_name):
    path = '{base}/channels/{channel_name}'.format(base=BASE_PATH, channel_name=channel_name)
    return get_twitch_path(path)


def get_status(channel_name):
    channel_data = get_channel(channel_name)
    stream_data = get_stream(channel_name)
    display_name = channel_data['display_name']
    status = channel_data['status']
    game = channel_data['game']
    logo_url = channel_data['logo']
    online = stream_data['stream'] is not None
    viewers = stream_data['stream']['viewers'] if online else None
    preview_url = stream_data['stream']['preview']['small'] if online else None
    return TwitchStatus(logo_url, status, display_name, game, online, viewers, preview_url)


class TwitchStatus(object):

    def __init__(self, logo_url, status, display_name, game, online, viewers, preview_url):
        self.logo_url = logo_url
        self.status = status
        self.display_name = display_name
        self.game = game
        self.online = online
        self.viewers = viewers
        self.preview_url = preview_url