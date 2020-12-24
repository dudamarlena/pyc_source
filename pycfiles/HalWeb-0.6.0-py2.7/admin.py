# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/apps/admin.py
# Compiled at: 2012-01-05 21:48:33
import conf.settings as settings
from imports import *
from google.appengine.ext import webapp
application = webapp.WSGIApplication(webapphandlers, debug=settings.DEBUG)
if __name__ == '__main__':
    runapp(application)