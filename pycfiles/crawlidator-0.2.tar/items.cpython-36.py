# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/example/scrapy_movie/items.py
# Compiled at: 2019-12-25 23:33:52
# Size of source mod 2**32: 1439 bytes
import mongoengine as me, scrapy, pymongo
from mongoengine_mate import ExtendedDocument
from .config import Config
from .db import client, db
c_movie_listpage = db['movie_listpage']
c_movie = db['movie']

class MovieListPage(ExtendedDocument):
    _id = me.fields.IntField(primary_key=True)
    status = me.fields.IntField()
    edit_at = me.fields.DateTimeField()
    meta = dict(collection='site_movie_listpage',
      db_alias=(Config.MongoDB.database))


class ScrapyMovieListpageItem(scrapy.Item):
    _id = scrapy.Field()
    status = scrapy.Field()
    edit_at = scrapy.Field()

    def build_url(self):
        return '{}/movie/listpage/{}'.format(Config.Url.domain, self._id)

    def process(self):
        c_movie_listpage.update_one(filter={'_id': self['_id']},
          update={'$set': dict(self)},
          upsert=True)


class ScrapyMovieItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    edit_at = scrapy.Field()

    def process(self):
        c_movie.update_one(filter={'_id': self['_id']},
          update={'$set': dict(self)},
          upsert=True)