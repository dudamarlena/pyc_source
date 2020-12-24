# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/node.py
# Compiled at: 2010-10-14 14:04:22
"""
Node

All machines or network elements, or virtual machines, or any other thing that
is going to be provisioned, configured, monitored and repaired, needs a way
of being uniquely identified.

The Node Id is the way to uniquely identify a node.

This version of node will use the host name.

TODO(g): Allow easy and flexible user-override using blocks so users can define
    custom methods for identifying their hosts.
"""
import socket

def GetName():
    """Returns the local node name, which uniquely identifies this node.
  
  TODO(g): Allow easy and flexible user-override using blocks so users can define
      custom methods for identifying their hosts.
  """
    hostname = socket.getfqdn()
    return hostname


def GetNamePathReady():
    """Returns a version of the Node name which can be put into an OS path without
  messing up the path name.
  """
    node_id = GetName()
    replace_char = '_'
    replace_needed = '-+=\\|/[]{}()!@#$%^&*();:`~'
    for char in replace_needed:
        while char in node_id:
            node_id = node_id.replace(char, replace_char)

    return node_id


def GetId():
    """Returns a unique node id, which in an integer."""
    raise Exception("Not yet implemented.  Needs some sort of service database,                   even a YAML file would do, and then needs to raise an                   exception if a node name doesnt match any node ids, and then                   it can call an RPC call on a listed hostname, which would                   give it a node number, and it could update it's node database                  from the RPC call and have a list of it's fellow nodes.")