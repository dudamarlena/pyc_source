# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyfmpcloud\settings.py
# Compiled at: 2020-05-06 10:41:17
# Size of source mod 2**32: 770 bytes
import configparser, os
cfile = os.path.join(os.path.dirname(__file__), 'config.ini')

def get_urlroot():
    cfg = configparser.ConfigParser()
    cfg.read(cfile)
    urlroot = cfg['API']['url_root']
    return urlroot


def get_urlrootfmp():
    cfg = configparser.ConfigParser()
    cfg.read(cfile)
    urlrootfmp = cfg['API']['url_root_fmp']
    return urlrootfmp


def get_apikey():
    cfg = configparser.ConfigParser()
    cfg.read(cfile)
    apikey = cfg['API']['api_key']
    return apikey


def set_apikey(apikey):
    cfg = configparser.ConfigParser()
    cfg.read(cfile)
    cfg['API']['api_key'] = apikey
    with open(cfile, 'w') as (configfile):
        cfg.write(configfile)