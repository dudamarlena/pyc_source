# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/projects/gap/.venv/lib/python2.7/site-packages/gap/templates/src/routes.py
# Compiled at: 2013-10-11 03:16:02
import webapp2, config
from gap.utils.routes import include
routes = (
 ('/', 'gap.views.welcome_screen'),
 ('/.*', 'gap.views.not_found'))