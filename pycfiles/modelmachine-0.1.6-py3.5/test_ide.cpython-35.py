# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/tests/test_ide.py
# Compiled at: 2016-02-09 07:36:55
# Size of source mod 2**32: 723 bytes
"""Test case for IDE."""
from unittest.mock import create_autospec
from pytest import raises
from modelmachine import ide
from modelmachine.cpu import AbstractCPU

def test_get_cpu():
    """Test define cpu method."""
    ide.CPU_LIST = {'abstract_cpu_test': create_autospec(AbstractCPU, True)}
    with raises(ValueError):
        ide.get_cpu(['not_found_cpu', '[config]', '[code]', '00 00', '[input]'], False)
    with raises(ValueError):
        ide.get_cpu(['[config]', '[code]', '00 00', '[input]'], False)
    cpu = ide.get_cpu(['abstract_cpu_test', '[config]', 'key=value',
     '[code]', '00 00', '99 00', '[input]'], False)
    assert isinstance(cpu, AbstractCPU)