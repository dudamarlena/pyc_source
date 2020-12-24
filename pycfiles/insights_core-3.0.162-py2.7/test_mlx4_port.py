# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mlx4_port.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from insights.tests import context_wrap
from insights.parsers import mlx4_port
from insights.parsers.mlx4_port import Mlx4Port
MLX4_CONTENT = '\nib\n'
MLX4_CONTENT_ML = '  line 1\n  line 2'
MLX4_PATH = '/sys/bus/pci/devices/0000:0c:00.0/mlx4_port1'

def test_mlx4_port():
    result = Mlx4Port(context_wrap(MLX4_CONTENT, path=MLX4_PATH))
    assert result.name == 'mlx4_port1'
    assert result.contents == ['ib']
    result = Mlx4Port(context_wrap(MLX4_CONTENT_ML, path=MLX4_PATH))
    assert result.name == 'mlx4_port1'
    assert result.contents == ['line 1', 'line 2']


def test_mlx4_docs():
    env = {'mlx4_port': Mlx4Port(context_wrap(MLX4_CONTENT, path=MLX4_PATH))}
    failed, total = doctest.testmod(mlx4_port, globs=env)
    assert failed == 0