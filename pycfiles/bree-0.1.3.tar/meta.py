# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/GDrive/Codes/ez/bree/bree/pagelets/meta.py
# Compiled at: 2015-01-24 09:45:18
from tornado.web import UIModule

class Meta(UIModule):

    def render(self, title='', desc='', keywords='', copyleft='', author='', icon='/static/favicon.ico', *args, **kwargs):
        buff = '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'
        buff += ('<title>{}</title>').format(title)
        buff += ('<meta name="description" content="{}">').format(desc)
        buff += ('<meta name="keywords" content="{}">').format(keywords)
        buff += ('<meta name="author" content="{}">').format(author)
        buff += ('<meta name="copyright" content="{}">').format(copyleft)
        buff += ('<link rel="icon" href="{}">').format(icon)
        return buff