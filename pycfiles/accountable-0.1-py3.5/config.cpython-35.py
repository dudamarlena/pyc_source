# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/accountable/config.py
# Compiled at: 2016-11-19 19:27:44
# Size of source mod 2**32: 2090 bytes
import os, click, yaml
from requests.auth import HTTPBasicAuth

class Config(object):
    CONFIG_DIR = os.path.expanduser('~/.accountable')
    DEFAULT_ISSUE_FIELDS = [
     {'reporter': 'displayName'},
     {'assignee': 'displayName'},
     {'issuetype': 'name'},
     {'status': {'statusCategory': 'name'}},
     'summary',
     'description']
    DEFAULT_ALIASES = {'cob': 'checkoutbranch', 
     'co': 'checkout'}

    def __init__(self):
        self._config = None

    def __getitem__(self, name):
        return self.config[name]

    def create(self, **kwargs):
        username = str(kwargs.get('username'))
        password = str(kwargs.get('password'))
        domain = str(kwargs.get('domain'))
        config_dict = self._config_dict(username, password, domain)
        self._create_config(config_dict)

    @property
    def config(self):
        if self._config is None:
            self._config = self._load_config()
        return self._config

    @property
    def auth(self):
        return HTTPBasicAuth(self['username'], self['password'])

    @property
    def config_file(self):
        return '{}/config.yaml'.format(self.CONFIG_DIR)

    def _load_config(self):
        with open(self.config_file, 'r') as (f):
            config = yaml.load(f)
        return config

    def _create_config_dir(self):
        if not os.path.exists(self.CONFIG_DIR):
            click.echo('Creating {}'.format(self.CONFIG_DIR))
            os.makedirs(self.CONFIG_DIR)

    def _config_dict(self, username, password, domain):
        return {'username': username, 
         'password': password, 
         'domain': domain, 
         'issue_fields': self.DEFAULT_ISSUE_FIELDS, 
         'aliases': self.DEFAULT_ALIASES}

    def _create_config(self, config_dict):
        self._create_config_dir()
        with open(self.config_file, 'w+') as (f):
            f.write(yaml.dump(config_dict, default_flow_style=False))
        click.echo('Configuration file written to {}'.format(self.config_file))