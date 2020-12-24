# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp3/options/arguments.py
# Compiled at: 2019-12-16 21:55:05
# Size of source mod 2**32: 1194 bytes
from __future__ import unicode_literals
import argparse
from textwrap import dedent

class ArgparseMixin:
    __doc__ = "Argparse utils\n\n    Usage\n    ::\n        from kipp3.options import options as opt\n\n        # set command argument\n        opt.add_argument('--test', type=str)\n\n        # parse argument\n        opt.parse_args()\n\n        # use argument\n        print(opt.test)\n    "

    def setup_argparse(self, name=''):
        """Setup argparse with name"""
        self._parser = argparse.ArgumentParser(name,
          formatter_class=(argparse.RawTextHelpFormatter))

    def add_argument(self, *args, **kw):
        """Add command arguments"""
        if not hasattr(self, '_parser'):
            self.setup_argparse()
        if '\n' in kw.get('help', ''):
            kw['help'] = dedent(kw['help'])
        (self._parser.add_argument)(*args, **kw)

    def parse_args(self, *args, **kw):
        """Parse command arguments"""
        is_patch_utilies = kw.pop('is_patch_utilies', True)
        args = (self._parser.parse_args)(*args, **kw)
        self.set_command_args(args, is_patch_utilies=is_patch_utilies)
        return args