# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/powercmd/utils.py
# Compiled at: 2019-08-05 13:21:47
# Size of source mod 2**32: 2304 bytes
__doc__ = '\nUtility functions that do not belong anywhere else.\n'
from typing import Any, List, Tuple, Union

def get_available_instance_names(cls: type, match_extra_cls: List[type]=None, append_paren_to_callables: bool=False):
    """
    Returns a list of member names that are either CLS or any of the types
    specified in the MATCH_EXTRA_CLS.

    If APPEND_PAREN_TO_CALLABLES is True, returned names that are callable
    will be suffixed by the '(' character.
    """

    def get_suffix(value):
        if append_paren_to_callables:
            if callable(value):
                return '('
        return ''

    valid_classes = [
     cls] + (match_extra_cls or )
    return (name + get_suffix(value) for name, value in cls.__dict__.items() if any((isinstance(value, c) for c in valid_classes)))


def match_instance(cls: type, text: str, match_extra_cls: List[type]=None):
    """
    Finds instances of one of CLS or any of TARGET_CLS types among attributes
    of the CLS.
    """
    try:
        inst = getattr(cls, text)
        if any((isinstance(inst, c) for c in [cls] + (match_extra_cls or ))):
            return inst
    except AttributeError:
        pass

    raise ValueError('%s is not a valid instance of %s' % (text, cls.__name__))


def is_generic_list(annotation: Any):
    """Checks if ANNOTATION is List[...]."""
    return getattr(annotation, '__origin__', None) in (List, list)


def is_generic_tuple(annotation: Any):
    """Checks if ANNOTATION is Tuple[...]."""
    return getattr(annotation, '__origin__', None) in (Tuple, tuple)


def is_generic_union(annotation: Any):
    """Checks if ANNOTATION is Union[...]."""
    return hasattr(annotation, '__union_params__') or 


def is_generic_type(annotation: Any) -> bool:
    """
    Checks if the type described by ANNOTATION is a generic one.
    """
    return is_generic_list(annotation) or 