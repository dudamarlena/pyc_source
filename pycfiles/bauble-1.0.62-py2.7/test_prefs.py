# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/test/test_prefs.py
# Compiled at: 2016-10-03 09:39:22
import logging
logger = logging.getLogger(__name__)
from bauble.test import BaubleTestCase
from bauble import prefs
from tempfile import mkstemp
from bauble import version_tuple
prefs.testing = True

class PreferencesTests(BaubleTestCase):

    def test_create_does_not_save(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        with open(pname) as (f):
            self.assertEquals(f.read(), '')

    def test_assert_initial_values(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertTrue(prefs.config_version_pref in p)
        self.assertTrue(prefs.picture_root_pref in p)
        self.assertTrue(prefs.date_format_pref in p)
        self.assertTrue(prefs.parse_dayfirst_pref in p)
        self.assertTrue(prefs.parse_yearfirst_pref in p)
        self.assertTrue(prefs.units_pref in p)
        self.assertEquals(p[prefs.config_version_pref], version_tuple[:2])
        self.assertEquals(p[prefs.picture_root_pref], '')
        self.assertEquals(p[prefs.date_format_pref], '%d-%m-%Y')
        self.assertEquals(p[prefs.parse_dayfirst_pref], True)
        self.assertEquals(p[prefs.parse_yearfirst_pref], False)
        self.assertEquals(p[prefs.units_pref], 'metric')

    def test_not_saved_while_testing(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        p.save()
        with open(pname) as (f):
            self.assertEquals(f.read(), '')

    def test_can_force_save(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        p.save(force=True)
        with open(pname) as (f):
            self.assertFalse(f.read() == '')

    def test_get_does_not_store_values(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertFalse('not_there_yet.1' in p)
        self.assertIsNone(p['not_there_yet.1'])
        self.assertEquals(p.get('not_there_yet.2', 33), 33)
        self.assertIsNone(p.get('not_there_yet.3', None))
        self.assertFalse('not_there_yet.1' in p)
        self.assertFalse('not_there_yet.2' in p)
        self.assertFalse('not_there_yet.3' in p)
        self.assertFalse('not_there_yet.4' in p)
        return

    def test_use___setitem___to_store_value_and_create_section(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertFalse('test.not_there_yet-1' in p)
        p['test.not_there_yet-1'] = 'all is a ball'
        self.assertTrue('test.not_there_yet-1' in p)
        self.assertEquals(p['test.not_there_yet-1'], 'all is a ball')
        self.assertEquals(p.get('test.not_there_yet-1', 33), 'all is a ball')

    def test_most_values_converted_to_string(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertFalse('test.not_there_yet-1' in p)
        p['test.not_there_yet-1'] = 1
        self.assertTrue('test.not_there_yet-1' in p)
        self.assertEquals(p['test.not_there_yet-1'], '1')
        p['test.not_there_yet-3'] = None
        self.assertEquals(p['test.not_there_yet-3'], 'None')
        return

    def test_boolean_values_stay_boolean(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertFalse('test.not_there_yet-1' in p)
        p['test.not_there_yet-1'] = True
        self.assertEquals(p['test.not_there_yet-1'], True)
        p['test.not_there_yet-2'] = False
        self.assertEquals(p['test.not_there_yet-2'], False)

    def test_saved_dictionary_like_ini_file(self):
        handle, pname = mkstemp(suffix='.dict')
        p = prefs._prefs(pname)
        p.init()
        self.assertFalse('test.not_there_yet-1' in p)
        p['test.not_there_yet-1'] = 1
        self.assertTrue('test.not_there_yet-1' in p)
        p.save(force=True)
        with open(pname) as (f):
            content = f.read()
            self.assertTrue(content.index('not_there_yet-1 = 1') > 0)
            self.assertTrue(content.index('[test]') > 0)