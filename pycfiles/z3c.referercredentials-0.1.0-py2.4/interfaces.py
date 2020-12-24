# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/referercredentials/interfaces.py
# Compiled at: 2007-08-27 17:51:44
"""HTTP Referer Credentials interfaces

$Id: interfaces.py 77888 2007-07-13 22:03:14Z roymathew $
"""
__docformat__ = 'reStructuredText'
import zope.schema
from zope.app.authentication import interfaces

class IHTTPRefererCredentials(interfaces.ICredentialsPlugin):
    """HTTP-Referer Credentials"""
    __module__ = __name__
    sessionKey = zope.schema.ASCIILine(title='Session Key', description='Session Key')
    allowedHosts = zope.schema.Tuple(title='Allowed Hosts', description='A list of hosts allowed to access.', value_type=zope.schema.TextLine(title='host'), default=('localhost', ))
    credentials = zope.schema.Field(title='Credentials', description='An object representing the credentials of the referred user.')
    challengeView = zope.schema.TextLine(title='Challenge View', description='The view to which the user is forwarded when not coming from a correct referer site.', default='unauthorized.html')