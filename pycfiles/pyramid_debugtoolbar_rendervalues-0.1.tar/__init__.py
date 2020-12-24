# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/pyramid_debugtoolbar_mongo/__init__.py
# Compiled at: 2014-12-29 21:12:57
from pyramid.settings import asbool
__author__ = 'gillesdevaux'

def includeme(config):
    stack_trace = asbool(config.registry.settings.get('debugtoolbarmongo.stacktrace', True))
    config.registry.settings['debugtoolbarmongo.stacktrace'] = stack_trace