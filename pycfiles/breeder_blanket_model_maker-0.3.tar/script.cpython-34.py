# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/breezekay/GDrive/Codes/ez/bree/bree/pagelets/script.py
# Compiled at: 2015-01-24 09:45:18
# Size of source mod 2**32: 726 bytes
from __future__ import unicode_literals
from tornado.web import UIModule

class Script(UIModule):

    def render(self, origin, compress=None, *args, **kwargs):
        debug = self.handler.js_debug
        to_show = []
        buff = ''
        if debug or compress is None:
            if isinstance(origin, str):
                to_show = [
                 origin]
            else:
                to_show = origin
        else:
            if isinstance(compress, str):
                to_show = [
                 compress]
            else:
                to_show = compress
        for v in to_show:
            buff += '<script src="{}"></script>'.format(self.handler.static_url(v))

        return buff