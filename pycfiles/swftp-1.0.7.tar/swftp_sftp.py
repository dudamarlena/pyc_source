# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kevin/Projects/object_storage/swftp/twisted/plugins/swftp_sftp.py
# Compiled at: 2013-03-04 16:01:13
"""
Defines serviceMaker, which required for automatic twistd integration for
swftp-sftp

See COPYING for license information.
"""
from twisted.application.service import ServiceMaker
serviceMaker = ServiceMaker('swftp-sftp', 'swftp.sftp.service', 'An SFTP Proxy Interface for Swift', 'swftp-sftp')