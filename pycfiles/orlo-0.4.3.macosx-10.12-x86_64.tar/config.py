# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/config.py
# Compiled at: 2017-05-17 11:01:23
from __future__ import print_function
import os
from six.moves.configparser import RawConfigParser
__author__ = 'alforbes'
defaults = {'ORLO_CONFIG': '/etc/orlo/orlo.ini', 
   'ORLO_LOGDIR': '/var/log/orlo'}
for var, default in defaults.items():
    try:
        defaults[var] = os.environ[var]
    except KeyError:
        pass

if os.environ.get('READTHEDOCS', None) == 'True':
    defaults['ORLO_LOGDIR'] = 'disabled'
config = RawConfigParser()
config.add_section('main')
config.set('main', 'time_format', '%Y-%m-%dT%H:%M:%SZ')
config.set('main', 'time_zone', 'UTC')
config.set('main', 'base_url', 'http://localhost:8080')
config.add_section('gunicorn')
config.set('gunicorn', 'workers', '2')
config.set('gunicorn', 'bind', '127.0.0.1:8080')
config.add_section('security')
config.set('security', 'enabled', 'false')
config.set('security', 'passwd_file', 'none')
config.set('security', 'secret_key', 'change_me')
config.set('security', 'token_ttl', '3600')
config.set('security', 'ldap_server', 'localhost.localdomain')
config.set('security', 'ldap_port', '389')
config.set('security', 'user_base_dn', 'ou=people,ou=example,o=test')
config.add_section('db')
config.set('db', 'uri', 'sqlite://')
config.set('db', 'echo_queries', 'false')
config.set('db', 'pool_size', '50')
config.add_section('flask')
config.set('flask', 'propagate_exceptions', 'true')
config.set('flask', 'debug', 'false')
config.set('flask', 'strict_slashes', 'false')
config.add_section('logging')
config.set('logging', 'level', 'info')
config.set('logging', 'format', '%(asctime)s [%(name)s] %(levelname)s %(module)s:%(funcName)s:%(lineno)d - %(message)s')
config.set('logging', 'directory', defaults['ORLO_LOGDIR'])
config.add_section('behaviour')
config.set('behaviour', 'versions_by_release', 'false')
config.read(defaults['ORLO_CONFIG'])