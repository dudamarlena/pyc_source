# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\exceptions.py
# Compiled at: 2015-08-04 11:44:30


class NoSuchWidgetError(Exception):

    def __str__(self):
        return 'Unknown Qt widget: %s' % (self.args[0],)


class UnsupportedPropertyError(Exception):
    pass


class WidgetPluginError(Exception):
    pass