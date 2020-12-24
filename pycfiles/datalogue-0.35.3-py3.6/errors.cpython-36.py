# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/errors.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 1329 bytes
from typing import Optional

class DtlError(Exception):

    def __init__(self, message, cause=None):
        super(DtlError, self).__init__(message)
        self.message = message
        self.cause = cause

    def __repr__(self):
        return f"DtlError({self.message} {str(self.cause)})"

    def __eq__(self, other: 'DtlError'):
        if isinstance(self, other.__class__):
            return self.message == other.message
        else:
            return False


def _enum_parse_error(enum_description: str, string: str) -> str:
    return "'%s' is not a valid %s" % (string, enum_description)


def _property_not_found(property_name: str, obj: dict) -> DtlError:
    return DtlError(f"Could not find '{property_name}' in the dictionary: {obj!r}")


def _invalid_property_type(property_name: str, expected: str, obj: dict) -> DtlError:
    return DtlError(f"Property '{property_name}' was expected to be '{expected}' in {obj!r}")


def _invalid_parameter_error(reason: str, class_or_function: str) -> DtlError:
    return DtlError(f"Failed to call/create {class_or_function} because {reason}")


def _invalid_pagination_params(param_name: str) -> DtlError:
    return DtlError(f"The parameter '{param_name}' must be a positive integer")