# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tfe/core/run.py
# Compiled at: 2018-10-14 15:04:23
import requests, os
from jinja2 import Template
from functools import partial
import urllib, json, sys, logging
from tfe.core.session import TFESession
from tfe.core.exception import RaisesTFEException, TFESessionException
from tfe.core.tfe import TFEObject, Validator

class Run(TFEObject):
    _base_dir = os.path.dirname(__file__)
    json_template = ''
    fields = [
     'run_message',
     'workspace_id',
     'configuration_version']

    def __init__(self, run_id=None, **kwargs):
        super()
        self.run_id = run_id
        self.workspace_id = None
        self.configuration_version = None
        Run.validator = type(('{0}Validator').format(self.__class__.__name__), (
         Validator,), dict(_fields=self.__class__.fields))()
        logging.basicConfig(format='%(asctime)-15s com.happypathway.tfe.%(name)s: %(message)s')
        Run.logger = logging.getLogger(self.__class__.__name__)
        for k, v in kwargs.items():
            setattr(self, k, v)

        with open(('{0}/templates/json/run.json.j2').format(self._base_dir)) as (vars_template):
            Run.json_template = Template(vars_template.read())
        return

    @property
    def create_url(self):
        return ('{0}/api/v2/runs').format(self.base_url)

    @property
    def read_url(self):
        return ('{0}/api/v2/runs/{1}').format(self.base_url, self.run_id)

    @property
    def list_url(self):
        return ('{0}/api/v2/workspaces/{1}/runs').format(self.base_url, self.workspace_id)

    @property
    def status(self):
        url = ('{0}/api/v2/runs/{1}').format(self.base_url, self.run_id)
        try:
            resp = self.session.get(url)
            return resp.json().get('data').get('attributes').get('status')
        except Exception as e:
            self.logger.error(str(e))
            return

        return

    def apply(self):
        resp = self.session.post(('{0}/api/v2/runs/{1}/actions/apply').format(self.base_url, self.run_id))
        resp.raise_for_status()
        return resp.json()

    def discard(self):
        resp = self.session.post(('{0}/api/v2/runs/{1}/actions/discard').format(self.base_url, self.run_id))
        return resp.status_code

    def cancel(self):
        resp = self.session.post(('{0}/api/v2/runs/{1}/actions/cancel').format(self.base_url, self.run_id))
        return resp.status_code

    def force_cancel(self):
        resp = self.session.post(('{0}/api/v2/runs/{1}/actions/force-cancel').format(self.base_url, self.run_id))
        return resp.status_code