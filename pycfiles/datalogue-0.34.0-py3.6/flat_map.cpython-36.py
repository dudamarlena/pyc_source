# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/flat_map.py
# Compiled at: 2020-04-24 18:45:43
# Size of source mod 2**32: 1099 bytes
from typing import List, Union
from datalogue.errors import DtlError
from datalogue.models.transformations.commons import Transformation

class FlatMap(Transformation):
    __doc__ = '\n    Creates multiple ADGs from one ADG and put each child into the given path of the new ADG.\n\n    '
    type_str = 'FlatMap'

    def __init__(self, on: List[str]):
        """
        :param on: array of string that represents the path where to put created ADGs 
        """
        Transformation.__init__(self, FlatMap.type_str)
        self.on = on

    def __eq__(self, other: 'FlatMap'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"FlatMap(on: {'.'.join(self.on)})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['on'] = self.on
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'FlatMap')]:
        on = json.get('on')
        if isinstance(on, DtlError):
            return on
        else:
            return FlatMap(on)