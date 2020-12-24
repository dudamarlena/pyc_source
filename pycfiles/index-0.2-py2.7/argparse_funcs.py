# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\lib\argparse_funcs.py
# Compiled at: 2013-08-05 10:21:39
from __future__ import division, absolute_import, print_function, unicode_literals
import os, argparse

class readable_file(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(values):
            raise argparse.ArgumentTypeError((b"FILE: '{0}' is not a valid path").format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError((b"FILE: '{0}' is not a readable file").format(values))


class readable_dir(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == b'~':
            setattr(namespace, self.dest, values)
            return
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError((b"DIR: '{0}' is not a valid path").format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError((b"DIR: '{0}' is not a readable dir").format(values))


class readable_file_or_dir(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == b'~':
            setattr(namespace, self.dest, values)
            return
        if not os.path.exists(values):
            raise argparse.ArgumentTypeError((b"DIR_or_FILE: '{0}' is not a valid path").format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError((b"DIR_or_FILE: '{0}' is not a readable dir").format(values))


class readable_file_or_dir_list(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            if value[0] == b'~':
                setattr(namespace, self.dest, values)
                continue
            if not os.path.exists(value):
                raise argparse.ArgumentTypeError((b"DIR_or_FILE: '{0}' is not a valid path").format(value))
            if os.access(value, os.R_OK):
                self.append_file(namespace, value)
            else:
                raise argparse.ArgumentTypeError((b"DIR_or_FILE: '{0}' is not a readable dir").format(value))

    def append_file(self, namespace, value):
        files_list = getattr(namespace, self.dest)
        if not files_list:
            files_list = []
        files_list.append(value)
        setattr(namespace, self.dest, files_list)