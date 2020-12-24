# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/clipy/argparse.py
# Compiled at: 2010-02-15 09:37:31
"""Utilities for defining commands based on argparse."""
import sys
argparse = __import__('argparse')
from clipy import command
__all__ = [
 'Command']

class Command(command.Command):
    """Command."""
    usage = '%(prog)s [options]'

    def create_parser(self):
        parser = argparse.ArgumentParser()
        parser.usage = self.usage
        return parser

    def parse_args(self, args):
        result = self.parser.parse_args(args)
        return (result, [])