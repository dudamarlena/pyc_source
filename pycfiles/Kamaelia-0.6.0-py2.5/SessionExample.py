# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/Handlers/SessionExample.py
# Compiled at: 2008-10-19 12:19:52
"""========================
Session Example
========================
A simple persistent request handler component.
Each time a URL that is handled by this component is requested, the page's
'hit counter' is incremented and shown to the user as text.
"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
import Kamaelia.Protocol.HTTP.ErrorPages
Sessions = {}

def SessionExampleWrapper(request):
    sessionid = request['uri-suffix']
    if Sessions.has_key(sessionid):
        session = Sessions[sessionid]
        if session['busy']:
            return ErrorPages.websiteErrorPage(500, 'Session handler busy')
        else:
            return session['handler']
    else:
        session = {'busy': True, 'handler': SessionExample(sessionid)}
        Sessions[sessionid] = session
        return session['handler']


class SessionExample(component):

    def __init__(self, sessionid):
        super(SessionExample, self).__init__()
        self.sessionid = sessionid

    def main(self):
        counter = 0
        while 1:
            counter += 1
            resource = {'statuscode': '200', 
               'data': '<html><body>%d</body></html>' % counter, 
               'incomplete': False, 
               'content-type': 'text/html'}
            self.send(resource, 'outbox')
            self.send(producerFinished(self), 'signal')
            Sessions[self.sessionid]['busy'] = False
            self.pause()
            yield 1


__kamaelia_components__ = (SessionExample,)