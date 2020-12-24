# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/importer_tests/test_keen.py
# Compiled at: 2014-02-03 17:56:37
"""

    importer: keen tests
    ~~~~~~~~~~~~~~~~~~~~

    this module tests ``Keen``-specific provider functionality.

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
import json, time, random, unittest, datetime
from importer import mix
from importer.mix import Keen
from importer.mix import KeenUploader
from importer.mix import KeenDownloader

class KeenTests(unittest.TestCase):
    """ Tests the ``Keen`` provider class, which is
        exposed at :py:class:`mix.Keen`. """

    def _valid_keen_provider(self, instance=False, params=False):
        """ Generate a valid :py:class:`Keen` provider
            object, with minimal config/etc for use
            in testing. """

        def _add_events(self, events):
            """ Quick shim to simulate a mocked ``Keen``
                library, supporting batch event writes. """
            self.events_cache = events
            return self

        def _extraction(self, kind, range):
            """ Quick shim to simulate a mocked ``Keen``
                library, supporting event extractions. """
            dt = datetime.datetime(year=2013, month=8, day=24, hour=12, minute=30, second=0)
            dt2 = datetime.datetime(year=2013, month=8, day=25, hour=12, minute=35, second=0)
            return [{'kind': kind, 'prop': 123, 'keen': {'timestamp': mix._TO_KEEN_DATE(dt)}}, {'kind': kind, 'prop': 124, 'keen': {'timestamp': mix._TO_KEEN_DATE(dt2)}}]

        _bus_, _name_, _library_, _adapters_, _config_ = (
         object(),
         'KEEN',
         type('KeenMock', (object,), {'project_id': None, 
            'read_key': None, 
            'write_key': None, 
            'add_events': _add_events, 
            'extraction': _extraction, 
            'events_cache': None})(),
         (
          KeenUploader, KeenDownloader),
         {'read_key': '__read_key__', 
            'write_key': '__write_key__', 
            'project_id': '__project_id__'})
        if instance:
            k = Keen(_bus_, _name_, _library_, _adapters_, **_config_)
            if params:
                return ((_bus_, _name_, _library_, _adapters_, _config_), k)
            return k
        if params:
            return ((_bus_, _name_, _library_, _adapters_, _config_), Keen)
        else:
            return Keen

    def test_keen_construct(self):
        """ Test the :py:class:`Keen` class, which
            implements the :py:class:`Provider`
            interface. """
        _keen_args, KeenProvider = self._valid_keen_provider(instance=False, params=True)
        _bus, _name, _library, _adapters, _config = _keen_args
        with self.assertRaises(TypeError):
            KeenProvider(_bus, _name, _library, tuple(), **_config)
        with self.assertRaises(TypeError):
            KeenProvider(_bus, _name, _library, (KeenUploader,), **_config)
        _valid_keen = KeenProvider(_bus, _name, _library, _adapters, **_config)
        self.assertEqual(_valid_keen.bus, _bus)
        self.assertEqual(_valid_keen.lib, _library)
        self.assertEqual(_valid_keen.name, 'KEEN')
        self.assertIsInstance(_valid_keen.adapters, tuple)
        self.assertEqual(len(_valid_keen.adapters), 2)

    def test_keen_config(self):
        """ Test :py:attr:`Keen.config`, which exposes
            ``Keen``-related provider config listed in
            *importer's* ``config.json``. """
        _keen_provider = self._valid_keen_provider(instance=True)
        self.assertIsInstance(_keen_provider.config, dict)
        self.assertEqual(_keen_provider.config['read_key'], '__read_key__')
        self.assertEqual(_keen_provider.config['write_key'], '__write_key__')
        self.assertEqual(_keen_provider.config['project_id'], '__project_id__')

    def test_keen_key_methods(self):
        """ Test utility methods exposed on :py:class:`Keen`
            that allow direct API users to change/set
            their config values (``project_id``, ``read_key``,
            and ``write_key``) in-flight. """
        _keen_provider = self._valid_keen_provider(instance=True)
        self.assertEqual(_keen_provider.read_key, _keen_provider.config['read_key'])
        self.assertEqual(_keen_provider.write_key, _keen_provider.config['write_key'])
        self.assertEqual(_keen_provider.project_id, _keen_provider.config['project_id'])
        self.assertEqual(_keen_provider._get_read_key(), _keen_provider.config['read_key'])
        self.assertEqual(_keen_provider._get_write_key(), _keen_provider.config['write_key'])
        self.assertEqual(_keen_provider._get_project_id(), _keen_provider.config['project_id'])
        _keen_provider.project_id = 'supguyz'
        self.assertEqual(_keen_provider.project_id, 'supguyz')
        self.assertEqual(_keen_provider.config['project_id'], 'supguyz')
        _keen_provider.read_key = 'readkey_sample'
        self.assertEqual(_keen_provider.read_key, 'readkey_sample')
        self.assertEqual(_keen_provider.config['read_key'], 'readkey_sample')
        _keen_provider.write_key = 'writekey_sample'
        self.assertEqual(_keen_provider.write_key, 'writekey_sample')
        self.assertEqual(_keen_provider.config['write_key'], 'writekey_sample')
        _keen_provider._set_project_id('supguyz2')
        self.assertEqual(_keen_provider.project_id, 'supguyz2')
        self.assertEqual(_keen_provider.config['project_id'], 'supguyz2')
        _keen_provider._set_read_key('readkey_sample2')
        self.assertEqual(_keen_provider.read_key, 'readkey_sample2')
        self.assertEqual(_keen_provider.config['read_key'], 'readkey_sample2')
        _keen_provider._set_write_key('writekey_sample2')
        self.assertEqual(_keen_provider.write_key, 'writekey_sample2')
        self.assertEqual(_keen_provider.config['write_key'], 'writekey_sample2')
        with self.assertRaises(ValueError):
            _keen_provider._set_config('invalid_config', True)


