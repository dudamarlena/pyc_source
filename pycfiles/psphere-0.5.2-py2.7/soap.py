# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/psphere/soap.py
# Compiled at: 2013-04-04 22:22:41
"""
A leaky wrapper for the underlying suds library.
"""
import logging, urllib2, suds
from pprint import pprint
logger = logging.getLogger(__name__)

class VimFault(Exception):

    def __init__(self, fault):
        self.fault = fault
        self.fault_type = fault.__class__.__name__
        self._fault_dict = {}
        for attr in fault:
            self._fault_dict[attr[0]] = attr[1]

        Exception.__init__(self, '%s: %s' % (self.fault_type, self._fault_dict))


def get_client(url):
    client = suds.client.Client(url + '/vimService.wsdl')
    client.set_options(location=url)
    return client


def create(client, _type, **kwargs):
    """Create a suds object of the requested _type."""
    obj = client.factory.create('ns0:%s' % _type)
    for key, value in kwargs.items():
        setattr(obj, key, value)

    return obj


def invoke(client, method, **kwargs):
    """Invoke a method on the underlying soap service."""
    try:
        result = getattr(client.service, method)(**kwargs)
    except AttributeError as e:
        logger.critical('Unknown method: %s', method)
        raise
    except urllib2.URLError as e:
        logger.debug(pprint(e))
        logger.debug("A URL related error occurred while invoking the '%s' method on the VIM server, this can be caused by name resolution or connection problems.", method)
        logger.debug('The underlying error is: %s', e.reason[1])
        raise
    except suds.client.TransportError as e:
        logger.debug(pprint(e))
        logger.debug('TransportError: %s', e)
    except suds.WebFault as e:
        logger.critical('SUDS Fault: %s' % e.fault.faultstring)
        if len(e.fault.faultstring) > 0:
            raise
        detail = e.document.childAtPath('/Envelope/Body/Fault/detail')
        fault_type = detail.getChildren()[0].name
        fault = create(fault_type)
        if isinstance(e.fault.detail[0], list):
            for attr in e.fault.detail[0]:
                setattr(fault, attr[0], attr[1])

        else:
            fault['text'] = e.fault.detail[0]
        raise VimFault(fault)

    return result


class ManagedObjectReference(suds.sudsobject.Property):
    """Custom class to replace the suds generated class, which lacks _type."""

    def __init__(self, _type, value):
        suds.sudsobject.Property.__init__(self, value)
        self._type = _type