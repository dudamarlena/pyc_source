# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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