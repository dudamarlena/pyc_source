# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/constant.py
# Compiled at: 2019-03-28 06:07:50
# Size of source mod 2**32: 1857 bytes
from norm.grammar.literals import ConstantType
import datetime
from typing import Union, List

class Constant(object):

    def __init__(self, type_, value=None):
        """
        The constant
        :param type_: the name of the constant type, e.g.,
                      [none, bool, integer, float, string, unicode, pattern, uuid, url, datetime]
        :type type_: ConstantType
        :param value: the value of the constant
        :type value: Union[str, int, float, bool, datetime.datetime, None]
        """
        self.type_ = type_
        self.value = value

    def __str__(self):
        if self.type_ in [ConstantType.STR, ConstantType.PTN, ConstantType.UID, ConstantType.URL]:
            return '"{}"'.format(self.value)
        else:
            if self.type_ in [ConstantType.FLT, ConstantType.INT, ConstantType.BOOL]:
                return '{}'.format(self.value)
            if self.type_ == ConstantType.DTM:
                return self.value.strftime('"%Y-%m-%d %H:%M:%S"')
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def execute(self, context):
        return self.value


class ListConstant(Constant):

    def __init__(self, type_, values):
        assert isinstance(values, list)
        super().__init__(type_)
        self.value = values

    def __str__(self):
        return '[' + ','.join(str(v) for v in self.value) + ']'

    def __repr__(self):
        return str(self)