# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/__init__.py
# Compiled at: 2019-07-09 10:49:45
# Size of source mod 2**32: 508 bytes
"""
Package Description.
"""
from ._version import __version__
__short_description__ = 'Package short description.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from troposphere import *
    from troposphere import AWSObject as TroposphereAWSObject
    from .core.associate import associate
    from .core.mate import Template, AWSObject
except ImportError as e:
    pass