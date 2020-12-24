# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyfmpcloud\settings.py
# Compiled at: 2020-05-11 14:30:11
# Size of source mod 2**32: 658 bytes
import configparser, os
cfile = os.path.join(os.path.dirname(__file__), 'config.ini')
cfg = configparser.ConfigParser()
cfg.read(cfile)
try:
    cfg.has_section('API')
except:
    raise Exception('Config File was not read.')

def get_urlroot():
    urlroot = cfg['API']['url_root']
    return urlroot


def get_urlrootfmp():
    urlrootfmp = cfg['API']['url_root_fmp']
    return urlrootfmp


def get_apikey():
    apikey = cfg['API']['api_key']
    return apikey


def set_apikey(apikey):
    cfg['API']['api_key'] = apikey
    with open(cfile, 'w') as (configfile):
        cfg.write(configfile)