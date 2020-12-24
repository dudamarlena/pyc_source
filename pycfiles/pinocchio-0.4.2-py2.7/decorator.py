# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pinocchio/decorator.py
# Compiled at: 2014-11-12 05:59:14
"""
decorator extension for 'nose'.

Allows you to decorate functions, classes, and methods with attributes
without modifying the actual source code.  Particularly useful in
conjunction with the 'attrib' extension package.
"""
import sys
err = sys.stderr
import logging, os
from nose.plugins.base import Plugin
log = logging.getLogger(__name__)

def sort_plugins_by_priority(a, b):
    pa = getattr(a, 'call_priority', 100)
    pb = getattr(b, 'call_priority', 100)
    return cmp(pa, pb)


class Decorator(Plugin):
    call_priority = -100

    def __init__(self):
        Plugin.__init__(self)

    def add_options(self, parser, env=os.environ):
        parser.add_option('--decorator-file', action='store', dest='decorator_file', default=None, help='Apply attributes in this file to matching functions, classes, and methods')
        return

    def configure(self, options, config):
        self.conf = config
        logger = logging.getLogger(__name__)
        logger.propagate = 0
        handler = logging.StreamHandler(err)
        logger.addHandler(handler)
        lvl = logging.WARNING
        if options.verbosity >= 5:
            lvl = 0
        elif options.verbosity >= 4:
            lvl = logging.DEBUG
        elif options.verbosity >= 3:
            lvl = logging.INFO
        logger.setLevel(lvl)
        if options.decorator_file:
            self.enabled = True
            self.decorator_file = options.decorator_file

    def begin(self):
        """
        Called before any tests are run.

        The only trick here is that we have to mangle the order of
        the plugins, because this plugin *must* be called before
        any plugins that examine the attributes being set.  This is
        done by sorting the plugins in-place.
        """
        self.conf.plugins.sort(sort_plugins_by_priority)
        filename = self.decorator_file
        fp = open(filename)
        curtains = {}
        for line in fp:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, attrib = line.split(':')
            name = name.strip()
            attrib = attrib.strip()
            l = curtains.get(name, [])
            l.append(attrib)
            curtains[name] = l

        self.curtains = curtains

    def wantClass(self, cls):
        """
        wantClass -- attach matching attributes to the class.
        """
        fullname = '%s.%s' % (cls.__module__, cls.__name__)
        self._attach_attributes(fullname, cls)
        return

    def wantMethod(self, method):
        """
        wantMethod -- attach matching attributes to this method.
        """
        fullname = '%s.%s.%s' % (method.__module__,
         method.__self__.__class__.__name__,
         method.__name__)
        self._attach_attributes(fullname, method)
        return

    def wantFunction(self, func):
        """
        wantFunction -- attach matching attributes to this function.
        """
        fullname = '%s.%s' % (func.__module__,
         func.__name__)
        self._attach_attributes(fullname, func)
        return

    def _attach_attributes(self, fullname, obj):
        """
        Attach attributes matching 'fullname' to the object 'obj'.
        """
        attribs = self.curtains.get(fullname, [])
        log.info('_attach_attributes: %s, %s' % (fullname, attribs))
        for a in attribs:
            obj.__dict__[a] = True