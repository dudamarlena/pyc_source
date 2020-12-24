# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/logger.py
# Compiled at: 2018-07-11 18:15:31
import io, logging, os, tempfile
from south.tests import unittest
import sys
from django.conf import settings
from django.db import connection, models
from south.db import db
from south.logger import close_logger

class TestLogger(unittest.TestCase):
    """
    Tests if the logging is working reasonably. Some tests ignored if you don't
    have write permission to the disk.
    """

    def setUp(self):
        db.debug = False
        self.test_path = tempfile.mkstemp(suffix='.south.log')[1]

    def test_db_execute_logging_nofile(self):
        """Does logging degrade nicely if SOUTH_LOGGING_ON not set?"""
        settings.SOUTH_LOGGING_ON = False
        db.create_table('test9', [('email_confirmed', models.BooleanField(default=False))])

    def test_db_execute_logging_off_with_basic_config(self):
        """
        Does the south logger avoid outputing debug information with
        south logging turned off and python logging configured with
        a basic config?"
        """
        settings.SOUTH_LOGGING_ON = False
        logging_stream = io.StringIO()
        logging.basicConfig(stream=logging_stream, level=logging.WARNING)
        db.create_table('test12', [('email_confirmed', models.BooleanField(default=False))])
        self.assertEqual(logging_stream.getvalue(), '')

    def test_db_execute_logging_validfile(self):
        """Does logging work when passing in a valid file?"""
        settings.SOUTH_LOGGING_ON = True
        settings.SOUTH_LOGGING_FILE = self.test_path
        try:
            fh = open(self.test_path, 'w')
        except IOError:
            return

        fh.close()
        db.create_table('test10', [('email_confirmed', models.BooleanField(default=False))])
        close_logger()
        try:
            os.remove(self.test_path)
        except:
            pass

    def test_db_execute_logging_missingfilename(self):
        """Does logging raise an error if there is a missing filename?"""
        settings.SOUTH_LOGGING_ON = True
        settings.SOUTH_LOGGING_FILE = None
        self.assertRaises(IOError, db.create_table, 'test11', [
         (
          'email_confirmed', models.BooleanField(default=False))])
        return