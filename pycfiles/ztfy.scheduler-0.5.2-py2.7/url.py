# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/url.py
# Compiled at: 2012-10-22 06:18:07
import chardet, codecs, urlparse
from ztfy.scheduler.interfaces import IURLCallerTask
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.scheduler.task import BaseTask
from ztfy.utils.html import htmlToText
from ztfy.utils.protocol import http

class URLCallerTask(BaseTask):
    """URL caller task"""
    implements(IURLCallerTask)
    url = FieldProperty(IURLCallerTask['url'])
    username = FieldProperty(IURLCallerTask['username'])
    password = FieldProperty(IURLCallerTask['password'])
    proxy_server = FieldProperty(IURLCallerTask['proxy_server'])
    proxy_port = FieldProperty(IURLCallerTask['proxy_port'])
    remote_dns = FieldProperty(IURLCallerTask['remote_dns'])
    proxy_username = FieldProperty(IURLCallerTask['proxy_username'])
    proxy_password = FieldProperty(IURLCallerTask['proxy_password'])
    connection_timeout = FieldProperty(IURLCallerTask['connection_timeout'])

    def run(self, report):
        parser = urlparse.urlparse(self.url)
        if not parser.netloc:
            raise Exception, 'Missing hostname - Task aborted'
        if self.proxy_server and not self.proxy_port:
            raise Exception, 'Proxy server defined without proxy port - Task aborted'
        params = parser.query and dict([ part.split('=') for part in parser.query.split('&') ]) or {}
        credentials = (self.username, self.password) if self.username else ()
        proxy = (self.proxy_server, self.proxy_port) if self.proxy_server else ()
        proxy_auth = (self.proxy_username, self.proxy_password) if self.proxy_username else ()
        client = http.HTTPClient('GET', parser.scheme, parser.netloc, parser.path, params=params, credentials=credentials, proxy=proxy, rdns=self.remote_dns, proxy_auth=proxy_auth, timeout=self.connection_timeout)
        response, content = client.getResponse()
        if response.status == 200:
            report.write(('\n').join([ '%s=%s' % (k, v) for k, v in response.items() ]) + '\n\n')
            if response.get('content-type', 'text/plain').startswith('text/html'):
                content = htmlToText(content)
            charset = chardet.detect(content).get('encoding') or 'utf-8'
            report.write(codecs.decode(content, charset))