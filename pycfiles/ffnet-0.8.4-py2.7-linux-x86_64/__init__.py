# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/__init__.py
# Compiled at: 2018-10-28 11:56:52
"""
-------------
ffnet package
-------------
"""
from __future__ import absolute_import
from ._version import version
import ffnet.fortran as fortran, ffnet.ffnet as ffnetmodule
from ffnet.ffnet import ffnet, mlgraph, tmlgraph, imlgraph, savenet, loadnet, exportnet, readdata
from ffnet.pikaia import pikaia
import ffnet._tests as _tests