# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/maclocate/skyhook.py
# Compiled at: 2008-09-12 16:20:22
import sys, simplexmlapi
from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientFactory
from twisted.web.client import getPage

class SkyhookProtocol(object):
    __module__ = __name__

    def __init__(self):
        self.parsed = 0
        self.with_errors = 0
        self.error_list = []
        self.results = []

    def error_handler(self, traceback, extra_args):
        print traceback, extra_args
        self.with_errors += 1
        self.error_list.append(extra_args)

    def xmlreq(self, macaddress, username='beta', realm='js.loki.com', signalstrength='-50'):
        """
        Create the XML document to be posted to Skyhook.
        """
        macaddress = macaddress.replace(':', '')
        return ("<?xml version='1.0'?>\n            <LocationRQ xmlns='http://skyhookwireless.com/wps/2005' \n                version='2.6' street-address-lookup='full'>\n                <authentication version='2.0'>\n                    <simple>\n                        <username>%(username)s</username>\n                        <realm>%(realm)s</realm>\n                    </simple>\n                </authentication>\n                <access-point>\n                    <mac>%(macaddress)s</mac>\n                    <signal-strength>%(signalstrength)s</signal-strength>\n                </access-point>\n            </LocationRQ>\n        " % locals()).strip()

    def get(self, r, macaddress):
        postdata = self.xmlreq(macaddress)
        d = getPage('https://api.skyhookwireless.com/wps2/location', method='POST', headers={'Content-Type': 'text/xml'}, postdata=postdata)
        return d

    def parse(self, data, macaddress):
        doc = simplexmlapi.loads(data)
        try:
            result = (
             doc.latitude._, doc.longitude._)
        except:
            result = doc.error._

        return (
         macaddress, result)

    def store(self, result):
        self.results.append(result)

    def done(self, data=None):
        self.parsed += 1
        if self.parsed >= self.FINISHEDNUM:
            for (mac, loc) in self.results:
                print '%s\t%s' % (mac, loc)

            reactor.stop()

    def start(self, macaddresses, standalone=True):
        d = defer.succeed('Starting...')
        if standalone:
            self.FINISHEDNUM = len(macaddresses)
        for macaddress in macaddresses:
            d.addCallback(self.get, macaddress)
            d.addErrback(self.error_handler, (macaddress, 'getting'))
            d.addCallback(self.parse, macaddress)
            d.addErrback(self.error_handler, (macaddress, 'parsing'))
            d.addCallback(self.store)
            d.addErrback(self.error_handler, (macaddress, 'storing'))
            if standalone:
                d.addCallback(self.done)

        if not standalone:
            return d


class SkyhookFactory(ClientFactory):
    __module__ = __name__

    def __init__(self, macs, standalone=False):
        self.protocol = SkyhookProtocol()
        self.standalone = standalone
        if standalone:
            self.start(macs)

    def start(self, macs):
        """
        Might split into groups here so as not to flood server.
        """
        if not self.standalone:
            return self.protocol.start(macs, self.standalone)
        else:
            self.protocol.start(macs, self.standalone)


def locate(*macs):
    """
    Attempt to locate interfaces.
    """
    f = SkyhookFactory(macs, standalone=True)
    reactor.run()


def cli():
    macs = sys.argv[1:]
    locate(*macs)