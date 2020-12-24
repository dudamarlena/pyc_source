# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\core\config.py
# Compiled at: 2010-06-04 07:07:11
"""Module containing configuration information for superpy.

This module should define the following configuration variables:

  smtpServer:      String name of smtp server to use when sending mail.
  serviceLogFile:  String path to location for superpy server log file.
  defaultLogLevel: Log level to use when starting server.
  
"""
import logging
smtpServer = 'FIXME'
serviceLogFile = 'c:/temp/superpy_log.txt'
defaultLogLevel = logging.DEBUG