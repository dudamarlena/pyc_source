# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: J:\workspace\python\haf\haf\common\schema.py
# Compiled at: 2020-03-21 04:56:32
# Size of source mod 2**32: 540 bytes
"""
file name : schema
description : the json schema check
others:
    usage:
        check_config(config)
"""
from jsonschema import validate
from haf.config import config_schema

def check_config(config):
    """
    check the haf run config is right or not with the config_schema in haf.config

    :param config: the input
    :return: check result
    """
    try:
        validate(instance=config, schema=config_schema)
        return True
    except Exception as e:
        try:
            print(e)
            return False
        finally:
            e = None
            del e