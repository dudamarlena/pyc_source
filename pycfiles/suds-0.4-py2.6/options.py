# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/transport/options.py
# Compiled at: 2010-01-12 17:00:23
"""
Contains classes for transport options.
"""
from suds.transport import *
from suds.properties import *

class Options(Skin):
    """
    Options:
        - B{proxy} - An http proxy to be specified on requests.
             The proxy is defined as {protocol:proxy,}
                - type: I{dict}
                - default: {}
        - B{timeout} - Set the url open timeout (seconds).
                - type: I{float}
                - default: 90
        - B{headers} - Extra HTTP headers.
                - type: I{dict}
                    - I{str} B{http} - The I{http} protocol proxy URL.
                    - I{str} B{https} - The I{https} protocol proxy URL.
                - default: {}
        - B{username} - The username used for http authentication.
                - type: I{str}
                - default: None
        - B{password} - The password used for http authentication.
                - type: I{str}
                - default: None
    """

    def __init__(self, **kwargs):
        domain = __name__
        definitions = [
         Definition('proxy', dict, {}),
         Definition('timeout', (int, float), 90),
         Definition('headers', dict, {}),
         Definition('username', basestring, None),
         Definition('password', basestring, None)]
        Skin.__init__(self, domain, definitions, kwargs)
        return