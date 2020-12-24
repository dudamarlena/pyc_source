# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/__init__.py
# Compiled at: 2011-10-03 21:41:12
try:
    try:
        __import__('pkg_resources').declare_namespace('kaa')
        __import__('pkg_resources').get_distribution('kaa-base').activate()
    except __import__('pkg_resources').DistributionNotFound:
        pass

except ImportError:
    pass

from kaa.base import *