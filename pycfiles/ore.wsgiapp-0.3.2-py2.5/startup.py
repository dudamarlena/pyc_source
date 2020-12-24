# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/startup.py
# Compiled at: 2008-05-01 10:27:18
"""
$Id: $
"""
import os, sys, code, zope.app.wsgi, zope.app.debug, wsgi

def application_factory(global_conf, zcml='site.zcml', devmode='off'):
    zcml_conf = os.path.join(global_conf['here'], zcml)
    devmode = devmode.lower() in ('true', 'True', 'on') and True or False
    return wsgi.getWSGIApplication(zcml_conf, devmode)