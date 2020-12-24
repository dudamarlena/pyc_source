# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\base\base.py
# Compiled at: 2019-05-21 04:22:39
# Size of source mod 2**32: 1813 bytes
import json, os
config = None

def get_config():
    global config
    if config is not None:
        return config
    else:
        if os.environ.get('MESOS_SANDBOX') is not None:
            path = os.environ.get('MESOS_SANDBOX') + '/config.json'
        else:
            path = 'config.json'
        if path is None:
            print('[base.get_config] path is null')
            return {}
        if not os.path.exists(path):
            print('[base.get_config] path not exists')
            return {}
        file = open(path)
        config = json.load(file)
        if 'ENV_HDFS_URI' not in config:
            config['ENV_HDFS_URI'] = 'hdfs://192.168.1.251:8020/'
        if 'ENV_HDFS_ROOT' not in config:
            config['ENV_HDFS_ROOT'] = 'algo/'
        print('[base.get_config] config -> %s' % config)
        return config


def get_hdfs_uri():
    config = get_config()
    return config['ENV_HDFS_URI']


def get_hdfs_root():
    config = get_config()
    return config['ENV_HDFS_ROOT']


def hdfs_normal_path(file):
    if file.startswith('/algo/'):
        return file
    else:
        if file.startswith('hdfs://'):
            return file
        if file.startswith('/'):
            return '/' + get_hdfs_root() + file
        return '/' + get_hdfs_root() + '/' + file


if __name__ == '__main__':
    get_config('config.test.json')