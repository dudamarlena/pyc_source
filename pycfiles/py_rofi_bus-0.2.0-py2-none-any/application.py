# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjharries/Code/@wizardsoftheweb/py-rofi-bus/py_rofi_bus/cli/application.py
# Compiled at: 2018-06-02 23:19:29
from argparse import ArgumentParser
from sys import argv
from subprocess import check_call
from py_rofi_bus.cli import Daemon

class Application(object):

    def __init__(self, parent_parser=None):
        if parent_parser is None:
            self.parser = ArgumentParser(prog='py-rofi-bus', description='The py-rofi-bus CLI application')
        else:
            self.parser = parent_parser.add_parser('daemon', help='Manage the py-rofi-bus daemon')
        return

    def attach_subparsers(self):
        self.subparsers = self.parser.add_subparsers(dest='subcommand', help='Available actions')

    def add_action_daemon(self):
        daemon = Daemon(parent_parser=self.subparsers)
        daemon.attach_subparsers()
        daemon.add_action_start()
        daemon.add_action_status()
        daemon.add_action_stop()

    @staticmethod
    def bootstrap(args=None):
        if args is None:
            args = argv[1:]
        application = Application()
        application.attach_subparsers()
        application.add_action_daemon()
        config = application.parser.parse_args(args)
        if 'daemon' == config.subcommand:
            Daemon.ACTIONS[config.action]()
        return


if '__main__' == __name__:
    Application.bootstrap()