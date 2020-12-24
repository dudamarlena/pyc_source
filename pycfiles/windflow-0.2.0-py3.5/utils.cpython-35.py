# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/utils.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 495 bytes


def generate_repr_method(*columns):

    def __repr__(self):
        return '<{name}{space}{cols}>'.format(name=type(self).__name__, space=' ' if len(columns) else '', cols=' '.join('{c}={{self.{c}}}'.format(c=c) for c in columns)).format(self=self)

    return __repr__


def generate_str_method(*columns):

    def __str__(self):
        return ' '.join('{{self.{c}}}'.format(c=str(c)) for c in columns).format(self=self)

    return __str__