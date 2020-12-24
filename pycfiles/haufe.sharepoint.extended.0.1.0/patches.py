# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/haufe.sharepoint-0.1.9/nadpathaufe/sharepoint/patches.py
# Compiled at: 2014-12-08 21:10:32
"""
suds monkey patches
"""
import re, suds.metrics as metrics
from suds.transport import TransportError, Request
from suds.plugin import PluginContainer
from logger import logger as log

def send(self, soapenv):
    """
    Send soap message.
    @param soapenv: A soap envelope to send.
    @type soapenv: L{Document}
    @return: The reply to the sent message.
    @rtype: I{builtin} or I{subclass of} L{Object}
    """
    result = None
    location = self.location()
    binding = self.method.binding.input
    transport = self.options.transport
    retxml = self.options.retxml
    nosend = self.options.nosend
    prettyxml = self.options.prettyxml
    timer = metrics.Timer()
    try:
        plugins = PluginContainer(self.options.plugins)
        soapenv = soapenv.str()
        rkeys = [
         'UpdateListItems', 'GetListItems', 'GetList', 'GetItem', 'AddAttachment', 'CopyIntoItems', 'DeleteAttachment', 'GetAttachmentCollection']
        soapenv = re.sub('\\<SOAP-ENV:Header\\/\\>', '', soapenv)
        soapenv = re.sub('Body>', 'SOAP-ENV:Body>', soapenv)
        for i in rkeys:
            _soapenv = soapenv
            soapenv = soapenv.replace(i, i + ' xmlns="http://schemas.microsoft.com/sharepoint/soap/"', 1)
            if _soapenv != soapenv:
                break

        soapenv = re.sub('\\<queryOptions\\/\\>', '', soapenv)
        soapenv = re.sub('\\<ViewFields\\>.*\\<\\/ViewFields\\>', '', soapenv)
        soapenv = re.sub('OnError="[\\w]+"', 'OnError="Continue"', soapenv)
        soapenv = re.sub('XMLSchema-instance', 'XMLSchema', soapenv)
        soapenv = re.sub('&amp;#13;&amp;#10;', '&#13;&#10;', soapenv)
        soapenv = re.sub('tns:', '', soapenv)
        soapenv = re.sub('ns0:', '', soapenv)
        soapenv = re.sub('ns1:', '', soapenv)
        soapenv = soapenv.encode('utf-8')
        ctx = plugins.message.sending(envelope=soapenv)
        soapenv = ctx.envelope
        if nosend:
            return RequestContext(self, binding, soapenv)
        request = Request(location, soapenv)
        request.headers = self.headers()
        timer.start()
        reply = transport.send(request)
        timer.stop()
        metrics.log.debug('waited %s on server reply', timer)
        ctx = plugins.message.received(reply=reply.message)
        reply.message = ctx.reply
        if retxml:
            result = reply.message
        else:
            result = self.succeeded(binding, reply.message)
    except TransportError as e:
        if e.httpcode in (202, 204):
            result = None
        else:
            result = self.failed(binding, e)

    return result


from suds.client import SoapClient
SoapClient.send = send