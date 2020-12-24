# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/m_syslog.py
# Compiled at: 2019-04-05 15:23:31
# Size of source mod 2**32: 7351 bytes
"""socket interface to unix syslog.
On Unix, there are usually two ways of getting to syslog: via a
local unix-domain socket, or via the TCP service.

Usually "/dev/log" is the unix domain socket.  This may be different
for other systems.

>>> my_client = syslog_client ('/dev/log')

Otherwise, just use the UDP version, port 514.

>>> my_client = syslog_client (('my_log_host', 514))

On win32, you will have to use the UDP version.  Note that
you can use this to log to other hosts (and indeed, multiple
hosts).

This module is not a drop-in replacement for the python
<syslog> extension module - the interface is different.

Usage:

>>> c = syslog_client()
>>> c = syslog_client ('/strange/non_standard_log_location')
>>> c = syslog_client (('other_host.com', 514))
>>> c.log ('testing', facility='local0', priority='debug')

"""
LOG_EMERG = 0
LOG_ALERT = 1
LOG_CRIT = 2
LOG_ERR = 3
LOG_WARNING = 4
LOG_NOTICE = 5
LOG_INFO = 6
LOG_DEBUG = 7
LOG_KERN = 0
LOG_USER = 1
LOG_MAIL = 2
LOG_DAEMON = 3
LOG_AUTH = 4
LOG_SYSLOG = 5
LOG_LPR = 6
LOG_NEWS = 7
LOG_UUCP = 8
LOG_CRON = 9
LOG_AUTHPRIV = 10
LOG_LOCAL0 = 16
LOG_LOCAL1 = 17
LOG_LOCAL2 = 18
LOG_LOCAL3 = 19
LOG_LOCAL4 = 20
LOG_LOCAL5 = 21
LOG_LOCAL6 = 22
LOG_LOCAL7 = 23
priority_names = {'alert':LOG_ALERT, 
 'crit':LOG_CRIT, 
 'debug':LOG_DEBUG, 
 'emerg':LOG_EMERG, 
 'err':LOG_ERR, 
 'error':LOG_ERR, 
 'info':LOG_INFO, 
 'notice':LOG_NOTICE, 
 'panic':LOG_EMERG, 
 'warn':LOG_WARNING, 
 'warning':LOG_WARNING}
facility_names = {'auth':LOG_AUTH, 
 'authpriv':LOG_AUTHPRIV, 
 'cron':LOG_CRON, 
 'daemon':LOG_DAEMON, 
 'kern':LOG_KERN, 
 'lpr':LOG_LPR, 
 'mail':LOG_MAIL, 
 'news':LOG_NEWS, 
 'security':LOG_AUTH, 
 'syslog':LOG_SYSLOG, 
 'user':LOG_USER, 
 'uucp':LOG_UUCP, 
 'local0':LOG_LOCAL0, 
 'local1':LOG_LOCAL1, 
 'local2':LOG_LOCAL2, 
 'local3':LOG_LOCAL3, 
 'local4':LOG_LOCAL4, 
 'local5':LOG_LOCAL5, 
 'local6':LOG_LOCAL6, 
 'local7':LOG_LOCAL7}
import socket

class syslog_client:

    def __init__(self, address='/dev/log'):
        self.address = address
        self.stream = 0
        if isinstance(address, type('')):
            try:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.socket.connect(address)
            except socket.error:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.stream = 1

        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    log_format_string = '<%d>%s\x00'

    def log(self, message, facility=LOG_USER, priority=LOG_INFO):
        message = self.log_format_string % (
         self.encode_priority(facility, priority),
         message)
        if self.stream:
            self.socket.send(message)
        else:
            self.socket.sendto(message, self.address)

    def encode_priority(self, facility, priority):
        if type(facility) == type(''):
            facility = facility_names[facility]
        if type(priority) == type(''):
            priority = priority_names[priority]
        return facility << 3 | priority

    def close(self):
        if self.stream:
            self.socket.close()