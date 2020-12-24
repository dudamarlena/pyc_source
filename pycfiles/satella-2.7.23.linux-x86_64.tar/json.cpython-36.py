# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/json.py
# Compiled at: 2020-05-08 08:03:23
# Size of source mod 2**32: 973 bytes
import json, typing as tp
from abc import ABCMeta, abstractmethod
__all__ = [
 'JSONEncoder', 'JSONAble', 'json_encode']
Jsonable = tp.TypeVar('Jsonable', list, dict, str, int, float, None)

class JSONAble(metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def to_json(self) -> Jsonable:
        """Return a JSON-able representation of this object"""
        pass


class JSONEncoder(json.JSONEncoder):
    __doc__ = '\n    This encoder will encode everything!\n    '

    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        try:
            return super().default(o)
        except TypeError:
            dct = {}
            for k, v in o.__dict__.items():
                dct[k] = repr(v)

            return dct


def json_encode(x: tp.Any) -> str:
    """
    Convert an object to JSON. Will properly handle subclasses of JSONAble

    :param x: object to convert
    """
    return JSONEncoder().encode(x)