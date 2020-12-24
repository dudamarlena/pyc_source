# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/options/arguments.py
# Compiled at: 2019-11-08 04:26:21
from __future__ import unicode_literals
import argparse
from textwrap import dedent

class ArgparseMixin:
    """Argparse utils

    Usage
    ::
        from kipp.options import options as opt

        # set command argument
        opt.add_argument('--test', type=str)

        # parse argument
        opt.parse_args()

        # use argument
        print(opt.test)
    """

    def setup_argparse(self, name=b''):
        """Setup argparse with name"""
        self._parser = argparse.ArgumentParser(name, formatter_class=argparse.RawTextHelpFormatter)

    def add_argument(self, *args, **kw):
        """Add command arguments"""
        if not hasattr(self, b'_parser'):
            self.setup_argparse()
        if b'\n' in kw.get(b'help', b''):
            kw[b'help'] = dedent(kw[b'help'])
        self._parser.add_argument(*args, **kw)

    def parse_args(self, *args, **kw):
        """Parse command arguments"""
        is_patch_utilies = kw.pop(b'is_patch_utilies', True)
        args = self._parser.parse_args(*args, **kw)
        self.set_command_args(args, is_patch_utilies=is_patch_utilies)
        return args