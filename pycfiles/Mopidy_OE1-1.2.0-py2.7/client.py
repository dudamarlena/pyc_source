# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mopidy_oe1/client.py
# Compiled at: 2017-06-11 07:35:55
from __future__ import unicode_literals
import logging, urllib2
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import dateutil.parser, simplejson
logger = logging.getLogger(__name__)

class HttpClient(object):
    cache_opts = {b'cache.type': b'memory'}
    cache = CacheManager(**parse_cache_config_options(cache_opts))

    @cache.cache(b'get', expire=60)
    def get(self, url):
        try:
            logger.info(b"Fetching data from '%s'.", url)
            response = urllib2.urlopen(url)
            content = response.read()
            encoding = response.headers[b'content-type'].split(b'charset')[(-1)]
            return unicode(content, encoding)
        except Exception as e:
            logger.error(b"Error fetching data from '%s': %s", url, e)

    def refresh(self):
        self.cache.invalidate(self.get, b'get')


class OE1Client(object):
    archive_uri = b'http://audioapi.orf.at/oe1/json/2.0/broadcasts/'
    record_uri = b'https://audioapi.orf.at/oe1/api/json/current/broadcast/%s/%s'
    item_uri = b'http://loopstream01.apa.at/?channel=oe1&shoutcast=0&id=%s'
    LIVE = b'http://mp3stream3.apasf.apa.at:8000/'
    CAMPUS = b'http://mp3stream4.apasf.apa.at:8000/'

    def __init__(self, http_client=HttpClient()):
        self.http_client = http_client

    def get_days(self):

        def to_day(rec):
            return {b'id': _get_day_id(rec), 
               b'label': _get_day_label(rec)}

        json = self._get_archive_json()
        if json is not None:
            return [ to_day(rec) for rec in reversed(json) ]
        else:
            return []

    def get_day(self, day_id):

        def to_item(i, rec):
            time = dateutil.parser.parse(rec[b'startISO'])
            return {b'id': str(i), 
               b'time': time.strftime(b'%H:%M:%S'), 
               b'title': rec[b'title']}

        day_rec = self._get_day_json(day_id)
        items = [ to_item(i, broadcast_rec) for i, broadcast_rec in enumerate(day_rec[b'broadcasts']) if broadcast_rec[b'isBroadcasted']
                ]
        return {b'id': day_id, 
           b'label': _get_day_label(day_rec), 
           b'items': items}

    def get_item(self, day_id, item_id):
        day = self.get_day(day_id)
        return next(item for item in day[b'items'] if item[b'id'] == item_id)

    def get_item_url(self, day_id, item_id):
        day_rec = self._get_day_json(day_id)
        item_id = int(item_id)
        item_rec = day_rec[b'broadcasts'][item_id]
        json = self._get_record_json(item_rec[b'programKey'], day_id)
        streams = json[b'streams']
        if len(streams) == 0:
            return b''
        streamId = streams[0][b'loopStreamId']
        return OE1Client.item_uri % streamId

    def refresh(self):
        self.http_client.refresh()

    def _get_json(self, uri):
        try:
            content = self.http_client.get(uri)
            decoder = simplejson.JSONDecoder()
            return decoder.decode(content)
        except Exception as e:
            logger.error(b"Error decoding content received from '%s': %s", uri, e)

    def _get_archive_json(self):
        return self._get_json(OE1Client.archive_uri)

    def _get_day_json(self, day_id):
        json = self._get_archive_json()
        return next(rec for rec in json if _get_day_id(rec) == day_id)

    def _get_record_json(self, programKey, day):
        return self._get_json(OE1Client.record_uri % (programKey, day))


def _get_day_id(day_rec):
    return str(day_rec[b'day'])


def _get_day_label(day_rec):
    time = dateutil.parser.parse(day_rec[b'dateISO'])
    return time.strftime(b'%a %d. %b %Y')