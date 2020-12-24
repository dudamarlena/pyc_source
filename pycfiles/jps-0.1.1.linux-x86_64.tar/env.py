# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/env.py
# Compiled at: 2016-06-11 06:32:43
import json, os
from .common import DEFAULT_HOST
from .common import DEFAULT_PUB_PORT
from .common import DEFAULT_SUB_PORT

def get_topic_suffix():
    return os.environ.get('JPS_SUFFIX', '')


def get_topic_prefix():
    return os.environ.get('JPS_PREFIX', '')


def get_master_host():
    return os.environ.get('JPS_MASTER_HOST', DEFAULT_HOST)


def get_pub_port():
    return os.environ.get('JPS_MASTER_PUB_PORT', DEFAULT_PUB_PORT)


def get_sub_port():
    return os.environ.get('JPS_MASTER_SUB_PORT', DEFAULT_SUB_PORT)


def get_default_serializer():
    serialize = os.environ.get('JPS_SERIALIZE', 'no')
    if serialize == 'json':
        return json.dumps
    else:
        return


def get_default_deserializer():
    serialize = os.environ.get('JPS_SERIALIZE', 'no')
    if serialize == 'json':
        return json.loads
    else:
        return


def get_remapped_topic_name(topic_name):
    if 'JPS_REMAP' not in os.environ:
        return topic_name
    remaps = os.environ['JPS_REMAP'].split(',')
    for remap in remaps:
        original, renamed = remap.split('=')
        if original.strip() == topic_name:
            return renamed.strip()

    return topic_name