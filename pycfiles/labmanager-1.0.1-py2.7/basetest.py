# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/test/basetest.py
# Compiled at: 2014-02-26 03:37:27
__author__ = 'root'
from suds.client import Client
client = Client('https://chnservices-lm.dctmlabs.com/LabManager/SOAP/LabManagerinternal.asmx?WSDL')
user = client.factory.create('AuthenticationHeader')
user['username'] = 'shaom2'
user['password'] = ')Slamdunk1986'
user['organizationname'] = 'PF-QA-DFS'
user['workspacename'] = 'Main'
client.set_options(soapheaders=user)
configuration_ID = 10221
template_ID = 12643
network_ID = 71
soapIP_mode = client.factory.create('SOAPIPMode')
netinfo = client.factory.create('NetInfo')
newArrayofNetInfo = client.factory.create('ArrayOfNetInfo')
newArrayofNetInfo.NetInfo.append(netinfo)
tangram_id = 8441
lxc_id = 22395
git_lab_ci_ruunner = 22005
import suds
try:
    print client.service.GetConfigurationByName('pagrant1')
except suds.WebFault as e:
    print e