# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_streamer.py
# Compiled at: 2018-10-15 23:12:48
import unittest, os, logging, sure, sys, inspect, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
from zas_rep_tools.src.classes.streamer import Streamer
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.test_helpers import exit_after
from zas_rep_tools.src.utils.basetester import BaseTester

class TestZASStreamerStreamer(BaseTester, unittest.TestCase):
    _multiprocess_shared_ = True

    def setUp(self):
        super(type(self), self).setUp()
        self._path_to_zas_rep_tools = os.path.dirname(os.path.dirname(os.path.dirname(inspect.getfile(Streamer))))
        self.test_consumer_key = '97qaczWSRfaaGVhKS6PGHSYXh'
        self.test_consumer_secret = 'mWUhEL0MiJh7FqNlOkQG8rAbC8AYs4YiEOzdiCwx26or1oxivc'
        self.test_access_token = '1001080557130932224-qi6FxuYwtvpbae17kCjAS9kfL8taNT'
        self.test_access_token_secret = 'jCu2tTVwUW77gzOtK9X9svbdKUFvlSzAo4JfIG8tVuSgX'

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_streamer_initialisation_000(self):
        self.prj_folder()
        stream = Streamer(self.test_consumer_key, self.test_consumer_secret, self.test_access_token, self.test_access_token_secret, self.tempdir_project_folder, language='de', mode=self.mode)
        assert isinstance(stream, Streamer)

    @attr(status='stable')
    def test_stream_twitter_500(self):
        self.prj_folder()
        stream = Streamer(self.test_consumer_key, self.test_consumer_secret, self.test_access_token, self.test_access_token_secret, self.tempdir_project_folder, logger_usage=False, language='de', mode=self.mode)
        try:

            @exit_after(5)
            def run_streamer():
                stream.stream_twitter()

            run_streamer()
        except SystemExit:
            assert True
        except Exception as e:
            print "!!!!!!!!!\n!!!!!!!!!\n If you have problem with this Test, probably the test Twitter Credentials was changed. Try to reinstall this package or set your own Twitter initials in the following Test File: 'test_zas_rep_tools_streamer.py'.!!!!!!!!!\n!!!!!!!!!\n "
            p(e, 'ERROR', c='r')