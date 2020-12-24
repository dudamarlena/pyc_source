# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/standalone/utils/file_utils.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 1941 bytes
import json, os
from cachetools import LRUCache
from cachetools import cached
PROJECT_BASE = None

def get_project_base_directory():
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir, os.pardir))
    return PROJECT_BASE


@cached(cache=LRUCache(maxsize=10))
def load_json_conf(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as (f):
            return json.load(f)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def dump_json_conf(config_data, conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path, 'w') as (f):
            json.dump(config_data, f, indent=4)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


if __name__ == '__main__':
    print(get_project_base_directory())
    print(load_json_conf('conf/transfer_conf.json'))