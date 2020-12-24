# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge/jet_bridge/handlers/not_found.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 224 bytes
import tornado.web

class NotFoundHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.set_status(404)
        self.render('404.html', **{'path': self.request.path})