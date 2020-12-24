# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/datatypes.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1218 bytes
import web3.utils.formatters
from web3.utils.toolz import concat, curry

@curry
def verify_attr(class_name, key, namespace):
    if key not in namespace:
        raise AttributeError('Property {0} not found on {1} class. `{1}.factory` only accepts keyword arguments which are present on the {1} class'.format(key, class_name))


class PropertyCheckingFactory(type):

    def __init__(cls, name, bases, namespace, **kargs):
        super().__init__(name, bases, namespace)

    def __new__(mcs, name, bases, namespace, normalizers=None):
        all_bases = set(concat(base.__mro__ for base in bases))
        for key in namespace:
            verify_key_attr = verify_attr(name, key)
            verify_key_attr(concat(base.__dict__.keys() for base in all_bases))

        if normalizers:
            processed_namespace = web3.utils.formatters.apply_formatters_to_dict(normalizers, namespace)
        else:
            processed_namespace = namespace
        return super().__new__(mcs, name, bases, processed_namespace)