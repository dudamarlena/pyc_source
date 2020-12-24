# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/query.py
# Compiled at: 2015-12-21 17:12:58
import Pyro4

def query_property(workspace_name, agent_address, property):
    workspace = Pyro4.Proxy('PYRONAME:' + workspace_name)
    agent = workspace.get_agent(agent_address)
    return getattr(agent, property)