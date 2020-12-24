# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paicli/config.py
# Compiled at: 2019-07-22 03:56:29
# Size of source mod 2**32: 3608 bytes
"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function
import os, sys, yaml, codecs
from .utils import to_str
if sys.version_info[0] == 2:
    input = raw_input
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

HOME = os.path.expanduser('~')

class Config(object):
    _paicli_dirname = '.paicli'
    _configfile = 'config.yaml'
    _accesstoken = '.token_{}'
    path_to_configdir = os.path.join(HOME, _paicli_dirname)
    path_to_configfile = os.path.join(HOME, _paicli_dirname, _configfile)

    def __init__(self, profile='default'):
        self.profile = to_str(profile)
        self.host = to_str('10.0.3.9')
        self._port = 9186
        self.username = to_str('')
        self.password = to_str('')
        self.access_token = to_str('')
        self.api_version = to_str('v1')
        self.path_to_accesstoken = os.path.join(HOME, self._paicli_dirname, self._accesstoken.format(self.profile))

    def add_profile(self):
        self.host = to_str(input('Host ip address for PAI [{}]: '.format(self.host)) or self.host)
        self.port = input('Port for REST API [{}]: '.format(self.port)) or self.port
        self.username = to_str(input('Your username [{}]: '.format(self.username)) or self.username)
        self.password = to_str(input('Your password (optional) [{}]: '.format(self.password)) or self.password)
        self.write_config()

    def load(self):
        with codecs.open(self.path_to_configfile, 'r', 'utf-8') as (f):
            yaml_config = ''.join(f.readlines())
            config = yaml.load(yaml_config, Loader=(yaml.SafeLoader))
        self.host = config[self.profile]['host']
        self.port = config[self.profile]['port']
        self.port = config[self.profile]['port']
        self.username = config[self.profile]['username']
        self.password = config[self.profile]['password']

    def load_access_token(self):
        with codecs.open(self.path_to_accesstoken, 'r', 'utf-8') as (f):
            self.access_token = f.readline().strip('\n').strip()

    def write_config(self):
        if not os.path.exists(self.path_to_configdir):
            os.makedirs(self.path_to_configdir)
        profiles = {}
        new_config = {'host':to_str(self.host), 
         'port':self.port, 
         'username':to_str(self.username), 
         'password':to_str(self.password)}
        try:
            with codecs.open(self.path_to_configfile, 'r', 'utf-8') as (f):
                profiles = yaml.load(''.join(f.readlines()))
                profiles[self.profile] = new_config
        except FileNotFoundError:
            profiles[self.profile] = new_config

        with codecs.open(self.path_to_configfile, 'w', 'utf-8') as (f):
            f.writelines(yaml.safe_dump(profiles, default_flow_style=False))

    def write_access_token(self):
        if not os.path.exists(self.path_to_configdir):
            os.makedirs(self.path_to_configdir)
        with codecs.open(self.path_to_accesstoken, 'w', 'utf-8') as (f):
            f.write(self.access_token)

    @property
    def port(self):
        return int(self._port)

    @port.setter
    def port(self, _port):
        self._port = int(_port)

    @property
    def api_uri(self):
        return 'http://{}:{}'.format(self.host, self.port)