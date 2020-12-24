# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/params_builder.py
# Compiled at: 2015-08-31 22:18:13
import alman

class ParamsBuilder(object):

    @classmethod
    def merge(cls, *args):
        params = {}
        for other_dict in args:
            params.update(other_dict)

        return params

    @classmethod
    def default_params(cls):
        return {}

    @classmethod
    def build(cls, params):
        """ Class currently does nothing, but was created to conform to spec."""
        return cls.merge(cls.default_params(), params)