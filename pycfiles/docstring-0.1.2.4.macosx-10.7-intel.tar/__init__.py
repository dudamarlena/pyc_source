# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eytan/Envs/docstring/lib/python2.7/site-packages/docstring/__init__.py
# Compiled at: 2012-11-28 17:44:53
"""
A module that enables generating HTML documentation out of docstrings.
Currently it is used for annotating django/tornado api endpoints.
"""
__title__ = 'docstring'
__version__ = '0.1.2.4'
__build__ = 5121
__author__ = 'Eytan Daniyalzade'
__license__ = 'ISC'
from utils import Endpoint
from utils import get_api_doc