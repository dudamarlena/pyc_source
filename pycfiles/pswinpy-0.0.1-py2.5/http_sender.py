# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pswinpy\http_sender.py
# Compiled at: 2011-05-04 09:59:40
import httplib
from pswinpy.mode import Mode

class HttpSender(object):
    host = 'gw2-fro.pswin.com:81'

    def __init__(self):
        pass

    def send(self, request):
        if not Mode.test:
            xml = request.xml()
            if Mode.debug:
                print 'Request: ', xml
            webservice = httplib.HTTP(HttpSender.host)
            webservice.putrequest('POST', '/')
            webservice.putheader('Content-type', 'text/xml; charset="UTF-8"')
            webservice.putheader('Content-length', '%d' % len(xml))
            webservice.endheaders()
            webservice.send(xml)
            if Mode.debug:
                (statuscode, statusmessage, header) = webservice.getreply()
                print 'Response: ', statuscode, statusmessage
                print 'headers: ', header
                res = webservice.getfile().read()
                print res