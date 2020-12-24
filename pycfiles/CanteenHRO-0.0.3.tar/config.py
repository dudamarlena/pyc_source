# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/util/config.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  config utils\n  ~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import os, importlib
_appconfig = {}

class Config(object):
    """  """
    __dev__ = None
    seen = set()
    wrap = None
    blocks = None

    def __init__(self, sub=None, **blocks):
        """  """
        global _appconfig
        self.blocks = blocks or _appconfig
        if not _appconfig:
            _appconfig = blocks
        self.wrap = sub

    app = property(lambda self: self.blocks.get('app', {'debug', True}))
    assets = property(lambda self: self.blocks.get('assets', {'debug': True}))
    config = property(lambda self: self.blocks.get('config', {}))
    debug = lambda self: any((self.__dev__,
     os.environ.get('SERVER_SOFTWARE', 'Not Dev').startswith('Dev'),
     os.environ.get('CANTEEN_DEBUG', False) in ('1', 'yes', 'on', 'true', 'sure', 'whynot'),
     self.config.get('debug', False),
     self.app.get('debug', False),
     __debug__))
    app_version = lambda self: '0.0.1-alpha' if 'version' not in self.app else ('-').join((('.').join(map(str, self.app['version'].values()[:3])),
     str(self.app['version']['release'])))
    load = lambda self, path: self.merge(importlib.import_module(path).config.blocks)
    __get__ = lambda self, instance, owner: self.wrap or self.blocks

    def get(self, key, default=None):
        """  """
        if self.blocks:
            if 'config' in self.blocks:
                return self.blocks['config'].get(key, {'debug': True})
            return self.blocks.get(key, default)
        return default