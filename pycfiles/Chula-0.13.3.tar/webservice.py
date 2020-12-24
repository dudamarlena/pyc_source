# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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