# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\maha_cet_parser\commands\Commands.py
# Compiled at: 2020-04-12 15:36:59
# Size of source mod 2**32: 1463 bytes
import configargparse, inspect, logging, maha_cet_parser.commands

class Command(object):

    def __init__(self, args):
        pass

    @staticmethod
    def parse_args(input_args):
        """Parse the command line arguments."""
        parser = configargparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='Specify a command for Maharastrha CET admission')
        for member in inspect.getmembers(maha_cet_parser.commands, inspect.isclass):
            if member[0] != 'Command':
                member[1].add_args(subparsers)

        args = parser.parse_args(input_args)
        return args

    @staticmethod
    def add_common_args(parser, arglist=None, required_override=True):
        pass

    @staticmethod
    def add_global_args(parser):
        pass

    def get_tags(self):
        return [
         {'Key':'StackPrefix', 
          'Value':self.stack_prefix},
         {'Key':'Environment', 
          'Value':self.env},
         {'Key':'Owner', 
          'Value':self.owner}]

    def load_arg_or_default(self, args, arg_name, default_value=None):
        if arg_name in args and getattr(args, arg_name) is not None:
            setattr(self, arg_name, getattr(args, arg_name))
        else:
            setattr(self, arg_name, default_value)