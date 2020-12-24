# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/test.py
# Compiled at: 2015-12-21 16:57:03
import sys, Pyro4, Pyro4.util
from pyage.core.agent import Agent
from pyage.core.query import query_property
from pyage.core.migration import migrate_agent
sys.excepthook = Pyro4.util.excepthook
print query_property('workspace.Max.4811', 'makz', 'fitness')
print '!'