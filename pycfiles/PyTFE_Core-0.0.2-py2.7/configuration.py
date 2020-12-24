# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tfe/core/configuration.py
# Compiled at: 2018-10-22 02:47:21
import requests, os
from jinja2 import Template
from functools import partial
import urllib, json, sys, tarfile, logging
from tfe.core.session import TFESession
from tfe.core.exception import RaisesTFEException, TFESessionException
from tfe.core.tfe import TFEObject, Validator

class Configuration(TFEObject):
    _base_dir = os.path.dirname(__file__)
    json_template = None
    hcl_template = None
    fields = [
     'auto_queue',
     'speculative']

    def __init__(self, configuration_id=None, **kwargs):
        super()
        self.auto_queue = False
        self.speculative = False
        self.upload_url = None
        self.workspace = None
        self.cleanup = False
        if configuration_id:
            self.id = configuration_id
        for k, v in kwargs.items():
            setattr(self, k, v)

        logging.basicConfig(format='%(asctime)-15s com.happypathway.tfe.%(name)s: %(message)s')
        Configuration.logger = logging.getLogger(self.__class__.__name__)
        Configuration.validator = type(('{0}Validator').format(self.__class__.__name__), (
         Validator,), dict(_fields=self.__class__.fields))()
        with open(('{0}/templates/json/configuration.json.j2').format(self._base_dir)) as (vars_template):
            Configuration.json_template = Template(vars_template.read())
        return

    @property
    def list_url(self):
        return ('{0}/api/v2/workspaces/{1}/configuration-versions?include=ingress_attributes').format(self.base_url, self.workspace.id)

    @property
    def read_url(self):
        return ('{0}/api/v2/configuration-versions/{1}').format(self.base_url, self.id)

    @property
    def create_url(self):
        return ('{0}/api/v2/workspaces/{1}/configuration-versions').format(self.base_url, self.workspace.id)

    def upload(self, config_path):
        _path = sanitize_path(config_path)
        cur_dir = os.getcwd()
        self.logger.info(('Changing Directory to {0}').format(_path))
        os.chdir(_path)

        def _filter(tar_info):
            self.logger.debug(('inspecting {0}').format(tar_info.name))
            if tar_info.name != 'terraform_config.tar.gz' and '.git' not in tar_info.name and '.terraform' not in tar_info.name:
                return tar_info
            else:
                return
                return

        with tarfile.open('terraform_config.tar.gz', 'w:gz') as (_tar):
            _tar.add('.', filter=_filter)
        self.logger.info(('Uploading {0}/terraform_config.tar.gz').format(os.getcwd()))
        cur_content_type = self.session.headers.get('Content-Type')
        exit_code = os.system(('curl --request PUT -F "data=@{0}" {1}').format('terraform_config.tar.gz', self.upload_url))
        self.session.headers['Content-Type'] = cur_content_type
        if self.cleanup:
            self.logger.info(('Removing {0}').format(os.path.join(os.getcwd(), 'terraform_config.tar.gz')))
            os.unlink('terraform_config.tar.gz')
        self.logger.info(('Changing Directory back to {0}').format(cur_dir))
        os.chdir(cur_dir)
        return exit_code