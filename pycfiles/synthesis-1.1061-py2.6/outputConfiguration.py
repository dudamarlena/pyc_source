# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/conf/outputConfiguration.py
# Compiled at: 2010-12-12 18:24:12
"""see ./docs/output_configurations.readme for information on setting these configurations"""
Configuration = {'8888': {'vendor': 'System Operator', 
            'outputFormat': 'hmiscsv', 
            'destinationURL': 'localhost', 
            'transportConfiguration': ''}, 
   '9999': {'vendor': 'System Operator', 
            'outputFormat': 'hmisxml', 
            'destinationURL': 'localhost', 
            'transportConfiguration': 'sys.stdout'}, 
   '1234': {'vendor': 'Some Vendor Name', 
            'outputFormat': 'svcpoint', 
            'destinationURL': 'someone@somewhere.net', 
            'transportConfiguration': 'email'}, 
   '5678': {'vendor': 'Some Vendor Name2', 
            'outputFormat': 'svcpoint', 
            'destinationURL': 'subdomain.domain.net', 
            'transportConfiguration': 'sftp', 
            'username': 'someuser', 
            'password': 'somepassword'}, 
   '91011': {'vendor': 'Some Vendor Name3', 
             'outputFormat': 'svcpoint', 
             'destinationURL': '192.168.0.208', 
             'transportConfiguration': 'sftp', 
             'username': 'someuser2', 
             'password': 'somepassword2'}, 
   '1313': {'outputFormat': 'hmiscsv', 
            'destinationURL': 'user@localhost', 
            'transportConfiguration': 'email'}}