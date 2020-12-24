# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\models.py
# Compiled at: 2020-04-19 14:32:46
# Size of source mod 2**32: 5504 bytes
from typing import Dict, List, Optional

class BanInfo:

    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.discriminator = data['discriminator']
        self.moderator_id = data['moderator_id']
        self.reason = data['reason']
        self.proof = data['proof']
        self.is_ban_active = data['is_ban_active']
        self.can_be_appealed = data['can_be_appealed']
        self.timestamp = data['timestamp']
        self.appeal_reason = data['appeal_reason']
        self.appeal_date = data['appeal_date']
        self.requested_by = data['requested_by']
        self.exists = data['exists']


class BanSimple:

    def __init__(self, data: dict):
        self.id = data['id']
        self.reason = data['reason']
        self.proof = data['proof']
        self.moderator_id = data['moderator_id']
        self.active = data['is_ban_active']


class Image:

    def __init__(self, data: dict):
        self.url = data['url']
        self.snowflake = data['snowflake']
        self.nsfw = data['nsfw']
        self.tag = data['tag']


class Location:

    def __init__(self, data: dict):
        self.address = data['address']
        self.lat = data['lat']
        self.lon = data['lon']
        self.bounding_box = data['bounding_box']
        self.type = data['type']
        self.map = data.get('map')


class LyricResult:

    def __init__(self, data: dict):
        self.artist = data['artist']
        self.artist_id = data['artist_id']
        self.album = data['album']
        self.album_ids = data['album_ids'].split(',')
        self.album_year = data['album_year'].split(',')
        self.name = data['name']
        self.lyrics = data['lyrics']
        self.search_str = data['search_str']
        self.album_art = data['album_art']
        self.popularity = data['popularity']
        self.id = data['id']
        self.search_score = data['search_score']


class PaginatorListing:

    def __init__(self, data: dict):
        self.count = data['ban_count']
        self.page_count = data['page_count']
        self.per_page = data['per_page']
        self.page = data['page']
        self.on_page = data['on_page']
        self.next_page = data['next_page']
        self.previous_page = data['previous_page']
        self.data = [BanInfo(ban) for ban in data['data']]


class Recommendation:

    def __init__(self, data: dict):
        youtube = data['youtube']
        spotify = data['spotify']
        spotify_album = spotify['album']
        spotify_artists = spotify['artists']
        self.name = data['name']
        self.youtube_id = youtube['id']
        self.youtube_link = youtube['link']
        self.youtube_title = youtube['title']
        self.youtube_thumbnail = youtube['thumbnail']
        self.spotify_id = spotify['id']
        self.spotify_name = spotify['name']
        self.spotify_link = spotify['link']
        self.spotify_album_name = spotify_album['name']
        self.spotify_album_art = spotify_album['album_art']
        self.spotify_album_link = spotify_album['link']
        self.spotify_artists = [{'name':artist['name'], 
         'link':artist['link']} for artist in spotify_artists]


class RedditImage:

    def __init__(self, data: dict):
        self.author = data.get('author')
        self.title = data.get('title')
        self.image_url = data.get('image_url')
        self.source = data.get('source')
        self.subreddit = data.get('subreddit')
        self.upvotes = data.get('upvotes')
        self.downvotes = data.get('downvotes')
        self.comments = data.get('comments')
        self.created_at = data.get('created_at')
        self.nsfw = data.get('nsfw')


class Tag:

    def __init__(self, data: dict):
        self.name = data.get('name')
        self.nsfw = data.get('nsfw')

    def __str__(self):
        return self.name


class TagCollection:

    def __init__(self, data: dict):
        self.raw_models = data.get('models')
        self.models = [Tag(t) for t in self.raw_models]
        self.sfw_tags = data.get('tags')
        self.nsfw_tags = data.get('nsfw_tags', [])

    def __len__(self):
        return len(self.models)

    def __dict__(self):
        return self.raw_models

    def __getitem__(self, item):
        return next((item == t.name for t in self.models), None)

    def __iter__(self):
        for t in self.models:
            (yield t)

    def __str__(self):
        return ', '.join([t.name for t in self.models])

    def exists(self, name):
        return any((name == t.name for t in self.models))


class WikiHowImage:

    def __init__(self, data: dict):
        self.url = data.get('url')
        self.title = data.get('title')
        self.nsfw = data.get('nsfw')
        self.article_url = data.get('article_url')