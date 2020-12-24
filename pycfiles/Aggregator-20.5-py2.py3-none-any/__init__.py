# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aggregate_prefixes/__init__.py
# Compiled at: 2019-06-24 08:30:52
__doc__ = '\nAggregates IPv4 or IPv6 prefixes.\n\nCore method is aggrega_prefixes in module aggregate_prefixes.\nIt gets an unsorted list IPv4 or IPv6 prefixes and returns a sorted list of aggregates.\n\nExample:\n\t>>> from aggregate_prefixes.aggregate_prefixes import aggregate_prefixes\n\t>>>\n\t>>> prefixes = ["192.0.2.1/32", "192.0.2.3/32", "192.0.2.2/32"]\n\t>>> print aggregate_prefixes(prefixes)\n\t[\'192.0.2.1/32\', \'192.0.2.2/31\']\n\t>>>\n'
from __future__ import absolute_import
from .aggregate_prefixes import aggregate_prefixes
from .__about__ import __version__, __author__, __author_email__, __url__, __description__, __license__, __classifiers__