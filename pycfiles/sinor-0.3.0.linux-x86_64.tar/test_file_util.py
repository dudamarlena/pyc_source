# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/test/test_file_util.py
# Compiled at: 2015-02-14 19:12:24
from sinor.file_util import relative_href_for_file
from nose.tools import assert_equals
from sinor.config import config
from mock import Mock
import os

def test_href_for_file():
    config.build_output_dir = Mock(return_value='build')
    config.blog_base_dir = Mock(return_value='blog')
    os.getcwd = Mock(return_value='/home/foo')
    assert_equals(relative_href_for_file('/home/foo/build/blog/2014/blog.html'), '/blog/2014/blog.html')