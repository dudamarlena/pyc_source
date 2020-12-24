# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benwaters/sensu-auditor/lib/python2.7/site-packages/sensu_auditor/defaults.py
# Compiled at: 2016-09-05 07:27:50
"""
Default Sensu-Auditor Settings. Override in the defaults file
"""
import sys, logging
CONFIG_PATH = '/etc/default/sensu-auditor.ini'
SENSU_LOG_FOLDER = '/var/log/sensu/'
LOG_LOCATION = 'log_location'
LOG_TYPES = [
 'sensu-client', 'sensu-server', 'sensu-api']
DEFAULT_CONFIG_FIELDS = {'log_location': '/var/log/sensu', 'log_level': logging.DEBUG, 
   'log_output': sys.stdout, 
   'days': 30}
DEFAULT_SECTIONS = {'user': 'User', 
   'group': 'Groups'}
MESSAGES = {'RECEIVED_MESSAGE': 'received check request', 
   'PUBLISHED_MESSAGE': 'publishing check result'}