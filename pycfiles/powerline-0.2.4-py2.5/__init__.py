# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/powerline/__init__.py
# Compiled at: 2008-04-11 18:06:43
from __future__ import absolute_import
import cherrypy
from os import path

class user_error(Exception):
    pass


from powerline import json, web, database
location = path.abspath(path.dirname(__file__))
web.template_dir = path.join(location, 'templates')
from powerline import manager, xmlrpc
cherrypy.config.namespaces.update(database=lambda k, v: setattr(database, k, v), output=lambda k, v: setattr(output, k, v))
__all__ = [
 'location', 'output', 'web', 'database', 'json', 'manager', 'xmlrpc']