# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py_rofi_bus/components/script.py
# Compiled at: 2018-06-03 14:06:06
from sys import argv, exit as sys_exit

class Script(object):

    @staticmethod
    def load_args(args=None):
        if args is None:
            args = argv[1:]
        return args

    def parse_args(self, process_args=None, *args, **kwargs):
        """"""
        pass

    def construct_output(self, *args, **kwargs):
        """"""
        pass

    def format_output(self, *args, **kwargs):
        """"""
        pass

    def dump_output(self, *args, **kwargs):
        """"""
        pass

    def loop_callback(self, *args, **kwargs):
        """"""
        pass

    @classmethod
    def bootstrap(cls, process_args=None, *args, **kwargs):
        script = cls(*args, **kwargs)
        loaded_args = script.load_args(process_args)
        script.parse_args(process_args=loaded_args, *args, **kwargs)
        script.loop_callback(*args, **kwargs)
        script.construct_output(*args, **kwargs)
        script.format_output(*args, **kwargs)
        script.dump_output(*args, **kwargs)