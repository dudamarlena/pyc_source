# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/hejtado/quido/api/endpoints/relays.py
# Compiled at: 2019-10-24 03:50:58
# Size of source mod 2**32: 2874 bytes
import logging
from flask import request
from flask_restplus import Resource, fields
import hejtado.quido.api as api
from hejtado.quido.business import Quido
log = logging.getLogger(__name__)
ns = api.namespace('quido/relays', description='Operations with Quido relays')
relays = api.model('Quido Relays', {'id':fields.Integer(readonly=True, description='The Quido Relay unique identifier'), 
 'name':fields.String(required=True, description='The relay name'), 
 'status':fields.String(required=False, description='Status of the relay (on/off)'), 
 'type':fields.String(required=False, description='Type of the output')})
QUIDO_RELAYS = {1:'prodluzovacka', 
 2:'reset-ling', 
 3:'tepla-voda'}
quido = Quido()

@ns.route('/')
class QuidoRelay(Resource):
    __doc__ = '\n    List the available Quido relays\n    '

    @ns.doc('list_quido_relays')
    @ns.marshal_list_with(relays)
    def get(self):
        """
        Get all relays and return them as list of dictionaries
        :return: List of available relays
        """
        return [{'id':relay_id,  'name':name} for relay_id, name in QUIDO_RELAYS.items()]


@ns.route('/<int:relay_id>')
class QuidoRelayItem(Resource):
    __doc__ = '\n    Get/Set the values on Quido Relay\n    '

    @ns.doc('get_quido_relay_values')
    @ns.marshal_with(relays)
    def get(self, relay_id):
        """
        Fetch a information about relay
        :param relay_id: ID of the Relay
        :return: Return information about relay
        """
        status = int(quido.get_relay_status(relay_id))
        if not status:
            status = 'off'
        else:
            status = 'on'
        log.debug('squido get relay status is "{}"'.format(status))
        name = quido.get_relay_name(relay_id)
        log.debug('squido get relay name is "{}"'.format(name))
        relay_type = quido.get_relay_type(relay_id)
        log.debug('squido get relay type is "{}"'.format(relay_type))
        relay_values = {'id':relay_id,  'name':name,  'status':status,  'type':relay_type}
        log.info('Relay values: {}'.format(relay_values))
        return [
         relay_values]

    @ns.doc('set_quido_relays_values')
    @api.expect(relays)
    @api.response(204, 'Relay successfully updated.')
    def put(self, relay_id):
        """
        Set the new status of the relay
        :param relay_id: ID of the relay
        :return: current relay status
        """
        data = request.json
        log.debug('QuidoRelayItem put received request {}'.format(data))
        status = data['status']
        quido.set_relay(relay_id, status)
        return (None, 204)