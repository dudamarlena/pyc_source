# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: apps/example/webapp/controller/webservice.py
# Compiled at: 2011-03-24 03:59:28
from chula import webservice
from chula.www.controller import base

class Webservice(base.Controller):

    @webservice.expose(transport='ASCII')
    def ascii(self):
        return {'some': 'payload'}

    @webservice.expose()
    def broken(self):
        return 0 / 0

    @webservice.expose(transport='PICKLE')
    def pickle(self):
        return {'some': 'payload'}

    @webservice.expose()
    def simple_json(self):
        return {'some': 'payload'}

    @webservice.expose(x_header=True)
    def xjson(self):
        return {'some': 'payload'}