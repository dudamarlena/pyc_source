# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/interfaces.py
# Compiled at: 2011-01-11 16:22:56
from zope.interface import Interface

class IZentinelTool(Interface):
    """
    Zentinel skin
    """
    __module__ = __name__


class IZenReportTool(Interface):
    """
    Reporting tool singleton/plugin for reports ...
    """
    __module__ = __name__