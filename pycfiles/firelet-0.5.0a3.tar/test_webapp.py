# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/projects/firelet/test/test_webapp.py
# Compiled at: 2012-05-18 18:48:18
from logging import getLogger
from nose.tools import raises, assert_raises, with_setup
from webtest import TestApp, AppError
import os
log = getLogger(__name__)
deb = log.debug
from testingutils import setup_dir, teardown_dir
from firelet import fireletd
REDIR = '302 Found'
app = None
tmpdir = None
orig_dir = None

def setup():
    global app
    setup_dir()
    app = TestApp(fireletd.app)


def teardown():
    teardown_dir()
    app = None
    return


@raises(AppError)
def test_bogus_page():
    app.get('/bogus_page')


def test_index_page():
    assert app.get('/').status == '200 OK'


def login():
    """run setup_app and log in"""
    setup_app()
    p = app.post('/login', {'user': 'admin', 'pwd': 'admin'})