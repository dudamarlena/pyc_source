# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/Elevator/tests/fakers.py
# Compiled at: 2012-10-23 04:08:00
import os, shutil, subprocess, tempfile, ConfigParser, random
from elevator.env import Environment

def gen_test_env():
    tmp = tempfile.mkdtemp(dir='/tmp')
    return Environment(**{'global': {'daemonize': 'no', 
                  'pidfile': os.path.join(tmp, 'elevator_test.pid'), 
                  'databases_storage_path': os.path.join(tmp, 'elevator_test'), 
                  'database_store': os.path.join(tmp, 'elevator_test/store.json'), 
                  'default_db': 'default', 
                  'port': 4141, 
                  'bind': '127.0.0.1', 
                  'activity_log': os.path.join(tmp, 'elevator_test.log'), 
                  'errors_log': os.path.join(tmp, 'elevator_errors.log'), 
                  'max_cache_size': 1024}})


def gen_test_conf():
    """Generates a ConfigParser object built with test options values"""
    global_config_options = {'pidfile': tempfile.mkstemp(suffix='.pid', dir='/tmp')[1], 
       'databases_storage_path': tempfile.mkdtemp(dir='/tmp'), 
       'database_store': tempfile.mkstemp(suffix='.json', dir='/tmp')[1], 
       'port': str(random.randint(4142, 60000)), 
       'activity_log': tempfile.mkstemp(suffix='.log', dir='/tmp')[1], 
       'errors_log': tempfile.mkstemp(suffix='_errors.log', dir='/tmp')[1]}
    config = ConfigParser.ConfigParser()
    config.add_section('global')
    for key, value in global_config_options.iteritems():
        config.set('global', key, value)

    return config


class TestDaemon(object):

    def __init__(self):
        self.bootstrap_conf()
        self.process = None
        self.port = self.config.get('global', 'port')
        return

    def __del__(self):
        for key, value in self.config.items('global'):
            if not isinstance(value, (int, float)) and os.path.exists(value):
                if os.path.isfile(value):
                    os.remove(value)
                elif os.path.isdir(value):
                    shutil.rmtree(value)

        os.remove(self.conf_file_path)

    def bootstrap_conf(self):
        self.conf_file_path = tempfile.mkstemp(suffix='.conf', dir='/tmp')
        self.config = gen_test_conf()
        with open(self.conf_file_path) as (f):
            self.config.write(f)

    def start(self):
        self.process = subprocess.Popen(['elevator',
         '--config', self.conf_file_path,
         '--port', self.port])

    def stop(self):
        self.process.kill()