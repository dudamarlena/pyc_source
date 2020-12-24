# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opendxl/viji/opendxl-console/dxlconsole/__init__.py
# Compiled at: 2019-06-07 18:26:01
from __future__ import absolute_import
from ._version import __version__
from .app import OpenDxlConsole

def get_version():
    """
    Returns the version of the package

    :return: The version of the package
    """
    return __version__