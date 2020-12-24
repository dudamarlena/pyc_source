# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/ZeroconfigService.py
# Compiled at: 2014-10-01 04:03:08
import logging, logging.config, pybonjour

class ZeroconfService:
    """A simple class witch publishes the actual service with avahi"""

    def __init__(self, name, port, stype='_wot._tcp', subtype='_sensor', domain='', host='', text=''):
        self.name = name
        self.stype = stype
        self.subtype = subtype + '._sub.' + stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text
        self.serviceDef = None
        return

    def register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            logging.debug('Registered service:')
            logging.debug('  name    =' + name)
            logging.debug('  regtype =' + regtype)
            logging.debug('  domain  =' + domain)

    def publish(self):
        avahitxt = pybonjour.TXTRecord(self.text, strict=True)
        self.serviceDef = pybonjour.DNSServiceRegister(name=self.name, regtype=self.stype, port=self.port, txtRecord=avahitxt, callBack=self.register_callback)

    def unpublish(self):
        self.serviceDef.close()