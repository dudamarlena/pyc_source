# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/GDrive/Codes/ez/bree/bree/pagelets/css.py
# Compiled at: 2015-01-24 09:45:18
# Size of source mod 2**32: 764 bytes
from __future__ import unicode_literals
from tornado.web import UIModule

class CSS(UIModule):

    def render(self, origin, compress=None, *args, **kwargs):
        debug = self.handler.css_debug
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
        for i in to_show:
            buff += '<link href="{}" media="screen" rel="stylesheet" type="text/css">'.format(self.handler.static_url(i))

        return buff