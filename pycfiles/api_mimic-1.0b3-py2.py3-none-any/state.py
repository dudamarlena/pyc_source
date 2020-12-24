# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/views/state.py
# Compiled at: 2019-02-06 12:21:52
from flask import request
from flask_classy import route
from ocs.api import exports
from ocs.api.validators import Validator
from ocs.conf import get_config
from voluptuous import All, Length, Schema
from . import MetadataAPIBaseView
from . import CONFIGURATION_NAME

class StateViewValidator(Validator):

    def validate_put(self, view):
        self.test_post_data(Schema({'state_detail': All(unicode, Length(min=0, max=128))}))
        run_in_devcker = get_config(CONFIGURATION_NAME).get('api-metadata.run-in-devcker', False)
        xforwaredfor = request.headers.getlist('X-Forwarded-For')
        if run_in_devcker and xforwaredfor:
            ip_addr = xforwaredfor[0]
        else:
            ip_addr = request.remote_addr
        return view(ip_addr)


class StateView(MetadataAPIBaseView):
    decorators = MetadataAPIBaseView.decorators + [
     exports.select_export(default='sh')]
    route_base = '/'
    validation_class = StateViewValidator()

    def _update_state(self, ip_addr, new_state):
        """ Update the server state """
        server = self._get_server_by_ip(ip_addr)
        response = self.privileged_compute_api.query().servers(server['id']).patch({'state_detail': new_state})
        return {'state_detail': response.get('server', {}).get('state_detail')}

    @route('/state', methods=['PATCH'])
    def put(self, ip_addr):
        ret = self._update_state(ip_addr, request.json['state_detail'])
        return ret