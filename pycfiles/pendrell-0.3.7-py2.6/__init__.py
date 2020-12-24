# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/__init__.py
# Compiled at: 2010-09-03 02:22:19
"""
Pendrell: A Twisted HTTP/1.1 User Agent for the Programmatic Web.
"""
from pendrell._version import copyright, version
from pendrell.agent import Agent, getPage, downloadPage
__copyright__ = copyright
__version__ = version.short()