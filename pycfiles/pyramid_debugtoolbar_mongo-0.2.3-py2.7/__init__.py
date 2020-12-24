# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/pyramid_debugtoolbar_mongo/__init__.py
# Compiled at: 2014-12-29 21:12:57
from pyramid.settings import asbool
__author__ = 'gillesdevaux'

def includeme(config):
    stack_trace = asbool(config.registry.settings.get('debugtoolbarmongo.stacktrace', True))
    config.registry.settings['debugtoolbarmongo.stacktrace'] = stack_trace