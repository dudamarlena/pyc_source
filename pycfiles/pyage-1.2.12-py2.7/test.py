# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/test.py
# Compiled at: 2015-12-21 16:57:03
import sys, Pyro4, Pyro4.util
from pyage.core.agent import Agent
from pyage.core.query import query_property
from pyage.core.migration import migrate_agent
sys.excepthook = Pyro4.util.excepthook
print query_property('workspace.Max.4811', 'makz', 'fitness')
print '!'