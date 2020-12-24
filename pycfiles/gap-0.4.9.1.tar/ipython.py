# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/projects/gap/.venv/lib/python2.7/site-packages/gap/templates/bin/ipython.py
# Compiled at: 2013-10-11 03:16:02
import sys
from os.path import dirname, realpath, join
import IPython
from gap.utils.setup import fix_sys_path, setup_testbed, setup_stubs
app_path = join(realpath(dirname(dirname(__file__))), 'src')
fix_sys_path(app_path)
TESTBED = setup_testbed()
from google.appengine.api.urlfetch import fetch
from google.appengine.ext import db, ndb
from google.appengine.api import memcache
IPython.embed()