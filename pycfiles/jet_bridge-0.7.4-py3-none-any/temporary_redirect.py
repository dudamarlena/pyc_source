# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge/jet_bridge/handlers/temporary_redirect.py
# Compiled at: 2019-10-12 10:12:14
from tornado.web import RedirectHandler

class TemporaryRedirectHandler(RedirectHandler):

    def initialize(self, url):
        super(TemporaryRedirectHandler, self).initialize(url, False)