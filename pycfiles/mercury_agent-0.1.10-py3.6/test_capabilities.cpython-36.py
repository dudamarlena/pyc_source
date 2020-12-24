# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_capabilities.py
# Compiled at: 2018-02-03 12:28:05
# Size of source mod 2**32: 2290 bytes
"""Unit tests for mercury_agent.capabilities"""
import mock
from mercury_agent import capabilities

def test_add_capability():
    """Test add_capability()"""
    capabilities.add_capability('c_entry', 'c_name', 'Capability Description')
    if not 'c_name' in capabilities.runtime_capabilities:
        raise AssertionError
    else:
        fake_capability = capabilities.runtime_capabilities['c_name']
        assert fake_capability['name'] == 'c_name'
        assert fake_capability['entry'] == 'c_entry'
        assert fake_capability['description'] == 'Capability Description'
    del capabilities.runtime_capabilities['c_name']


@mock.patch('mercury_agent.capabilities.add_capability')
def test_capability(mock_add_capability):
    """Test @capability() decorator"""

    @capabilities.capability('c_name', 'Capability Description', num_args=1)
    def c_entry(x):
        """Return input."""
        return x

    c_entry('foo')
    mock_add_capability.assert_called_once_with(c_entry, 'c_name',
      'Capability Description',
      num_args=1,
      doc='Return input.',
      serial=False,
      kwarg_names=None,
      no_return=False,
      dependency_callback=None,
      timeout=1800,
      task_id_kwargs=False)