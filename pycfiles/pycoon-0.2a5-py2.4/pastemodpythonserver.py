# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\wsgi\frontend\pastemodpythonserver.py
# Compiled at: 2006-12-08 05:04:41
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
import sys, os
from mod_python import apache
from pycoon.wsgi.servers.paste.modpython import Handler
from pycoon import wsgi

def handler(req):
    options = req.get_options()
    pycoon = wsgi.pycoonFactory({'server-xconf': options['config']})
    Handler(req).run(pycoon)
    return apache.OK