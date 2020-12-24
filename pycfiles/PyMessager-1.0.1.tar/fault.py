# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymessagefocus2/fault.py
# Compiled at: 2016-08-14 13:14:51
from xmlrpclib import ProtocolError
from xmlrpclib import Fault as RPCFault

class Fault(Exception):
    """
    This error class exists to standardise certain xmlrpclib.Fault and
    xmlrpclib.ProtocolError instances under a single interface that conforms
    to the Adestra MessageFocus documentation.
    """

    def __init__(self, faultCode, faultString):
        super(Exception, self).__init__('%s: %s' % (faultCode, faultString))
        self.faultCode = faultCode
        self.faultString = faultString

    @staticmethod
    def parse(fn):

        def func_wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if isinstance(e, ProtocolError):
                    if e.errcode == 401:
                        raise Fault(301, 'You must be authenticated to use this resource.')
                if isinstance(e, RPCFault):
                    if e.faultCode == 200:
                        if 'invalid input syntax for integer' in e.faultString:
                            raise Fault(204, 'Argument invalid or of incorrect type, e.g. you have passed a String where an Integer is expected.')
                        elif 'column' in e.faultString and 'does not exist' in e.faultString:
                            raise Fault(204, 'Argument invalid or of incorrect type, e.g. you have passed a Struct where an Integer is expected.')
                        elif 'Campaign has not been published' in e.faultString:
                            raise Fault(216, 'Campaign has not been published.')
                    raise Fault(e.faultCode, e.faultString)
                raise e

        return func_wrapper