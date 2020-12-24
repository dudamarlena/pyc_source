# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/noop.py
# Compiled at: 2010-09-20 14:05:31
"""
Do nothing with input
"""
__rcsid__ = '$Id: noop.py 25224 2010-09-20 18:05:30Z dang $'
__author__ = 'Dan Gunter'
from netlogger.analysis.modules import _base

class Analyzer(_base.Analyzer):
    """Copy input to output.
    """

    def __init__(self, **kw):
        """Constructor.
        """
        _base.Analyzer.__init__(self, **kw)

    def process(self, data):
        pass