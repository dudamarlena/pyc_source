# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/static/main.py
# Compiled at: 2014-04-20 17:43:59
import controllers
from lib.server import webapp_enhanced
app = webapp_enhanced()
app.route(controllers.all_classes())
app.start()