# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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