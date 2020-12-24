# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/config/settings.py
# Compiled at: 2012-12-17 14:25:29
__home__ = '/Users/rfaulkner/'
__project_home__ = ('').join([__home__, 'projects/E3_analysis/'])
__web_home__ = ('').join([__project_home__, 'web_interface/'])
__sql_home__ = ('').join([__project_home__, 'SQL/'])
__message_templates_home__ = ('').join([__project_home__, 'wsor/message_templates/'])
__server_log_local_home__ = ('').join([__project_home__, 'logs/'])
__data_file_dir__ = ('').join([__project_home__, 'data/'])
__wsor_msg_templates_home_dir__ = ('').join([__home__, 'projects/wsor/message_templates/'])
__web_app_module__ = 'web_interface'
__system_user__ = 'rfaulk'
connections = {'slave': {'user': 'research', 
             'host': '127.0.0.1', 
             'db': 'staging', 
             'passwd': '46c2f5d9481', 
             'port': 3307}, 
   'slave-2': {'user': 'rfaulk', 
               'host': '127.0.0.1', 
               'db': 'rfaulk', 
               'passwd': '8uncleb1', 
               'port': 3307}}