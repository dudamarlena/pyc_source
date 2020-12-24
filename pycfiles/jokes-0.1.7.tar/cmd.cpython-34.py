# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/jks/Root/Dev/python/jokes/jokes/modules/cmd.py
# Compiled at: 2015-10-26 15:57:32
# Size of source mod 2**32: 591 bytes


def help(*args):
    """ Info about commands """
    helpstr = '--------------------------------\n List of Shell Commands:\n\n help :) show list of commands\n joke :) show metainfo\n exit :) exit the shell\n\njokes built-in statements: \n--------------------------------'
    return helpstr


def joke(*args):
    return 'this is a funny joke version 0.00'


class jokes:

    def output(self, *args):
        return args

    def input(self):
        return input()

    def call(self, *args):
        vals = []
        for arg in args:
            vals.append(arg())

        return vals