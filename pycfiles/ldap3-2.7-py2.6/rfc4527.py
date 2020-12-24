# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\rfc4527.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from .. import NO_ATTRIBUTES, ALL_ATTRIBUTES, STRING_TYPES
from ..operation.search import build_attribute_selection
from .controls import build_control

def _read_control(oid, attributes, criticality=False):
    if not attributes:
        attributes = [
         NO_ATTRIBUTES]
    elif attributes == ALL_ATTRIBUTES:
        attributes = [
         ALL_ATTRIBUTES]
    if isinstance(attributes, STRING_TYPES):
        attributes = [
         attributes]
    value = build_attribute_selection(attributes, None)
    return build_control(oid, criticality, value)


def pre_read_control(attributes, criticality=False):
    """Create a pre-read control for a request.
    When passed as a control to the controls parameter of an operation, it will
    return the value in `Connection.result` before the operation took place.
    """
    return _read_control('1.3.6.1.1.13.1', attributes, criticality)


def post_read_control(attributes, criticality=False):
    """Create a post-read control for a request.
    When passed as a control to the controls parameter of an operation, it will
    return the value in `Connection.result` after the operation took place.
    """
    return _read_control('1.3.6.1.1.13.2', attributes, criticality)