class KeenUploaderTests(KeenTests):
    """ Tests the ``Keen`` uploader class, which is
        exposed at :py:class:`mix.KeenUploader`. """

    def test_keen_upload(self):
        """ Test the :py:meth:`upload` method on the uploader
            for ``Keen``, exposed at :py:class:`mix.KeenUploader`. """
        _keen_provider = self._valid_keen_provider(instance=True)
        uploader = _keen_provider.uploader
        c_uploader = _keen_provider.uploader
        self.assertEqual(uploader, c_uploader)
        _keen_provider.uploader.events_by_kind = {}
        event_1 = (
         'sample_kind', {'blab': True}, None)
        event_2 = ('sample_kind', {'bleebs': True}, mix.timezone('UTC').localize(datetime.datetime.fromtimestamp(random.randint(1377605000, 1377895000))))
        event_3 = ('sample_kind2', {'blops': True}, mix.timezone('UTC').localize(datetime.datetime.now()))
        for kind, event, timestamp in (event_1, event_2, event_3):
            _keen_provider.uploader.upload(kind, json.dumps(event), timestamp if timestamp is not None else None)

        self.assertTrue('sample_kind' in _keen_provider.uploader.events_by_kind)
        self.assertTrue('sample_kind2' in _keen_provider.uploader.events_by_kind)
        self.assertEqual(len(_keen_provider.uploader.events_by_kind['sample_kind']), 2)
        self.assertEqual(len(_keen_provider.uploader.events_by_kind['sample_kind2']), 1)
        return

    def test_keen_upload_commit(self):
        """ Test the :py:meth:`commit` method on the uploader
            for ``Keen``, exposed at :py:class:`mix.KeenUploader`. """
        _keen_provider = self._valid_keen_provider(instance=True)
        _keen_provider.uploader.events_by_kind = {}
        event_1 = (
         'sample_kind', {'blab': True}, None)
        event_2 = ('sample_kind', {'bleebs': True}, mix.timezone('UTC').localize(datetime.datetime.fromtimestamp(random.randint(1377605000, 1377895000))))
        event_3 = ('sample_kind2', {'blops': True}, mix.timezone('UTC').localize(datetime.datetime.now()))
        for kind, event, timestamp in (event_1, event_2, event_3):
            _keen_provider.uploader.upload(kind, json.dumps(event), timestamp if timestamp is not None else None)

        count = _keen_provider.uploader.commit()
        self.assertEqual(count, 3)
        self.assertIsInstance(_keen_provider.lib.events_cache, dict)
        self.assertTrue('sample_kind' in _keen_provider.lib.events_cache)
        self.assertTrue('sample_kind2' in _keen_provider.lib.events_cache)
        self.assertEqual(len(_keen_provider.lib.events_cache['sample_kind']), 2)
        self.assertEqual(len(_keen_provider.lib.events_cache['sample_kind2']), 1)
        return


class KeenDownloaderTests(KeenTests):
    """ Tests the ``Keen`` downloader class, which is
        exposed at :py;class:`mix.KeenDownloader`. """

    def test_keen_download(self):
        """ Test the :py:meth:`upload` method on the downloader
            for ``Keen``, exposed at :py:class:`mix.KeenUploader`. """
        _keen_provider = self._valid_keen_provider(instance=True)
        downloader = _keen_provider.downloader
        c_downloader = _keen_provider.downloader
        self.assertEqual(downloader, c_downloader)
        start, end = datetime.datetime(year=2013, month=8, day=20, hour=12, minute=0, second=0), datetime.datetime(year=2013, month=8, day=30, hour=12, minute=0, second=0)
        events = []
        for kind, deserialized, timestamp in _keen_provider.downloader.download(start, end, ['sample_kind']):
            self.assertIsInstance(kind, basestring)
            self.assertIsInstance(deserialized, dict)
            self.assertIsInstance(timestamp, datetime.datetime)
            self.assertEqual(kind, 'sample_kind')
            events.append((kind, deserialized, timestamp))

        self.assertEqual(len(events), 2)