# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\test_catwalk.py
# Compiled at: 2011-06-10 12:37:00
import unittest
try:
    import json
except ImportError:
    import simplejson as json

from turbogears import controllers, expose, testutil
from turbogears.toolbox.catwalk import CatWalk
from catwalk_models import browse

def setup_module():
    testutil.start_server()


def teardown_module():
    testutil.stop_server()


def browse_data(model):
    """load some test data, only once"""
    if model.Artist.select().count() > 0:
        return
    genres = ('Latin Jazz Rock Pop Metal Dance Hall\n        Reggae Disco Funk Ska Swing Acid Folk Reggaeton\n        World Classic Hip-Hop Rythm&Blues Blues').split()
    for genre in genres:
        model.Genre(name=genre)

    instruments = ('bass drum').split()
    for instrument in instruments:
        model.Instrument(name=instrument)

    for artist_id in range(15):
        artist = model.Artist(name='Artist #%s' % artist_id)
        for album_id in range(15):
            album = model.Album(name='Album #%s_%s' % (artist_id, album_id), artist=artist)
            for song_id in range(15):
                model.Song(name='Song #%s_%s_%s' % (artist_id, album_id, song_id), album=album)

        for genre in model.Genre.select():
            genre.addArtist(artist)


class MyRoot(controllers.RootController):
    __module__ = __name__

    @expose()
    def index(self):
        pass


class Browse(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        browse_data(browse)
        testutil.mount(MyRoot(), '/')
        testutil.mount(CatWalk(browse), '/catwalk')
        self.app = testutil.make_app()

    def test_wrong_filter_format(self):
        response = self.app.get('/catwalk/browse/?object_name=Song&filters=Guantanemera&tg_format=json')
        assert 'filter_format_error' in response

    def test_wrong_filter_column(self):
        response = self.app.get('/catwalk/browse/?object_name=Song&filters=guacamole:2&tg_format=json')
        assert 'filter_column_error' in response

    def test_filters(self):
        response = self.app.get('/catwalk/browse/?object_name=Song&tg_format=json')
        values = json.loads(response.body)
        assert values['total'] == 15 * 15 * 15
        response = self.app.get('/catwalk/browse/?object_name=Song&filters=album:1&tg_format=json')
        response.headers['Content-Type'] = 'application/json'
        values = response.json
        assert values['total'] == 15

    def test_response_fields(self):
        response = self.app.get('/catwalk/browse/?object_name=Artist&start=3&page_size=20&tg_format=json')
        values = json.loads(response.body)
        assert 'headers' in values
        assert 'rows' in values
        assert 'start' in values
        assert 'page_size' in values
        assert 'total' in values
        assert values['start'] == 3
        assert values['page_size'] == 20
        assert values['total'] == 15

    def test_rows_joins_count(self):
        response = self.app.get('/catwalk/browse/?object_name=Artist&tg_format=json')
        values = json.loads(response.body)
        artist = browse.Artist.get(1)
        assert int(values['rows'][0]['genres']) == len(list(artist.genres))
        assert int(values['rows'][0]['albums']) == len(list(artist.albums))

    def test_rows_column_number(self):
        response = self.app.get('/catwalk/browse/?object_name=Artist&tg_format=json')
        values = json.loads(response.body)
        assert len(values['rows'][0]) == 4

    def test_rows_limit(self):
        response = self.app.get('/catwalk/browse/?object_name=Artist&tg_format=json')
        values = json.loads(response.body)
        assert 'rows' in values
        assert len(values['rows']) == 10
        response = self.app.get('/catwalk/browse/?object_name=Artist&page_size=15&tg_format=json')
        values = json.loads(response.body)
        assert 'rows' in values
        assert len(values['rows']) == 15

    def test_header_labels(self):
        response = self.app.get('/catwalk/browse/?object_name=Artist&tg_format=json')
        values = json.loads(response.body)
        assert len(values['headers']) == 5
        for header in values['headers']:
            assert header['name'] in ('id', 'name', 'albums', 'genres', 'plays_instruments')


class TestJoinedOperations(testutil.DBTest):
    __module__ = __name__
    model = browse

    def setUp(self):
        testutil.mount(MyRoot(), '/')
        testutil.mount(CatWalk(browse), '/catwalk')
        testutil.DBTest.setUp(self)
        browse_data(browse)
        self.app = testutil.make_app()

    def tearDown(self):
        testutil.DBTest.tearDown(self)

    def test_addremove_related_joins(self):
        artist = self.model.Artist.get(1)
        assert len(artist.plays_instruments) == 0
        self.app.get('/catwalk/updateJoins?objectName=Artist&id=1&join=plays_instruments&joinType=&joinObjectName=Instrument&joins=1%2C2&tg_format=json')
        assert len(artist.plays_instruments) == 2
        self.app.get('/catwalk/updateJoins?objectName=Artist&id=1&join=plays_instruments&joinType=&joinObjectName=Instrument&joins=1&tg_format=json')
        assert len(artist.plays_instruments) == 1