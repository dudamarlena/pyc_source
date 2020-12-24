# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/tal/interfaces.py
# Compiled at: 2012-07-12 02:08:15
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class IWorkflowTalesAPI(Interface):
    """'wf' TALES namespace interface"""

    def status(self):
        """Get status label of the adapted content"""
        pass

    def published(self):
        """Check if adapted content is published"""
        pass

    def visible(self):
        """Check if adapted content is visible"""
        pass