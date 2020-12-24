# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tonio/sources/odooselenium/odooselenium/__init__.py
# Compiled at: 2016-12-06 01:58:53
"""odooselenium provides tools to interact with Odoo using Selenium."""
import pkg_resources
from odooselenium.api import *
__version__ = pkg_resources.get_distribution(__package__).version