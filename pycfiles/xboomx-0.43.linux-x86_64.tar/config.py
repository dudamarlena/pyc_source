# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/xboomx/config.py
# Compiled at: 2013-08-15 04:24:36
import os, json, logging

def load_config():
    try:
        with open(os.getenv('HOME') + '/.xboomx/config') as (config_file):
            return json.loads(('\n').join(config_file.readlines()))
    except:
        logging.error('Failed to load config file')
        return {}


config = load_config()