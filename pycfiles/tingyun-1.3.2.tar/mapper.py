# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/mapper.py
# Compiled at: 2016-06-30 06:13:10
import logging
ENV_CONFIG_FILE = 'TING_YUN_CONFIG_FILE'
CONSTANCE_OUT_DATE_CONFIG = -815
CONSTANCE_INVALID_DATA_TOKEN = CONSTANCE_OUT_DATE_CONFIG
CONSTANCE_DISCARD_DATA = -816
CONSTANCE_SERVER_UNAVAILABLE = -817
CONSTANCE_RETRY_DATA = -818
CONSTANCE_HARVEST_ERROR = -819
CONSTANCE_LICENSE_INVALID = -820
CONSTANCE_SESSION_NOT_ACTIVED = -830
_LOG_LEVEL = {'CRITICAL': logging.CRITICAL, 
   'ERROR': logging.ERROR, 
   'WARNING': logging.WARNING, 
   'INFO': logging.INFO, 
   'DEBUG': logging.DEBUG, 
   'NOTSET': logging.NOTSET, 
   'FATAL': logging.FATAL, 
   'WARN': logging.WARN}
BOOL_MAPPING = {'ON': True, 
   'OFF': False, 
   'TRUE': True, 
   'FALSE': False}

def map_log_level(s):
    level = None
    try:
        return _LOG_LEVEL[('%s' % str(s).upper())]
    except Exception as _:
        pass

    return level


def map_app_name(s):
    return s or None


def map_include_environ(s):
    return str(s).split()


def map_key_words(v):
    """
    :param v:
    :return:
    """
    if isinstance(v, bool):
        return v
    else:
        v = str(v).upper()
        if v in BOOL_MAPPING:
            return BOOL_MAPPING[v]
        return
        return


CONFIG_ITEM = [{'section': 'tingyun', 'key': 'license_key', 'mapper': None}, {'section': 'tingyun', 'key': 'enabled', 'mapper': map_key_words}, {'section': 'tingyun', 'key': 'app_name', 'mapper': map_app_name}, {'section': 'tingyun', 'key': 'audit_mode', 'mapper': map_key_words}, {'section': 'tingyun', 'key': 'auto_action_naming', 'mapper': map_key_words}, {'section': 'tingyun', 'key': 'ssl', 'mapper': map_key_words}, {'section': 'tingyun', 'key': 'action_tracer.log_sql', 'mapper': map_key_words}, {'section': 'tingyun', 'key': 'log_file', 'mapper': None}, {'section': 'tingyun', 'key': 'log_level', 'mapper': map_log_level}]