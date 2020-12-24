# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/__init__.py
# Compiled at: 2015-07-22 23:54:21
"""A collection of tools and helpers for use with Django."""
from collections import namedtuple
version_info_t = namedtuple('version_info_t', ('major', 'minor', 'micro', 'releaselevel',
                                               'serial'))
VERSION = version_info_t(0, 3, 2, '', '')
__version__ = ('{0.major}.{0.minor}.{0.micro}{0.releaselevel}').format(VERSION)
__author__ = 'Alex Hayes'
__contact__ = 'alex@alution.com'
__homepage__ = 'https://github.com/alexhayes/django-toolkit'
__docformat__ = 'restructuredtext'