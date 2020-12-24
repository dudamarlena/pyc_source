# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./scripts/../apps/example/webapp/controller/sample.py
# Compiled at: 2011-03-19 21:05:04
from chula import webservice
from chula.www import controller

class Sample(controller.Controller):

    def index(self):
        return 'Sample controller'

    def page(self):
        return 'Sample controller:page'

    @webservice.expose()
    def webservice(self):
        return {'color': 'red', 'features': [1, 2, 3, None, 'abc']}