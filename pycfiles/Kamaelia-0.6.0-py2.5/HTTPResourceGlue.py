# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/HTTPResourceGlue.py
# Compiled at: 2008-10-19 12:19:52
"""HTTP Resource Glue 

What does it do?
====================
It picks the appropriate resource handler for a request using any of the
request's attributes (e.g. uri, accepted encoding, language, source etc.)

Its basic setup is to match prefixes of the request URI each of which have
their own predetermined request handler class (a component class).

HTTPResourceGlue also creates an instance of the handler component,
allowing complete control over its __init__ parameters.
Feel free to write your own for your webserver configuration.
"""
import types
from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
from Kamaelia.Protocol.HTTP.Handlers.SessionExample import SessionExampleWrapper
from Kamaelia.Protocol.HTTP.Handlers.UploadTorrents import UploadTorrentsWrapper
import Kamaelia.Protocol.HTTP.ErrorPages
URLHandlers = [
 [
  '/session/', SessionExampleWrapper],
 [
  '/torrentupload', UploadTorrentsWrapper],
 [
  '/', lambda r: Minimal(request=r, homedirectory='htdocs/', indexfilename='index.html')]]

def createRequestHandler(request):
    if request.get('bad'):
        return ErrorPages.websiteErrorPage(400, request.get('errormsg', ''))
    else:
        for (prefix, handler) in URLHandlers:
            if request['raw-uri'][:len(prefix)] == prefix:
                request['uri-prefix-trigger'] = prefix
                request['uri-suffix'] = request['raw-uri'][len(prefix):]
                return handler(request)

    return ErrorPages.websiteErrorPage(404, 'No resource handlers could be found for the requested URL.')