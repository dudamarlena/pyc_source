# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adambogdal/git/freepacktbook/freepacktbook/utils.py
# Compiled at: 2017-07-19 15:37:40
from os import environ

class ImproperlyConfiguredError(Exception):
    pass


def check_config(variables):
    for variable in variables:
        if variable not in environ:
            raise ImproperlyConfiguredError('%s environment variable is required' % variable)


def env_variables_required(variables):

    def decorated(func):

        def new_function(*args, **kwargs):
            check_config(variables)
            func(*args, **kwargs)

        return new_function

    return decorated