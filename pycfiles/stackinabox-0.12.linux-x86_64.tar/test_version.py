# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmeyer/Devel/stackInABox/.tox/twine/lib/python2.7/site-packages/stackinabox/tests/test_version.py
# Compiled at: 2017-05-27 01:24:11
import os, unittest, stackinabox

class TestVersionMatch(unittest.TestCase):

    def setUp(self):
        super(TestVersionMatch, self).setUp()

    def tearDown(self):
        super(TestVersionMatch, self).tearDown()

    def test_version_match(self):
        version_source = ('{0}.{1}').format(stackinabox.version[0], stackinabox.version[1])
        version_setup = None
        with open('../setup.py', 'rt') as (input_data):
            for line in input_data:
                ln = line.strip()
                if ln.startswith('version='):
                    l = ln.replace("'", '', 2).replace(',', '')
                    version_setup = l.split('=')[1]
                    break

        self.assertEqual(version_source, version_setup)
        return