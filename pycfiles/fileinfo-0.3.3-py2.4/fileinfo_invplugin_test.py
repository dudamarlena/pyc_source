# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/test/fileinfo_invplugin_test.py
# Compiled at: 2008-06-08 17:16:28
"""Contains a test investigator.

"""
from fileinfo.investigator import BaseInvestigator

class TestInvestigator(BaseInvestigator):
    """A class for determining attributes of files."""
    __module__ = __name__
    attrMap = {'foo': 'getFoo'}
    totals = ()

    def activate(self):
        """Try activating self, setting 'active' variable."""
        self.active = True
        return self.active

    def getFoo(self):
        """Return 'bar'."""
        return 'bar'