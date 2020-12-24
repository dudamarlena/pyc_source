# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/settings.py
# Compiled at: 2018-06-21 10:51:14
# Size of source mod 2**32: 1305 bytes
import os, yaml
home_path = os.path.expanduser('~')
settings_path = os.path.join(home_path, '.flu.yaml')
WSGI_NUM_WORKERS = None
WSGI_HOST = None
WSGI_PORT = None
WSGI_FLU_LOG = None
APP_HOST = None
APP_PORT = None
APP_AVAILABLE = True
DEBUG = None
DATABASE = {'NAME':None, 
 'USER':None, 
 'PASSWORD':None, 
 'HOST':None, 
 'PORT':None}
if not os.path.exists(settings_path):
    settings_yaml = {'WSGI_NUM_WORKERS':'4',  'WSGI_HOST':'0.0.0.0', 
     'WSGI_PORT':'8000', 
     'WSGI_FLU_LOG':'.flu.log', 
     'APP_HOST':'0.0.0.0', 
     'APP_PORT':'5000', 
     'APP_AVAILABLE':True, 
     'DEBUG':False, 
     'DATABASE':{'NAME':'<DATABASE_HERE>', 
      'USER':'<DATABASE_USER_HERE>', 
      'PASSWORD':'<DATABASE_PASSWORD_HERE>', 
      'HOST':'<DATABASE_HOST_HERE>', 
      'PORT':'<DATABASE_PORT_HERE>'}}
    with open(os.path.join(settings_path), 'w') as (f):
        yaml.dump(settings_yaml, f, default_flow_style=False)
    raise Exception('Please configure your settings file (%s)' % settings_path)
with open(os.path.join(settings_path), 'r') as (f):
    globals().update(yaml.load(f))
PATH = os.path.dirname(os.path.abspath(__file__))