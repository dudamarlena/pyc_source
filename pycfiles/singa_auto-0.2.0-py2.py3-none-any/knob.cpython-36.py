# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/model/knob.py
# Compiled at: 2020-04-24 21:27:49
# Size of source mod 2**32: 9961 bytes
import abc
from typing import Union, List
POLICIES = [
 'SHARE_PARAMS', 'EARLY_STOP', 'SKIP_TRAIN', 'QUICK_EVAL', 'DOWNSCALE']

class KnobValue:
    __doc__ = '\n        Wrapper for a ``CategoricalValue``.\n    '

    def __init__(self, value: Union[(str, int, float, bool)]):
        self._value, self._dtype = self._parse_value(value)

    @property
    def value(self):
        return self._value

    @property
    def dtype(self) -> type:
        return self._dtype

    @staticmethod
    def _parse_value(value):
        value_type = None
        if isinstance(value, int):
            value_type = int
        else:
            if isinstance(value, float):
                value_type = float
            else:
                if isinstance(value, bool):
                    value_type = bool
                else:
                    if isinstance(value, str):
                        value_type = str
                    else:
                        raise TypeError('Only the following knob value data types are supported: `int`, `float`, `bool` or `str`')
        return (
         value, value_type)


CategoricalValue = Union[(str, int, float, bool, KnobValue)]

class BaseKnob(abc.ABC):
    __doc__ = '\n        The base class for a knob type.\n    '

    @property
    def value_type(self) -> type:
        raise NotImplementedError()


class CategoricalKnob(BaseKnob):
    __doc__ = '\n        Knob type representing a categorical value of type ``int``, ``float``, ``bool`` or ``str``.\n        ``values`` is a list of candidate cateogrical values for this knob type; a realization of this knob type would be an element of ``values``.\n    '

    def __init__(self, values: List[CategoricalValue]):
        self._values, self._value_type = self._validate_values(values)

    @property
    def value_type(self):
        return self._value_type

    @property
    def values(self) -> list:
        return self._values

    @staticmethod
    def _validate_values(values):
        values = [KnobValue(x) if not isinstance(x, KnobValue) else x for x in values]
        if len(values) == 0:
            raise ValueError('Length of `values` should at least 1')
        if any([values[0].dtype is not x.dtype for x in values]):
            raise TypeError('`values` should have elements of the same type')
        value_type = values[0].dtype
        return (
         values, value_type)


class FixedKnob(BaseKnob):
    __doc__ = '\n        Knob type representing a fixed value of type ``int``, ``float``, ``bool`` or ``str``.\n        Essentially, this represents a knob type that does not require tuning.\n    '

    def __init__(self, value: CategoricalValue):
        self._value = KnobValue(value) if not isinstance(value, KnobValue) else value
        self._value_type = self._value.dtype

    @property
    def value_type(self):
        return self._value_type

    @property
    def value(self):
        return self._value


class PolicyKnob(BaseKnob):
    __doc__ = '\n    Knob type representing whether a certain policy should be activated, as a boolean.\n    E.g. the ``EARLY_STOP`` policy knob decides whether the model should stop model training early, or not. \n    Offering the ability to activate different policies can optimize hyperparameter search for your model. \n    Activation of all policies default to false.\n\n    Refer to :ref:`model-policies` to understand how to use this knob type.\n    '

    def __init__(self, policy: str):
        if policy not in POLICIES:
            raise ValueError('Policy type must be one of {}'.format(POLICIES))
        self._policy = policy

    @property
    def value_type(self):
        return bool

    @property
    def policy(self):
        return self._policy


class IntegerKnob(BaseKnob):
    __doc__ = '\n    Knob type representing an ``int`` value within a specific interval [``value_min``, ``value_max``].\n    ``is_exp`` specifies whether the knob value should be scaled exponentially.\n    '

    def __init__(self, value_min: int, value_max: int, is_exp: bool=False):
        self._validate_values(value_min, value_max)
        self._value_min = value_min
        self._value_max = value_max
        self._is_exp = is_exp

    @property
    def value_type(self):
        return int

    @property
    def value_min(self) -> int:
        return self._value_min

    @property
    def value_max(self) -> int:
        return self._value_max

    @property
    def is_exp(self) -> bool:
        return self._is_exp

    @staticmethod
    def _validate_values(value_min, value_max):
        if not isinstance(value_min, int):
            raise ValueError('`value_min` should be an `int`')
        else:
            if not isinstance(value_max, int):
                raise ValueError('`value_max` should be an `int`')
            if value_min > value_max:
                raise ValueError('`value_max` should be at least `value_min`')


