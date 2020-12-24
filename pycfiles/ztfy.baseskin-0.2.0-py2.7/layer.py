# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/layer.py
# Compiled at: 2014-03-19 06:22:09
from z3c.form.interfaces import IFormLayer
from z3c.formui.interfaces import IFormUILayer
from z3c.jsonrpc.layer import IJSONRPCLayer
from z3c.layer.pagelet import IPageletBrowserLayer

class IBaseSkinLayer(IFormLayer, IFormUILayer, IPageletBrowserLayer, IJSONRPCLayer):
    """Base skin layer"""
    pass