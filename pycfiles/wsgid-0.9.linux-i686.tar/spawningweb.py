# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/servers/spawningweb.py
# Compiled at: 2009-03-08 14:05:54
import os, sys, subprocess
from wsgid.server import BaseWSGIServer, get_app, create_config
from spawning.spawning_controller import run_controller, DEFAULTS

class ConfigHolder(object):
    """A config holder"""
    app = None


class WSGIServer(BaseWSGIServer):

    def start(self):
        if not self.conf.application:
            self.log.warn('For spawning, must provide an importable app instance')
            self.conf.application = 'wsgid.server.default_app'
        factory_args = DEFAULTS.copy()
        factory_args.update({'verbose': False, 
           'host': self.conf.host, 
           'port': self.conf.port, 
           'access_log_file': os.path.join(self.conf.logdir, 'access.log'), 
           'coverage': False, 
           'args': [
                  self.conf.application], 
           'wsgid_conf': self.conf.to_dict(), 
           'num_processes': 4})
        run_controller('wsgid.servers.spawningweb.config_factory', factory_args)


def config_factory(args):
    args['app_factory'] = 'wsgid.servers.spawningweb.app_factory'
    return args


def app_factory(args):
    conf = create_config(args.get('wsgid_conf', {}))
    app = get_app(conf)
    return app