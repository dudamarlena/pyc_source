# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/model.py
# Compiled at: 2018-04-23 11:23:30
# Size of source mod 2**32: 2217 bytes
import os, stat
from rumba.elements.topology import DIF, ShimEthDIF, ShimUDPDIF, NormalDIF, IPCP, ShimEthIPCP, ShimUDPIPCP, Node, SSHConfig, LinkQuality, Delay, Loss, Distribution
from rumba.elements.experimentation import Experiment, Testbed, Executor, tmp_dir
__all__ = [
 'DIF',
 'ShimEthDIF',
 'ShimUDPDIF',
 'NormalDIF',
 'IPCP',
 'ShimEthIPCP',
 'ShimUDPIPCP',
 'Node',
 'SSHConfig',
 'LinkQuality',
 'Delay',
 'Loss',
 'Distribution',
 'Experiment',
 'Testbed',
 'Executor',
 'tmp_dir',
 'cache_dir']
try:
    os.mkdir(tmp_dir)
    os.chmod(tmp_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
except OSError:
    pass

cache_parent_dir = os.path.join(os.path.expanduser('~'), '.cache/')
try:
    os.mkdir(cache_parent_dir)
except OSError:
    pass

cache_dir = os.path.join(os.path.expanduser('~'), '.cache/rumba/')
try:
    os.mkdir(cache_dir)
except OSError:
    pass