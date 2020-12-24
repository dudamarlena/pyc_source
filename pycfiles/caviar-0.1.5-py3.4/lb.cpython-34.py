# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/engine/lb.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 1538 bytes
"""
Load balancer module.
"""

class LoadBalancer:
    __doc__ = '\n\tLoad balancer.\n\t'

    def __init__(self, ssh_session_fact, lb_machine):
        self._LoadBalancer__ssh_session = ssh_session_fact.session(lb_machine.web_user, lb_machine.host)
        self._LoadBalancer__lb_machine = lb_machine

    def add_instance(self, name, host, port):
        """
                Add an instance with the given name, host and port to the load balancer.

                :param str name:
                   Instance name.
                :param str host:
                   Instance host.
                :param str port:
                   Instance port.
                """
        for line in self._LoadBalancer__ssh_session.execute(self._LoadBalancer__lb_machine.add_instance_cmd(name, host, port)):
            pass

    def remove_instance(self, name):
        """
                Remove the instance with the given name from the load balancer.
                
                :param str name:
                   Instance name.
                """
        for line in self._LoadBalancer__ssh_session.execute(self._LoadBalancer__lb_machine.remove_instance_cmd(name)):
            pass