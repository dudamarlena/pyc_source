# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/api/gunicorn-logging/gunicorn_logging/settings.py
# Compiled at: 2018-06-19 06:28:13
# Size of source mod 2**32: 1507 bytes
import os, sys, importlib
try:
    sys.path.append(os.getenv('WORKSPACE', '/'))
    settings = importlib.import_module(os.getenv('DJANGO_SETTINGS_MODULE'))
except Exception as e:
    from collections import namedtuple
    env = {k:v for k, v in os.environ.items() if not k.startswith('_') if not k.startswith('_')}
    settings = (namedtuple('settings', env.keys()))(*env.values())

LOGSTASH_HOST = getattr(settings, 'LOGSTASH_HOST', 'localhost') or 'localhost'
LOGSTASH_PORT = getattr(settings, 'LOGSTASH_PORT', 5000) or 5000
LOGSTASH_DB_PATH = getattr(settings, 'LOGSTASH_DB_PATH', None)
LOGSTASH_TRANSPORT = getattr(settings, 'LOGSTASH_TRANSPORT', 'logstash_async.transport.TcpTransport') or 'logstash_async.transport.TcpTransport'
LOGSTASH_SSL_ENABLE = getattr(settings, 'LOGSTASH_SSL_ENABLE', False)
LOGSTASH_SSL_VERIFY = getattr(settings, 'LOGSTASH_SSL_VERIFY', True)
LOGSTASH_KEYFILE = getattr(settings, 'LOGSTASH_KEYFILE', None)
LOGSTASH_CERTFILE = getattr(settings, 'LOGSTASH_CERTFILE', None)
LOGSTASH_CA_CERTS = getattr(settings, 'LOGSTASH_CA_CERTS', None)
LOGSTASH_ENABLE = getattr(settings, 'LOGSTASH_ENABLE', True)
LOGSTASH_EVENT_TTL = getattr(settings, 'LOGSTASH_EVENT_TTL', None)
LOGSTASH_ENCODING = getattr(settings, 'LOGSTASH_ENCODING', 'utf-8') or 'utf-8'
LOGSTASH_MESSAGE_TYPE = getattr(settings, 'LOGSTASH_MESSAGE_TYPE', 'API') or 'API'
LOGSTASH_MESSAGE_SUBTYPE = getattr(settings, 'LOGSTASH_MESSAGE_SUBTYPE', 'Gunicorn') or 'Gunicorn'
LOGSTASH_EXTRA = getattr(settings, 'LOGSTASH_EXTRA', {}) or {}