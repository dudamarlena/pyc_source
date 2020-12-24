# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/engine/nodealloc.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 1831 bytes
"""
Node allocator module.
"""

class NodeAllocator:
    __doc__ = '\n\tNode allocator.\n\t'

    def __init__(self, ssh_session_fact, das_machine, node_alloc_machine):
        self._NodeAllocator__das_machine = das_machine
        self._NodeAllocator__node_alloc_machine = node_alloc_machine
        self._NodeAllocator__das_ssh_session = ssh_session_fact.session(das_machine.appserver_user, das_machine.host)
        self._NodeAllocator__node_alloc_ssh_session = ssh_session_fact.session(node_alloc_machine.appserver_user, node_alloc_machine.host)

    def prepare(self, domain_name, node_name):
        """
                Install the specified domain saved master password to the specified node
                file system.

                :param str domain_name:
                   Name of the domain who owns the saved master password.
                :param str node_name:
                   Name of the node where the master password must be installed on.
                   
                :rtype:
                   str
                :return:
                   The node allocator host.
                """
        any(self._NodeAllocator__node_alloc_ssh_session.execute(self._NodeAllocator__node_alloc_machine.ping_cmd()))
        any(self._NodeAllocator__das_ssh_session.execute(self._NodeAllocator__das_machine.install_master_password_cmd(domain_name, node_name, self._NodeAllocator__node_alloc_machine.host)))
        return self._NodeAllocator__node_alloc_machine.host