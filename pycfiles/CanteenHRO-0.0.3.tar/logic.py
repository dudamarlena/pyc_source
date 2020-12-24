# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/base/logic.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  logic base\n  ~~~~~~~~~~\n\n  Provides base configuration and code to setup Canteen ``Logic`` classes, which\n  allow a developer to provide a piece of cross-cutting functionality to their\n  entire application.\n\n  ``Logic`` classes are Canteen ``Component``s, meaning they provide injectable\n  structures for the DI engine. ``Logic`` classes, when bound to a string name\n  with ``decorators.bind``, will be accessible from ``Compound`` object methods\n  at ``self.name``.\n\n  Example:\n\n    # -*- coding: utf-8 -*-\n    from canteen import decorators, Logic\n\n    @decorators.bind('math')\n    class Math(Logic):\n\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
from ..core import meta
from ..util import decorators

@decorators.singleton
class Logic(object):
    """ Base class for Canteen ``Logic`` components. Specifies a class tree on the
      ``Proxy.Component`` side (meaning that it *provides* DI resources, instead
      of a ``Proxy.Compound``, which *consumes* them).

      ``Logic`` classes must be bound using the ``decorators.bind`` tool, which
      takes a ``str`` name and binds a ``Logic`` class (or child) to that name
      on all ``Compound`` classes and objects. """
    __owner__, __metaclass__ = 'Logic', meta.Proxy.Component