# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/frontends/console.py
# Compiled at: 2007-12-02 16:26:54
from salamoia.frontends.frontend import *
from optparse import OptionGroup
import xmlrpclib, code, readline, atexit, os
from salamoia.h2o.xmlclient import Client
from salamoia.frontends.config import Config

class Console(Frontend):
    __module__ = __name__

    def name(self):
        return 'console'

    def options(self, parser):
        """Return an option group specifing the front end specific options"""
        from optparse import OptionGroup
        optionGroup = OptionGroup(parser, 'Salamoia console options')
        optionGroup.add_option('-b', '--base', type='string', dest='base', help='base url')
        optionGroup.add_option('-p', '--port', type='string', dest='port', help='port')
        optionGroup.add_option('-H', '--host', type='string', dest='host', help='host')
        return optionGroup

    def run(self):
        (options, args) = self.optionParser.parse_args()
        self.options = options
        self.args = args
        historyPath = os.path.expanduser('~/.salamoia-console-history')

        def save_history(historyPath=historyPath):
            import readline
            readline.write_history_file(historyPath)

        if os.path.exists(historyPath):
            readline.read_history_file(historyPath)
        atexit.register(save_history)
        cfg = Config.defaultConfig()
        username = cfg.get('general', 'username')
        password = cfg.get('general', 'password')
        port = cfg.get('general', 'port')
        if self.options.port:
            port = self.options.port
        host = 'localhost'
        if self.options.host:
            host = self.options.host
        base = 'hostello'
        if self.options.base:
            base = self.options.base
        server = Client(host, port, base=base, username=username, password=password)
        code.interact(local={'server': server, 's': server, '__server__': server}, banner='Salamoia python interactive console')


def start():
    Console.start()