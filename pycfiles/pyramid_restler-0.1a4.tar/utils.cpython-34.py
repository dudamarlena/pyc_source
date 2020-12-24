# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/utils.py
# Compiled at: 2014-08-22 04:59:55
# Size of source mod 2**32: 741 bytes
__author__ = 'tarzan'

def is_sqlalchemy_column(col):
    try:
        from sqlalchemy.orm.attributes import InstrumentedAttribute
        from sqlalchemy.orm.properties import ColumnProperty
        return isinstance(col, InstrumentedAttribute) and isinstance(col.property, ColumnProperty)
    except ImportError as e:
        return False


def sqlalchemy_obj_to_dict(obj):
    """
    Return a dict from a sqlalchemy object
    :param object obj: object that contains source information
    :return: data from object
    :rtype : dict
    """
    cls = obj.__class__
    data = {a:obj.__getattribute__(a) for a, c in cls.__dict__.items() if is_sqlalchemy_column(c)}
    return data