# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/asvmq/__init__.py
# Compiled at: 2019-01-31 09:41:23
# Size of source mod 2**32: 268 bytes
"""This python package contains the Python Module version number
and it contains the major base classes required to do communication in the ASV"""
__version__ = '0.1.6'
from .topic_communications import Publisher, Subscriber, log_debug, log_info, log_warn, log_fatal