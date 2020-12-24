# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/py-elevator/tests/fakers.py
# Compiled at: 2012-10-23 05:10:23
import tempfile, os, shutil, subprocess, random, ConfigParser

def gen_test_conf():
    """Generates a ConfigParser object built with test options values"""
    global_config_options = {'pidfile': tempfile.mkstemp(suffix='.pid', dir='/tmp')[1], 
       'databases_storage_path': tempfile.mkdtemp(dir='/tmp'), 
       'database_store': tempfile.mkstemp(suffix='.json', dir='/tmp')[1], 
       'bind': '127.0.0.1', 
       'port': str(random.randint(4142, 60000)), 
       'activity_log': tempfile.mkstemp(suffix='.log', dir='/tmp')[1], 
       'errors_log': tempfile.mkstemp(suffix='_errors.log', dir='/tmp')[1], 
       'max_cache_size': 1024}
    config = ConfigParser.RawConfigParser()
    config.add_section('global')
    for key, value in global_config_options.iteritems():
        config.set('global', key, value)

    return config


class TestDaemon(object):

    def __init__(self):
        self.bootstrap_conf()
        self.process = None
        self.port = self.config.get('global', 'port')
        self.bind = self.config.get('global', 'bind')
        return

    def __del__(self):
        for key, value in self.config.items('global'):
            if not isinstance(value, int) and os.path.exists(value):
                if os.path.isfile(value):
                    os.remove(value)
                elif os.path.isdir(value):
                    shutil.rmtree(value)

        os.remove(self.conf_file_path)

    def bootstrap_conf(self):
        self.conf_file_path = tempfile.mkstemp(suffix='.conf', dir='/tmp')[1]
        self.config = gen_test_conf()
        with open(self.conf_file_path, 'w') as (f):
            self.config.write(f)

    def start(self):
        self.process = subprocess.Popen(['elevator',
         '--config', self.conf_file_path,
         '--bind', self.bind,
         '--port', self.port,
         '--log-level', 'CRITICAL'])

    def stop(self):
        self.process.kill()