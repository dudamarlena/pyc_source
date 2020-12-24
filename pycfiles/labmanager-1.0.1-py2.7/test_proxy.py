# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/test/test_proxy.py
# Compiled at: 2014-02-26 03:37:27
__author__ = 'root'
user = {}
user['wsdl_url'] = 'https://chnservices-lm.dctmlabs.com/LabManager/SOAP/LabManagerinternal.asmx?WSDL'
user['username'] = 'shaom2'
user['password'] = ')Slamdunk1986'
user['organizationname'] = 'PF-QA-DFS'
user['workspacename'] = 'Main'
import logging
from labmanager.lmwsproxy import LMService
logger = logging.getLogger()
service = LMService(user, logger)
service.configuration_undeploy_by_id(int(10313))