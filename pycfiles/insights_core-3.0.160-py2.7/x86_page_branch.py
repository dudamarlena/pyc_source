# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/x86_page_branch.py
# Compiled at: 2019-11-14 13:57:46
"""
X86PageBranch - combiner for x86 kernel features:
=================================================

x86 kernel features includes:
    * PTI (Page Table Isolation)
    * IBPB (Indirect Branch Prediction Barrier)
    * IBRS (Indirect Branch Restricted Speculation)

This combiner reads information from debugfs:

Examples:
    >>> type(dv)
    <class 'insights.combiners.x86_page_branch.X86PageBranch'>
    >>> dv.pti
    1
    >>> dv.ibpb
    3
    >>> dv.ibrs
    2
    >>> dv.retp
    0

    Attributes:
        pti (int): The result parsed of '/sys/kernel/debug/x86/pti_enabled'

        ibpb (int): The result parsed of '/sys/kernel/debug/x86/ibpb_enabled'

        ibrs (int): The result parsed of '/sys/kernel/debug/x86/ibrs_enabled'

        retp (int): The result parsed of '/sys/kernel/debug/x86/retp_enabled'
"""
from insights.core.plugins import combiner
from insights.parsers.x86_debug import X86PTIEnabled, X86IBPBEnabled, X86IBRSEnabled, X86RETPEnabled

@combiner(X86PTIEnabled, X86IBPBEnabled, X86IBRSEnabled, optional=[X86RETPEnabled])
class X86PageBranch(object):
    """
    This combiner provides an interface to the three X86 Page Table/Branch Prediction parsers.
    If retp_enabled is not available, self.retp is None.
    """

    def __init__(self, pti_enabled, ibpb_enabled, ibrs_enabled, retp_enabled):
        self.pti = pti_enabled.value
        self.ibpb = ibpb_enabled.value
        self.ibrs = ibrs_enabled.value
        self.retp = None
        if retp_enabled:
            self.retp = retp_enabled.value
        return