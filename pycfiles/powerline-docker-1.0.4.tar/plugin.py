# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/powerline/lib/plugin.py
# Compiled at: 2008-04-11 16:31:10
from os import path, listdir
from cherrypy import log
import imp

class mount_point(type):
    known = set()

    def __init__(cls, name, bases, attrs):
        if hasattr(cls, '_plugins'):
            cls.add(cls)
        else:
            cls._plugins = set()
            if 'add' not in attrs:
                cls.add = classmethod(lambda cls, plugin: cls.plugins.add(plugin))
                cls.plugins = cls._plugins
            mount_point.known.add(cls)


def load(*paths):
    for path in paths:
        load_path(path)


def load_path(location):
    for file in set([ path.splitext(x)[0] for x in listdir(location) if not x.startswith('.') ]):
        load_file(location, file)


def load_file(location, filename):
    found = []
    mod_name = path.splitext(filename)[0]
    new_mod = None
    try:
        (fp, pathname, desc) = imp.find_module(mod_name, [location])
        try:
            new_mod = imp.load_module(mod_name, fp, pathname, desc)
        finally:
            if fp:
                fp.close()

    except ImportError, err:
        log('Failed to import %s, %s' % (mod_name, err))

    return