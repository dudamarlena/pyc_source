# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wduss/src/github.com/dalloriam/engel/engel/utils.py
# Compiled at: 2017-01-06 15:18:40
# Size of source mod 2**32: 287 bytes


def html_property(prop_name):

    def getter(self):
        return self._attributes[prop_name]

    def setter(self, value):
        self._set_attribute(prop_name, value)

    def deleter(self):
        self._set_attribute(prop_name, None)

    return property(getter, setter, deleter)