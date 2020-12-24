# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/importer_tests/test_mixpanel.py
# Compiled at: 2014-03-21 17:16:13
"""

    importer: mixpanel tests
    ~~~~~~~~~~~~~~~~~~~~~~~~

    this module tests ``Mixpanel``-specific provider functionality.

    :author: Sam Gammon <sam@keen.io>
    :license: This software follows the MIT (OSI-approved)
              license for open source software. A truncated
              version is included here; for full licensing
              details, see ``LICENSE.md`` in the root directory
              of the project.

              Copyright (c) 2013, Keen IO

              The above copyright notice and this permission notice shall be included in
              all copies or substantial portions of the Software.

              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
              THE SOFTWARE.

"""
import time, json, base64, random, unittest, datetime
from importer import mix
from importer.mix import _MIXPANEL_API
from importer.mix import _MIXPANEL_EXPORT
from importer.mix import Mixpanel
from importer.mix import MixpanelUploader
from importer.mix import MixpanelDownloader

class MixpanelTests(unittest.TestCase):
    """ Tests the ``Mixpanel`` provider class, which is
        exposed at :py:class:`mix.Mixpanel`. """
    random_ts = lambda self: datetime.datetime.fromtimestamp(random.randint(1377605000, 1377895000))

    def _valid_mixpanel_provider(self, instance=False, params=False):
        """ Tests the ``Mixpanel`` provider class, which is
            exposed at :py:class:`mix.Mixpanel`. """

        def _request(self, methods, params={}):
            """ Shim for submitting API requests to
                ``Mixpanel``. Returns ``self`` for
                chainability/introspection, unless
                the ``methods`` list contains 'export',
                in which case a fake export is mocked
                and returned. """
            self.mock_request = (
             methods, params)
            if 'export' in methods:
                return iter([
                 json.dumps({'event': 'sample_kind', 'properties': {'time': int(time.mktime(self.random_ts().timetuple())), 
                                   'blabs': True}}),
                 json.dumps({'event': 'sample_kind', 'properties': {'time': int(time.mktime(self.random_ts().timetuple())), 
                                   'bleebs': True}}),
                 ''])
            return self

        def _library(self, api_key, api_secret):
            """ Shim for constructing the API layer
                for ``Mixpanel``. Returns ``self`` for
                chainability/introspection. """
            self.api_key = api_key
            self.api_secret = api_secret
            return self

        _bus_, _name_, _library_, _adapters_, _config_ = (
         object(),
         'MIXPANEL',
         type('MixpanelMock', (object,), {'request': _request, 
            'api_key': None, 
            'api_secret': None, 
            'mock_request': None, 
            'Mixpanel': _library, 
            'random_ts': self.random_ts})(),
         (
          MixpanelUploader, MixpanelDownloader),
         {'api_key': '_api_key_', 
            'api_secret': '_api_secret_'})
        if instance:
            m = Mixpanel(_bus_, _name_, _library_, _adapters_, **_config_)
            if params:
                return ((_bus_, _name_, _library_, _adapter_, _config_), m)
            return m
        if params:
            return ((_bus_, _name_, _library_, _adapters_, _config_), Mixpanel)
        else:
            return Mixpanel

    def test_mixpanel_construct(self):
        """ Test the :py:class:`Mixpanel` class, which
            implements the :py:class:`Provider`
            interface. """
        _mixpanel_args, MixpanelProvider = self._valid_mixpanel_provider(instance=False, params=True)
        _bus, _name, _library, _adapters, _config = _mixpanel_args
        with self.assertRaises(TypeError):
            MixpanelProvider(_bus, _name, _library, tuple(), **_config)
        with self.assertRaises(TypeError):
            MixpanelProvider(_bus, _name, _library, (MixpanelUploader,), **_config)
        _valid_mixpanel = MixpanelProvider(_bus, _name, _library, _adapters, **_config)
        self.assertNotEqual(_valid_mixpanel.timezone, None)
        self.assertEqual(_valid_mixpanel.lib.api_key, '_api_key_')
        self.assertEqual(_valid_mixpanel.lib.api_secret, '_api_secret_')
        return

    def test_mixpanel_config(self):
        """ Test :py:attr:`Mixpanel.config`, which exposes
            ``Mixpanel``-related provider config listed in
            *importer's* ``config.json``. """
        _mixpanel_provider = self._valid_mixpanel_provider(instance=True)
        self.assertIsInstance(_mixpanel_provider.config, dict)
        self.assertEqual(_mixpanel_provider.config.get('api_key'), '_api_key_')
        self.assertEqual(_mixpanel_provider.config.get('api_secret'), '_api_secret_')

    def test_mixpanel_toggle_export(self):
        """ Test :py:attr:`Mixpanel` with Python's ``with``
            protocol, applied in this case to seamlessly
            switch the API endpoint used by ``Mixpanel``,
            which must be done when exporting versus
            importing events. """
        _mixpanel_provider = self._valid_mixpanel_provider(instance=True)
        self.assertEqual(_mixpanel_provider.client.ENDPOINT, _MIXPANEL_API)
        with self.assertRaises(RuntimeError):
            with _mixpanel_provider:
                self.assertEqual(_mixpanel_provider.client.ENDPOINT, _MIXPANEL_EXPORT)
                raise RuntimeError('this should bubble up')
        self.assertEqual(_mixpanel_provider.client.ENDPOINT, _MIXPANEL_API)


