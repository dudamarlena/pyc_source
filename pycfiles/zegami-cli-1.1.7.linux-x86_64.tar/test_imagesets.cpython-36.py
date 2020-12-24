# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/tests/test_imagesets.py
# Compiled at: 2018-05-22 09:29:16
# Size of source mod 2**32: 1118 bytes
"""Imageset tests."""
from . import HTTPBaseTestCase
from .. import imagesets

class ImagesetTestCase(HTTPBaseTestCase):

    def test_update_to_url_imageset(self):
        session = self.make_session(200, {'imageset': {'test': 'data'}})
        ims_url = 'test:my-test'
        configuration = {'dataset_column':'foo', 
         'dataset_id':'my ds id'}
        exp_imageset = {'name':'Imageset created by CLI', 
         'source':{'dataset_id':'my ds id', 
          'transfer':{'url': {'dataset_column': 'foo'}}}}
        imagesets._update_to_url_imageset(session, configuration, ims_url)
        self.assertEqual(session.adapters['test:'].log, [
         (
          'PUT',
          'test:my-test',
          exp_imageset,
          'application/json')])