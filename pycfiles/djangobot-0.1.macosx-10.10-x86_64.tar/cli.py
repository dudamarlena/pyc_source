# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scott/.envs/home/lib/python2.7/site-packages/djangobot/cli.py
# Compiled at: 2016-04-09 16:44:17
import argparse, importlib, os, sys
from .client import Client

class CLI(object):
    """
    Main command-line interface
    """

    def __init__(self):
        description = 'Slack bridge to a channels-based Django app'
        self.parser = argparse.ArgumentParser(description=description)
        self.parser.add_argument('-t', '--token', dest='token', help='Slack API token', default=os.environ.get('DJANGOBOT_TOKEN', None))
        self.parser.add_argument('channel_layer', help='ASGI channel layer instance to listen on given as path.to.module:layer')
        return

    @classmethod
    def entry(cls):
        """
        External starting point
        """
        cls().run(sys.argv[1:])

    def run(self, args):
        """
        Pass in raw arguments, instantiate Slack API and begin client.
        """
        args = self.parser.parse_args(args)
        if not args.token:
            raise ValueError('Supply the slack token through --token or setting DJANGOBOT_TOKEN')
        sys.path.insert(0, '.')
        module_path, object_path = args.channel_layer.split(':', 1)
        channel_layer = importlib.import_module(module_path)
        for part in object_path.split('.'):
            channel_layer = getattr(channel_layer, part)

        Client(channel_layer=channel_layer, token=args.token).run()