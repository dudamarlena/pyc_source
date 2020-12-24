# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/decorators.py
# Compiled at: 2017-11-28 02:59:59
import warnings

class generic_deprecation(object):

    def __init__(self, message, warning_class=DeprecationWarning, stack_level=2):
        self.message = message
        self.warning_class = warning_class
        self.stack_level = stack_level

    def __call__(self, method):

        def wrapped(*args, **kwargs):
            warnings.warn(self.message, self.warning_class, self.stack_level)
            return method(*args, **kwargs)

        return wrapped