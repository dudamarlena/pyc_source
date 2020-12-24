# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tfe/core/variable.py
# Compiled at: 2018-10-14 15:08:34
import requests, os
from jinja2 import Template
from functools import partial
import urllib, json, logging, hcl, sys
from tfe.core.session import TFESession
from tfe.core.tfe import Validator, TFEObject
from tfe.core.exception import TFEException, RaisesTFEException, TFESessionException

class Variable(TFEObject):
    _base_dir = os.path.dirname(__file__)
    json_template = None
    hcl_template = None
    fields = [
     'key',
     'value',
     'category',
     'hcl',
     'sensitive',
     'workspace_id']

    def __init__(self, variable_id=None):
        super()
        self.organization = None
        self.workspace = None
        if variable_id:
            self.id = variable_id
        else:
            self.id = None
        Variable.validator = type(('{0}Validator').format(self.__class__.__name__))
        logging.basicConfig(format='%(asctime)-15s %(message)s')
        Variable.logger = logging.getLogger(self.__class__.__name__)
        Variable.validator = type(('{0}Validator').format(self.__class__.__name__), (
         Validator,), dict(_fields=self.__class__.fields))()
        with open(('{0}/templates/json/variable.json.j2').format(self._base_dir)) as (_template):
            Variable.json_template = Template(_template.read())
        with open(('{0}/templates/hcl/variable.hcl.j2').format(self._base_dir)) as (_template):
            Variable.hcl_template = Template(_template.read())
        return

    @property
    def list_url(self):
        query_params = []
        query_params.append(('filter%5Borganization%5D%5Bname%5D={0}').format(self.organization))
        query_params.append(('filter%5Bworkspace%5D%5Bname%5D={0}').format(self.workspace))
        return ('{0}/api/v2/vars?{1}').format(self.base_url, ('&').join(query_params))

    @property
    def create_url(self):
        return ('{0}/api/v2/vars').format(self.base_url)

    @property
    def update_url(self):
        return ('{0}/api/v2/vars/{1}').format(self.base_url, self.id)

    @property
    def delete_url(self):
        return ('{0}/api/v2/vars/{1}').format(self.base_url, self.id)