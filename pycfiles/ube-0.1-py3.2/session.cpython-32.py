# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/common/session.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on May 8, 2010

@author: Nicklas Boerjesson
"""
from ube.common.settings import UBPMSettings

class UBPMSession(object):
    """
    The session class contains:
    * providing database connection(s).
    * security desciptors.
    * session information.
    """

    def New_Session(self, login, password):
        """
        Get a new session from the authentication server.
        """
        self.Username = UBPMSettings.Parser.get('credentials', 'username')
        self.Password = UBPMSettings.Parser.get('credentials', 'password')
        raise Exception('Invalid login')

    def __init__(self, settings):
        """
        Constructor
        """
        self.UnifiedBPMURI = settings.Parser.get('broker', 'broker_server_base_URI')
        AuthURI = self.UnifiedBPMURI + '/services/authentication_soap.wsgi?wsdl'
        print('Creating Session SOAP client, URL: ' + AuthURI)
        print('Done.')