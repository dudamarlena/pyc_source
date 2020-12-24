# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/__init__.py
# Compiled at: 2014-04-17 10:56:25
__all__ = [
 'run', 'run_ec2', 'run_map', 'run_reduce', 'get_config', 'get_default_config']
from .main import run
from .ec2 import run as run_ec2
from .map import run as run_map
from .reduce import run as run_reduce
from .config import get_config, get_default_config
from .version import __version__