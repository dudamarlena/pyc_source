# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/warmup.py
# Compiled at: 2012-06-22 10:46:07
import env_setup
env_setup.setup()
from webapp2 import WSGIApplication, RequestHandler, Route
from agar.env import on_production_server

class WarmupHandler(RequestHandler):

    def get(self):
        self.response.out.write('Warmed Up')


application = WSGIApplication([
 Route('/_ah/warmup', WarmupHandler, name='warmup')], debug=not on_production_server)