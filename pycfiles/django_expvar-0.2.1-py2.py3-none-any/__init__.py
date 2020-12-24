# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/code/python/django-expvar/expvar/__init__.py
# Compiled at: 2016-05-01 17:02:19


class ExpVar(object):
    """ subclass this to define an expvar

    set the `name` attribute or override `.get_name()`

    and define a `.value()` method.
    """

    def get_name(self):
        return self.name

    def value(self):
        return