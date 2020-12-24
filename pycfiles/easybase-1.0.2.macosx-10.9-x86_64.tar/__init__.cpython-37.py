# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/__init__.py
# Compiled at: 2019-12-20 08:50:03
# Size of source mod 2**32: 534 bytes
"""
EasyBase, a developer-friendly Python library to interact with Apache
HBase. Support Time-Range scan and multi-version access
"""
from pkg_resources import resource_filename
import thriftpy2
thriftpy2.load((resource_filename('easybase', 'HBase.thrift')),
  module_name='HBase_thrift')
from ._version import __version__
from .connection import DEFAULT_HOST, DEFAULT_PORT, Connection
from .table import Table
from .pool import ConnectionPool, NoConnectionsAvailable