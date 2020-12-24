# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/config.py
# Compiled at: 2016-03-02 11:37:45
"""
"""
import os, appdirs
from six.moves import input
import yaml
from .dialog import ConfigGenerator

class NotConfigured(Exception):
    pass


data = {}

class ConfigFile(object):
    """ A wrapper for managing creating and reading a config file
    takes (optional) appname str kwarg,
    for testing creation/destruction """
    appname = 'gitberg'
    file_name = 'config.yaml'

    def __init__(self, appname=None):
        if appname:
            self.appname = appname
        self.dir = appdirs.user_config_dir(self.appname)
        self.exists_or_make()
        self.parse()

    @property
    def file_path(self):
        return os.path.join(self.dir, self.file_name)

    def exists_or_make(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'a'):
                os.utime(self.file_path, None)
        return

    def write(self):
        with open(self.file_path, 'wb') as (self.file):
            self.file.write(self.yaml)
        return True

    @property
    def yaml(self):
        global data
        return yaml.dump(data, default_flow_style=False)

    def __repr__(self):
        return self.read()

    def read(self):
        with open(self.file_path) as (_fp):
            return _fp.read()

    def parse(self):
        global data
        data = yaml.load(self.read())

    def check_self(self):
        pass


def check_config():
    """ Report if there is an existing config file
    """
    global data
    configfile = ConfigFile()
    if data.keys() > 0:
        print 'gitberg config file exists'
        print '\twould you like to edit your gitberg config file?'
    else:
        print 'No config found'
        print '\twould you like to create a gitberg config file?'
    answer = input('-->  [Y/n]')
    if not answer:
        answer = 'Y'
    if answer in 'Yy':
        print 'Running gitberg config generator ...'
        config_gen = ConfigGenerator(current=data)
        config_gen.ask()
        data = config_gen.answers
        configfile.write()
        print ('Config written to {}').format(configfile.file_path)