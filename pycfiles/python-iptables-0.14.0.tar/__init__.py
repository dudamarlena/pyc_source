# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vilmos/Projects/python-iptables/iptc/__init__.py
# Compiled at: 2018-04-16 20:15:10
"""
.. module:: iptc
   :synopsis: Python bindings for libiptc.

.. moduleauthor:: Vilmos Nebehaj
"""
from iptc.ip4tc import is_table_available, Table, Chain, Rule, Match, Target, Policy, IPTCError
from iptc.ip6tc import is_table6_available, Table6, Rule6
from iptc.errors import *
__all__ = []