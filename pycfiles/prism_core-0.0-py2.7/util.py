# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_core/util.py
# Compiled at: 2014-01-03 23:42:57
import logging
from pyramid.threadlocal import get_current_registry
log = logging.getLogger('prism.core.util')

class AttrDict(dict):
    """
    Dictionary implementation that lets you refer to dictionary keys as
    normal attributes.
    """
    __slots__ = ()

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return dict.__getattr__(self, attr)
        if attr in self:
            return self.__getitem__(attr)
        raise AttributeError

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            return dict.__setattr__(self, attr, value)
        else:
            return self.__setitem__(attr, value)


def prism_settings(key=None, default=None):
    settings = get_current_registry().settings
    if key:
        value = settings.get('prism.%s' % key, default)
        if value == 'true':
            return True
        if value == 'false':
            return False
        return value
    else:
        return dict((x.split('.', 1)[1], y) for x, y in settings.iteritems() if x.startswith('prism.'))