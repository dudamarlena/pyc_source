# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/hejtado/quido/api/endpoints/thermometers.py
# Compiled at: 2019-10-15 17:49:52
# Size of source mod 2**32: 1337 bytes
import logging
from flask_restplus import Resource, fields
import hejtado.quido.api as api
from hejtado.quido.business import Quido
log = logging.getLogger(__name__)
ns = api.namespace('quido/thermometers', description='Operations with Quido thermometer(s)')
thermometers = api.model('Quido Thermometer', {'id':fields.Integer(readonly=True, description='The Quido Thermometer unique identifier'), 
 'name':fields.String(required=True, description='The Thermometer name'), 
 'temperature':fields.String(required=True, description='Temperature measured by Thermometer')})
quido = Quido()

@ns.route('/')
class QuidoThermometer(Resource):
    __doc__ = '\n    List the available Quido thermometers\n    '

    @ns.doc('list_quido_thermometers')
    @ns.marshal_list_with(thermometers)
    def get(self):
        """
        Get all thermometers and return them as list of dictionaries
        :return: List of available thermometers
        """
        boiler_temperature = quido.get_boiler_temperature()
        log.info('Temperature of the boiler is: {}'.format(boiler_temperature))
        return [
         {'id':1, 
          'name':'boiler',  'temperature':boiler_temperature}]