# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: //bigfoot/grimmhelga/Production/scripts/libraries/nuke\pysideuic\exceptions.py
# Compiled at: 2014-04-23 23:47:04


class NoSuchWidgetError(Exception):

    def __str__(self):
        return 'Unknown Qt widget: %s' % (self.args[0],)


class UnsupportedPropertyError(Exception):
    pass


class WidgetPluginError(Exception):
    pass