class MixpanelUploaderTests(MixpanelTests):
    """ Tests the ``Mixpanel`` uploader class, which is
        exposed at :py:class:`mix.MixpanelUploader`. """

    def test_mixpanel_upload(self):
        """ Test the :py:meth:`upload` method on the uploader
            for ``Mixpanel``, exposed at :py:class:`mix.MixpanelUploader`. """
        _mixpanel_provider = self._valid_mixpanel_provider(instance=True)
        uploader = _mixpanel_provider.uploader
        c_uploader = _mixpanel_provider.uploader
        self.assertEqual(uploader, c_uploader)
        event_1 = (
         'sample_kind', {'blab': True}, None)
        event_2 = ('sample_kind', {'bleebs': True}, datetime.datetime.fromtimestamp(random.randint(1377605000, 1377895000)))
        event_3 = ('sample_kind2', {'blops': True}, datetime.datetime.now())
        for kind, event, timestamp in (event_1, event_2, event_3):
            _mixpanel_provider.uploader.upload(kind, json.dumps(event), mix._TO_MIXPANEL_DATE(timestamp) if timestamp else None)

        self.assertTrue('sample_kind' in _mixpanel_provider.uploader.events_by_kind)
        self.assertTrue('sample_kind2' in _mixpanel_provider.uploader.events_by_kind)
        self.assertEqual(len(_mixpanel_provider.uploader.events_by_kind['sample_kind']), 2)
        self.assertEqual(len(_mixpanel_provider.uploader.events_by_kind['sample_kind2']), 1)
        return _mixpanel_provider

    def test_mixpanel_upload_commit(self):
        """ Test the :py:meth:`commit` method on the uploader
            for ``Mixpanel``, exposed at :py:class:`mix.MixpanelUploader`. """
        _mixpanel_provider = self._valid_mixpanel_provider(instance=True)
        self.assertEqual(len(_mixpanel_provider.uploader.events_by_kind.keys()), 2)
        self.assertEqual(len(_mixpanel_provider.uploader.events_by_kind['sample_kind']), 2)
        self.assertEqual(len(_mixpanel_provider.uploader.events_by_kind['sample_kind2']), 1)
        count = _mixpanel_provider.uploader.commit()
        self.assertEqual(count, 3)
        self.assertNotEqual(_mixpanel_provider.client.mock_request, None)
        return


class MixpanelDownloaderTests(MixpanelTests):
    """ Tests the ``Mixpanel`` downloader class, which is
        exposed at :py:class:`mix.MixpanelDownloader`. """

    def test_mixpanel_download(self):
        """ Test the :py:meth:`upload` method on the downloader
            for ``Mixpanel``, exposed at :py:class:`mix.MixpanelUploader`. """
        _mixpanel_provider = self._valid_mixpanel_provider(instance=True)
        downloader = _mixpanel_provider.downloader
        c_downloader = _mixpanel_provider.downloader
        self.assertEqual(downloader, c_downloader)
        start, end = datetime.datetime(year=2013, month=8, day=20, hour=12, minute=0, second=0), datetime.datetime(year=2013, month=8, day=30, hour=12, minute=0, second=0)
        events = []
        for kind, deserialized, timestamp in _mixpanel_provider.downloader.download(start, end, ['sample_kind']):
            self.assertIsInstance(kind, basestring)
            self.assertIsInstance(deserialized, dict)
            self.assertIsInstance(timestamp, datetime.datetime)
            self.assertEqual(kind, 'sample_kind')
            events.append((kind, deserialized, timestamp))

        self.assertEqual(len(events), 2)