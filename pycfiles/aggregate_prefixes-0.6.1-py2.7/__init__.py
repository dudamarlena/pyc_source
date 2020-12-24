# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aggregate_prefixes/__init__.py
# Compiled at: 2019-06-24 08:30:52
"""
Aggregates IPv4 or IPv6 prefixes.

Core method is aggrega_prefixes in module aggregate_prefixes.
It gets an unsorted list IPv4 or IPv6 prefixes and returns a sorted list of aggregates.

Example:
        >>> from aggregate_prefixes.aggregate_prefixes import aggregate_prefixes
        >>>
        >>> prefixes = ["192.0.2.1/32", "192.0.2.3/32", "192.0.2.2/32"]
        >>> print aggregate_prefixes(prefixes)
        ['192.0.2.1/32', '192.0.2.2/31']
        >>>
"""
from __future__ import absolute_import
from .aggregate_prefixes import aggregate_prefixes
from .__about__ import __version__, __author__, __author_email__, __url__, __description__, __license__, __classifiers__