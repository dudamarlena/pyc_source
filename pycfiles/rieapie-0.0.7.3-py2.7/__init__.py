# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rieapie/__init__.py
# Compiled at: 2013-08-12 07:55:04
"""
"""
version = '0.0.7.3'
try:
    from rieapie.trickery import Api, pre_request, post_request
    import rieapie.wrappers
except ImportError as e:
    print 'error initializing rieapie'