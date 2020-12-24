# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/ceph_osd_tree.py
# Compiled at: 2019-05-16 13:41:33
"""
CephOsdTree
===========

Combiner provides the information about ceph osd tree. It
uses the results of the ``CephOsdTree``, ``CephInsights`` and ``CephOsdTreeText`` parsers.
The order from most preferred to least preferred is ``CephOsdTree``, ``CephInsights``, ``CephOsdTreeText``.

Examples:
    >>> type(cot)
    <class 'insights.combiners.ceph_osd_tree.CephOsdTree'>
    >>> cot['nodes'][0]['children']
    [-7, -3, -5, -9]
"""
from insights.core.plugins import combiner
from insights import LegacyItemAccess
from insights.parsers.ceph_cmd_json_parsing import CephOsdTree as CephOsdTreeParser
from insights.parsers.ceph_insights import CephInsights
from insights.parsers.ceph_osd_tree_text import CephOsdTreeText

@combiner([CephOsdTreeParser, CephInsights, CephOsdTreeText])
class CephOsdTree(LegacyItemAccess):
    """
    Combiner provides the information about ceph osd tree. It
    uses the results of the ``CephOsdTree``, ``CephInsights`` and ``CephOsdTreeText`` parsers.
    The order from most preferred to least preferred is ``CephOsdTree``, ``CephInsights``, ``CephOsdTreeText``.
    """

    def __init__(self, cot, ci, cott):
        if cot:
            self.data = cot
        elif ci:
            self.data = ci.data['osd_tree']
        else:
            self.data = cott