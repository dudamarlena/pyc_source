# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/vcp/test_vcp/test_vcp_codes.py
# Compiled at: 2019-11-29 22:48:56
# Size of source mod 2**32: 3036 bytes
import pytest, voluptuous as vol
from ..vcp_codes import VCPCode, get_vcp_code_definition
VCP_CODE_SCHEMA = vol.Schema({vol.Required('name'): str, 
 vol.Required('value'): int, 
 vol.Required('type'): vol.Any('rw', 'ro', 'wo'), 
 vol.Required('function'): vol.Any('c', 'nc', 't')})

@pytest.fixture(scope='module', params=(VCPCode._VCP_CODE_DEFINTIONS.keys()))
def vcp_definition(request):
    return get_vcp_code_definition(request.param)


def test_vcp_code_schema(vcp_definition):
    VCP_CODE_SCHEMA(vcp_definition.definition)


@pytest.mark.parametrize('property', ['name', 'value', 'type', 'function'])
def test_properties(vcp_definition, property):
    getattr(vcp_definition, property)


def test_repr(vcp_definition):
    repr(vcp_definition)


@pytest.mark.parametrize('test_type, readable', [('ro', True), ('wo', False), ('rw', True)])
def test_readable(test_type, readable):
    code = VCPCode({'type': test_type})
    assert code.readable == readable


@pytest.mark.parametrize('test_type, writeable', [('ro', False), ('wo', True), ('rw', True)])
def test_writeable(test_type, writeable):
    code = VCPCode({'type': test_type})
    assert code.writeable == writeable


def test_properties_value():
    """ Test that dictionary values propagate to properties. """
    test_name = 'unit test'
    test_value = 4886718345
    test_type = 'unit test type'
    test_function = 'unit test value'
    test_definition = {'name':test_name, 
     'value':test_value, 
     'type':test_type, 
     'function':test_function}
    code = VCPCode(test_definition)
    if not code.name == test_name:
        raise AssertionError
    else:
        if not code.value == test_value:
            raise AssertionError
        elif not code.type == test_type:
            raise AssertionError
        assert code.function == test_function