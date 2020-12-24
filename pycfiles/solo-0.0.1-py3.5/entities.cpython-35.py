# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/server/entities.py
# Compiled at: 2016-03-03 02:09:43
# Size of source mod 2**32: 777 bytes
import json
from typing import Optional, Dict, Any, Iterable

class BaseEntity:
    FIELDS = tuple()
    IN_MODIFIERS = {}
    OUT_MODIFIERS = {'str': str, 
     'json': json.dumps}
    DEFAULT_MODIFIERS = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self, *fields: Iterable[str]) -> Dict[(str, Any)]:
        if not fields:
            fields = self.FIELDS
        rv = {}
        out_modifiers = self.OUT_MODIFIERS
        for f in fields:
            field, *modifiers = f.split('|')
            field = field.strip()
            v = getattr(self, field)
            for m in modifiers:
                v = out_modifiers[m.strip()](v)

            rv[field] = v

        return rv