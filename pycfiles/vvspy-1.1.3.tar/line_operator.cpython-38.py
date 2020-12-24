# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\line_operator.py
# Compiled at: 2019-12-07 13:33:32
# Size of source mod 2**32: 688 bytes


class LineOperator:
    __doc__ = '\n\n       Describes the operator of a :class:`Connection`.\n\n       Attributes\n       -----------\n\n       raw :class:`dict`\n           Raw dict received by the API.\n       id :class:`str`\n           id of the operator.\n       name :class:`str`\n           display name of the operator.\n       public_code :class:`str`\n           public_code of the operator.\n    '

    def __init__(self, **kwargs):
        self.raw = kwargs
        self.id = kwargs.get('code', kwargs.get('id'))
        self.name = kwargs.get('name')
        self.public_code = kwargs.get('publicCode')

    def __str__(self):
        return f"{self.name} ({self.id})"