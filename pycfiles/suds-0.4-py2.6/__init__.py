# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/__init__.py
# Compiled at: 2010-09-13 12:24:18
"""
Suds is a lightweight SOAP python client that provides a
service proxy for Web Services.
"""
import os, sys
__version__ = '0.4'
__build__ = 'GA R699-20100913'

class MethodNotFound(Exception):

    def __init__(self, name):
        Exception.__init__(self, "Method not found: '%s'" % name)


class PortNotFound(Exception):

    def __init__(self, name):
        Exception.__init__(self, "Port not found: '%s'" % name)


class ServiceNotFound(Exception):

    def __init__(self, name):
        Exception.__init__(self, "Service not found: '%s'" % name)


class TypeNotFound(Exception):

    def __init__(self, name):
        Exception.__init__(self, "Type not found: '%s'" % tostr(name))


class BuildError(Exception):
    msg = '\n        An error occured while building a instance of (%s).  As a result\n        the object you requested could not be constructed.  It is recommended\n        that you construct the type manually using a Suds object.\n        Please open a ticket with a description of this error.\n        Reason: %s\n        '

    def __init__(self, name, exception):
        Exception.__init__(self, BuildError.msg % (name, exception))


class SoapHeadersNotPermitted(Exception):
    msg = '\n        Method (%s) was invoked with SOAP headers.  The WSDL does not\n        define SOAP headers for this method.  Retry without the soapheaders\n        keyword argument.\n        '

    def __init__(self, name):
        Exception.__init__(self, self.msg % name)


class WebFault(Exception):

    def __init__(self, fault, document):
        if hasattr(fault, 'faultstring'):
            Exception.__init__(self, "Server raised fault: '%s'" % fault.faultstring)
        self.fault = fault
        self.document = document


class Repr:

    def __init__(self, x):
        self.x = x

    def __str__(self):
        return repr(self.x)


def tostr(object, encoding=None):
    """ get a unicode safe string representation of an object """
    if isinstance(object, basestring):
        if encoding is None:
            return object
        else:
            return object.encode(encoding)
    if isinstance(object, tuple):
        s = [
         '(']
        for item in object:
            if isinstance(item, basestring):
                s.append(item)
            else:
                s.append(tostr(item))
            s.append(', ')

        s.append(')')
        return ('').join(s)
    else:
        if isinstance(object, list):
            s = [
             '[']
            for item in object:
                if isinstance(item, basestring):
                    s.append(item)
                else:
                    s.append(tostr(item))
                s.append(', ')

            s.append(']')
            return ('').join(s)
        if isinstance(object, dict):
            s = [
             '{']
            for item in object.items():
                if isinstance(item[0], basestring):
                    s.append(item[0])
                else:
                    s.append(tostr(item[0]))
                s.append(' = ')
                if isinstance(item[1], basestring):
                    s.append(item[1])
                else:
                    s.append(tostr(item[1]))
                s.append(', ')

            s.append('}')
            return ('').join(s)
        try:
            return unicode(object)
        except:
            return str(object)

        return


class null:
    """
    The I{null} object.
    Used to pass NULL for optional XML nodes.
    """
    pass


def objid(obj):
    return obj.__class__.__name__ + ':' + hex(id(obj))


import client