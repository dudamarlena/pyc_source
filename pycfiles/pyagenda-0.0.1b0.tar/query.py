# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/query.py
# Compiled at: 2015-12-21 17:12:58
import Pyro4

def query_property(workspace_name, agent_address, property):
    workspace = Pyro4.Proxy('PYRONAME:' + workspace_name)
    agent = workspace.get_agent(agent_address)
    return getattr(agent, property)