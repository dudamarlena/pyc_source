# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahnve/.virtualenvs/blog/lib/python2.7/site-packages/test/test_config.py
# Compiled at: 2015-02-14 19:14:47
from nose.tools import assert_equals
from sinor.config import config
from mock import Mock

def test_empty_feed_title():
    config.load_toml_file = Mock(return_value={'build': {}})
    config.blog_title = Mock(return_value='foo')
    assert_equals(config.feed_title(), 'foo')


def test_empty_partials_dir():
    config.load_toml_file = Mock(return_value={'build': {}})
    assert_equals(config.build_partials_dir(), '')