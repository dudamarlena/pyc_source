# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/api/controller/credential_controller.py
# Compiled at: 2017-08-02 01:06:09
import json, logging
from flask import request
import flask_restful
from flask_restful import reqparse
from six.moves import http_client
from column.api.common import utils
from column.api import manager
LOG = logging.getLogger(__name__)
credential_schema = {'$schema': 'http://json-schema.org/schema#', 
   'type': 'object', 
   'properties': {'value': {'type': 'string'}}, 'required': [
              'value'], 
   'additionalProperties': False}

class Credential(flask_restful.Resource):
    """Column api credential resource class

    Attributes:
         manager (obj): manager interface for calling column library method to
                        get/update the credential
    """

    def __init__(self):
        self.manager = manager.get_manager('credential')
        self.get_parser = self._get_parser()

    def _get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str, required=True)
        return parser

    def get(self):
        """Get a credential by file path"""
        args = self.get_parser.parse_args()
        return self.manager.get_credential(args)

    @utils.validator(credential_schema, http_client.BAD_REQUEST)
    def put(self):
        """Update a credential by file path"""
        cred_payload = utils.uni_to_str(json.loads(request.get_data()))
        return self.manager.update_credential(cred_payload)