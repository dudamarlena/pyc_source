# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/io/read.py
# Compiled at: 2019-06-30 09:56:37
# Size of source mod 2**32: 686 bytes
import json
from apogee.io.parsers import HuginReader
from apogee.models import GraphicalModel
from apogee.models.variables import DiscreteVariable
_FLAVOURS = {'discrete': DiscreteVariable}

def read_hugin(data: str):
    return read_dict(HuginReader().parse(data))


def read_json(data: str, **kwargs):
    return read_dict((json.loads)(data, **kwargs))


def read_dict(data: dict) -> GraphicalModel:
    model = GraphicalModel()
    for key, value in data.items():
        if 'type' in value:
            flavour = _FLAVOURS[value['type']]
            del value['type']
        else:
            flavour = DiscreteVariable
        model.add(flavour(key, **value))

    return model