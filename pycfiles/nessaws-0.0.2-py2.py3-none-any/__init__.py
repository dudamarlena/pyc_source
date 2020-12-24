# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adamstauffer/Desktop/TerbiumCode/Github/nessaws/src/nessaws/__init__.py
# Compiled at: 2017-03-10 11:19:35
"""nessaws: Automate Nessus scans against AWS EC2/RDS endpoints."""
from __future__ import absolute_import
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'