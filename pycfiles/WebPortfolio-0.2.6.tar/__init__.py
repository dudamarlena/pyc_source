# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/web-portfolio/webportfolio/__init__.py
# Compiled at: 2015-10-23 05:42:54
"""
WebPortfolio

"""
from core import *
from decorators import *

class ViewError(Exception):
    pass


class ModelError(Exception):
    pass