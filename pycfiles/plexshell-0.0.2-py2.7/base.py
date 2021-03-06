# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/plexshell/commands/base.py
# Compiled at: 2011-09-18 04:58:23
from cmd import Cmd
from httplib import HTTPConnection
from plexshell.utils import PlexError, Colors, colorize
import os, sys

class PlexCmd(Cmd, object):
    """ Base class for plex commands """

    def __init__(self, conn=None, *args, **kwargs):
        if kwargs.get('stdin', None) and kwargs['stdin'] != sys.stdin:
            setattr(self, 'interactive', False)
            self.use_rawinput = False
        super(PlexCmd, self).__init__(*args, **kwargs)
        self.conn = conn
        return

    def help_help(self):
        print 'Print command specific help'

    def help_exit(self):
        print 'Exit the interpreter.'
        print 'You can also use the Ctrl-D shortcut.'

    def help_shell(self):
        print 'Execute shell commands'

    def help_clear(self):
        print 'Clear the screen'

    def help_get(self):
        print 'Get a resource'

    def do_exit(self, s=None):
        return True

    def do_shell(self, s):
        os.system(s)

    def do_clear(self, s):
        os.system('clear')

    def do_get(self, name):
        resource = self.get_resource(name)
        if resource:
            print resource

    def do_EOF(self, line):
        return True

    def get_resource(self, name):
        if name.startswith('/'):
            return get(self.conn, name, 'Failed to get resource')

    def set_host(self, host, port):
        self.conn = HTTPConnection(host, port)
        self.update_prompt()

    def update_prompt(self):
        context = getattr(self, 'prompt_context', None)
        interactive = getattr(self, 'interactive', True)
        if not interactive:
            prompt = ''
        elif not self.conn:
            prompt = 'disconnected >'
        elif context:
            prompt = '%s:%s %s > ' % (self.conn.host, self.conn.port, context)
        else:
            prompt = '%s:%s > ' % (self.conn.host, self.conn.port)
        self.prompt = colorize(prompt, Colors.Green)
        return

    def cmdloop(self, intro=None):
        while True:
            try:
                return super(PlexCmd, self).cmdloop(intro)
            except PlexError as e:
                print e
            except KeyboardInterrupt:
                print 'Goodbye!'
                exit(1)

    do_EOF = do_exit
    help_EOF = help_exit