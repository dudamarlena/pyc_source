# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/napalm_aos/__init__.py
# Compiled at: 2019-06-13 23:53:04
"""napalm_aos package."""
import pkg_resources
from napalm_aos.aos import AOSDriver
try:
    __version__ = pkg_resources.get_distribution('napalm-aos').version
except pkg_resources.DistributionNotFound:
    __version__ = 'Not installed'

__all__ = ['AOSDriver']