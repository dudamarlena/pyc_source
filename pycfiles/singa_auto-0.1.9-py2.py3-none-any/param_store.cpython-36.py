# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/param_store/param_store.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 3136 bytes
import abc, msgpack, traceback, numpy as np
from singa_auto.model import Params

class InvalidParamsFormatError(Exception):
    pass


PARAM_DATA_TYPE_SEPARATOR = '//'
PARAM_DATA_TYPE_NUMPY = 'NP'

class ParamStore(abc.ABC):
    __doc__ = '\n        Persistent store for model parameters.\n    '

    @abc.abstractmethod
    def save(self, params: Params) -> str:
        """
            Persists a set of parameters, returning a unique ID for the params.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, params_id: str) -> Params:
        """
            Loads persisted parameters, identified by ID.
        """
        raise NotImplementedError()

    @staticmethod
    def _serialize_params(params):
        params_simple = _simplify_params(params)
        params_bytes = msgpack.packb(params_simple, use_bin_type=True)
        return params_bytes

    @staticmethod
    def _deserialize_params(params_bytes):
        params_simple = msgpack.unpackb(params_bytes, raw=False)
        params = _unsimplify_params(params_simple)
        return params


def _simplify_params(params):
    try:
        params_simple = {}
        assert isinstance(params, dict)
        for name, value in params.items():
            if not isinstance(name, str):
                raise AssertionError
            else:
                assert PARAM_DATA_TYPE_SEPARATOR not in name
                if isinstance(value, np.ndarray):
                    name = f"{PARAM_DATA_TYPE_NUMPY}{PARAM_DATA_TYPE_SEPARATOR}{name}"
                    value = value.tolist()
                elif not isinstance(value, (str, float, int)):
                    raise AssertionError
            params_simple[name] = value

        return params_simple
    except:
        traceback.print_stack()
        raise InvalidParamsFormatError()


def _unsimplify_params(params_simple):
    params = {}
    for name, value in params_simple.items():
        if PARAM_DATA_TYPE_SEPARATOR in name:
            type_id, name = name.split(PARAM_DATA_TYPE_SEPARATOR)
            if type_id == PARAM_DATA_TYPE_NUMPY:
                value = np.array(value)
        params[name] = value

    return params