# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/swift_log.py
# Compiled at: 2019-05-16 13:41:33
"""
SwiftLog - file ``/var/log/containers/swift/swift.log`` and ``/var/log/swift/swift.log``
========================================================================================
"""
from insights import parser, Syslog
from insights.specs import Specs

@parser(Specs.swift_log)
class SwiftLog(Syslog):
    """Class for parsing ``/var/log/containers/swift/swift.log`` and
    ``/var/log/swift/swift.log`` file.

    Provide access to swift log using the
    :class:`insights.core.Syslog` parser class.

    Sample ``swift.log`` file content::

      Sep 29 23:50:29 rh-server object-server: Starting object replication pass.
      Sep 29 23:50:29 rh-server object-server: Nothing replicated for 0.01691198349 seconds.
      Sep 29 23:50:29 rh-server object-server: Object replication complete. (0.00 minutes)
      Sep 29 23:50:38 rh-server container-server: Beginning replication run
      Sep 29 23:50:38 rh-server container-server: Replication run OVER
      Sep 29 23:50:38 rh-server container-server: Attempted to replicate 0 dbs in 0.00064 seconds (0.00000/s)

    Examples:

      >>> obj_server_lines = swift_log.get("object-server")
      >>> len(obj_server_lines)
      3
      >>> obj_server_lines[0].get("procname")
      'object-server'
      >>> obj_server_lines[0].get("message")
      'Starting object replication pass.'

    """
    pass