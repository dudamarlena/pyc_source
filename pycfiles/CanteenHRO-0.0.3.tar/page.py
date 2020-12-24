# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/base/page.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  page base\n  ~~~~~~~~~\n\n  ``Page``s represnt the simplest way to respond to an HTTP request in Canteen.\n  They are inherently bound to HTTP, in that you specify methods directly from\n  the HTTP spec to be executed when the corresponding method is requested.\n\n  Example:\n\n    # -*- coding: utf-8 -*-\n    from canteen import url, Page\n\n    @url('/')\n    class Home(Page):\n\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
from . import handler

class Page(handler.Handler):
    """ Extendable class exposed to developers to prepare a class that responds to
      particular HTTP requests. Great way to return static content or render
      templates, as ``Page``s come preconfigured for use with :py:mod:`Jinja2`
      and Canteen's builtin logic (session, static asset and caching tools). """
    __owner__ = 'Page'