class FloatKnob(BaseKnob):
    __doc__ = '\n        Knob type representing a ``float`` value within a specific interval [``value_min``, ``value_max``].\n        ``is_exp`` specifies whether the knob value should be scaled exponentially.\n    '

    def __init__(self, value_min: float, value_max: float, is_exp: bool=False):
        self._validate_values(value_min, value_max)
        self._value_min = float(value_min)
        self._value_max = float(value_max)
        self._is_exp = is_exp

    @property
    def value_type(self):
        return float

    @property
    def value_min(self) -> float:
        return self._value_min

    @property
    def value_max(self) -> float:
        return self._value_max

    @property
    def is_exp(self) -> bool:
        return self._is_exp

    @staticmethod
    def _validate_values(value_min, value_max):
        if not isinstance(value_min, float):
            if not isinstance(value_min, int):
                raise ValueError('`value_min` should be a `float` or `int`')
        else:
            if not isinstance(value_max, float):
                if not isinstance(value_max, int):
                    raise ValueError('`value_max` should be a `float` or `int`')
            if value_min > value_max:
                raise ValueError('`value_max` should be at least `value_min`')


class ArchKnob(BaseKnob):
    __doc__ = "\n        Knob type representing part of a model's architecture as a fixed-size list of categorical values. \n        ``items`` is a list of list of candidate categorical values; a realization of this knob type would be a list of categorical values, wIth the value at each index matching an element of the list of candidates at that index.\n        \n        To illustrate, the following can be a definition of 3-layer model's architecture search space inspired by the ENAS cell architecture construction strategy:\n\n        ::\n\n            l0 = KnobValue(0) # Input layer as input connection\n            l1 = KnobValue(1) # Layer 1 as input connection\n            l2 = KnobValue(2) # Layer 2 as input connection\n            ops = [KnobValue('conv3x3'), KnobValue('conv5x5'), KnobValue('avg_pool'), KnobValue('max_pool')]\n            arch_knob = ArchKnob([\n                [l0], ops, [l0], ops,                   # To form layer 1, choose input 1, op on input 1, input 2, op on input 2, then combine post-op inputs as preferred                                     \n                [l0, l1], ops, [l0, l1], ops,           # To form layer 2, ...\n                [l0, l1, l2], ops, [l0, l1, l2], ops,   # To form layer 3, ...\n            ])\n            \n\n        If the same ``KnobValue`` instance is reused at different indices in ``items``, they are considered to be *semantically* identical for the purposes of architecture search.\n        For example, in the above code snippet, the meaning of ``l0`` in the 1st item index and ``l0`` in the 3rd item index are identical - they refer to an input connection from the input layer.  \n\n        It is assumed that the realization of components of the architecture `later` in the list is influenced by the components of architecture `earlier` in the list. \n        For example, which operation is to be applied on an input (e.g. which value in ``ops``) is somewhat dependent on the source of the input (e.g. which value in ``[l0, l1, l2]``).\n\n        Note that the exact model architecture space is not fully described with this knob - it still depends on how the model code constructs the computation graph and implements the various building blocks of the model. \n\n        Encoding of the architecture with ``ArchKnob`` can be flexibly defined as necessary. You can search only over operations and have the connections in the architecture already hard-coded\n        as part of the model, or you can search only over input indices of various layers and have operations already decided. \n    "

    def __init__(self, items: List[List[CategoricalValue]]):
        self._items = self._validate_values(items)

    @property
    def value_type(self):
        return list

    @property
    def items(self) -> List[List[CategoricalValue]]:
        return self._items

    def __len__(self):
        return len(self._items)

    @staticmethod
    def _validate_values(items):
        for i, values in enumerate(items):
            items[i] = [KnobValue(x) if not isinstance(x, KnobValue) else x for x in values]

        return items