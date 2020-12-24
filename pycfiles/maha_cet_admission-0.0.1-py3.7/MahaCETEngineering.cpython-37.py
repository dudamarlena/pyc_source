# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\maha_cet_parser\commands\MahaCETEngineering.py
# Compiled at: 2020-04-12 12:34:01
# Size of source mod 2**32: 488 bytes
from .Commands import Command
import logging
from xlrd import open_workbook

class MahaCETEngineering(Command):

    def __init__(self, args):
        """Intialize the object by using the arguments from argparse"""
        Command.__init__(self, args)

    @staticmethod
    def add_args(subparsers):
        pass

    @staticmethod
    def add_common_args(parser, arglist=None, required_override=True):
        """Parse the common command line arguments """
        pass