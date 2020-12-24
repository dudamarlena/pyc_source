# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/map_function.py
# Compiled at: 2020-05-07 16:37:14
# Size of source mod 2**32: 1199 bytes
from typing import Union
from datalogue.errors import DtlError, _property_not_found
from datalogue.models.transformations.commons import Transformation

class MapFunction(Transformation):
    __doc__ = '\n    Applies a given function to an ADG that should return and ADG\n\n    It should be of the form:\n\n    (adg: ADG, env: MAP) => {\n        // Here the content of function goes\n    }\n\n    ALPHA Feature\n    '
    type_str = 'MapFunction'

    def __init__(self, f: str):
        """
        :param f: function to be applied to the adg
        """
        Transformation.__init__(self, MapFunction.type_str)
        self.f = f

    def __eq__(self, other: 'MapFunction'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"MapFunction(f: {self.f!r})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['f'] = self.f
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'MapFunction')]:
        f = json.get('f')
        if f is None:
            return _property_not_found('f', json)
        else:
            return MapFunction(f)