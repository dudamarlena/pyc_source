# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/json/decoder.py
# Compiled at: 2016-04-07 08:23:49
# Size of source mod 2**32: 1283 bytes
import json, py3o.types as types

class Py3oJSONDecoder(json.JSONDecoder):
    """Py3oJSONDecoder"""

    def __init__(self, config=None, *args, **kwargs):
        if config is None:
            config = {}
        if not isinstance(config, types.Py3oTypeConfig):
            config = types.Py3oTypeConfig(**config)
        self.config = config
        super(Py3oJSONDecoder, self).__init__(object_hook=self._py3o_object_hook, parse_int=config.integer, parse_float=config.float, *args, **kwargs)

    def _py3o_object_hook(self, dct):
        py3o_type = dct.get('_py3o')
        if py3o_type is None:
            return dct
        val = dct.get('val')
        if py3o_type == 'date':
            res = self.config.date.strptime(val, '%Y%m%d')
        else:
            if py3o_type == 'time':
                res = self.config.time.strptime(val, '%H%M%S')
            else:
                if py3o_type == 'dt':
                    res = self.config.datetime.strptime(val, '%Y%m%d%H%M%S')
                else:
                    raise ValueError('Unknown type {}'.format(py3o_type))
        return res