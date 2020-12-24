# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\services\web.py
# Compiled at: 2011-02-11 15:06:34
"""
A HTTP/HTTPS server.
"""
from seishub.core import __version__ as SEISHUB_VERSION
from seishub.core.config import IntOption, BoolOption, Option, ListOption
from seishub.core.defaults import HTTP_PORT, HTTPS_PORT, HTTPS_CERT_FILE, HTTPS_PKEY_FILE, HTTP_LOG_FILE, HTTPS_LOG_FILE, ADMIN_THEME, DEFAULT_PAGES
from seishub.core.exceptions import InternalServerError, ForbiddenError, SeisHubError
from seishub.core.processor import Processor, HEAD, getChildForRequest
from seishub.core.processor.interfaces import IFileSystemResource, IResource, IStatical, IRESTResource, IAdminResource
from seishub.core.util.path import addBase
from seishub.core.util.text import isInteger
from twisted.application import service
from twisted.application.internet import SSLServer, TCPServer
from twisted.internet import threads, defer, ssl
from twisted.python.failure import Failure
from twisted.web import http, server, static
import StringIO, errno, gzip, os, urllib
__all__ = [
 'WebService']
RESOURCELIST_ROOT = '<?xml version="1.0" encoding="UTF-8"?>\n\n<seishub xml:base="%s" xmlns:xlink="http://www.w3.org/1999/xlink">%s\n</seishub>\n'
RESOURCELIST_NODE = '\n  <%s category="%s"%s xlink:type="simple" xlink:href="%s"><![CDATA[%s]]></%s>'

class WebRequest(Processor, http.Request):
    """
    A request via the HTTP/HTTPS protocol.
    """

    def __init__(self, channel, queued):
        self.env = channel.factory.env
        Processor.__init__(self, self.env)
        http.Request.__init__(self, channel, queued)
        self.notifications = []
        self.default_pages = self.env.config.getlist('web', 'default_pages') or DEFAULT_PAGES

    def isAuthenticatedUser(self):
        """
        XXX: this will change soon!
        """
        if self.getUser() == 'anonymous':
            return False
        try:
            authenticated = self.env.auth.checkPassword(self.getUser(), self.getPassword())
        except:
            return False

        return authenticated

    def getUser(self):
        return http.Request.getUser(self)

    def authenticate(self):
        """
        """
        self.setHeader('WWW-Authenticate', 'Basic realm="SeisHub"')
        self.setResponseCode(http.UNAUTHORIZED)
        self.write('Authentication required.')
        self.finish()

    def render(self):
        """
        Renders the requested resource returned from the self.process() method.
        """
        if self.path == '/manage/logout':
            self.authenticate()
            return
        try:
            result = getChildForRequest(self.env.tree, self)
        except SeisHubError as e:
            self.setResponseCode(e.code, e.message)
            self.env.log.http(e.code, e.message)
            self.write('')
            self.finish()
            return
        except Exception as e:
            self.env.log.error(e)
            self.write('')
            self.finish()
            return

        self.setHeader('server', 'SeisHub ' + SEISHUB_VERSION)
        self.setHeader('date', http.datetimeToString())
        if result == server.NOT_DONE_YET:
            return
        if not IAdminResource.providedBy(result) and self.env.auth.getUser('anonymous').permissions == 755:
            pass
        elif not result.public and not self.isAuthenticatedUser():
            self.authenticate()
            return
        if IFileSystemResource.providedBy(result):
            data = result.render(self)
            if result.folderish:
                for id in self.default_pages:
                    if id in data and not data[id].folderish:
                        data = data[id].render(self)
                        return self._renderFileResource(data)

                return self._renderFolder(data)
            return self._renderFileResource(data)
        elif IStatical.providedBy(result):
            data = result.render(self)
            if isinstance(data, basestring):
                return self._renderResource(data)
            if isinstance(data, dict):
                return self._renderFolder(data)
        else:
            if IRESTResource.providedBy(result):
                d = threads.deferToThread(result.render, self)
                d.addCallback(self._cbSuccess)
                d.addErrback(self._cbFailed)
                return server.NOT_DONE_YET
            if IResource.providedBy(result):
                d = threads.deferToThread(result.render, self)
                d.addCallback(self._cbSuccess)
                d.addErrback(self._cbFailed)
                return server.NOT_DONE_YET
        msg = "I don't know how to handle this resource type %s"
        raise InternalServerError(msg % type(result))

    def _cbSuccess(self, result):
        if isinstance(result, dict):
            return self._renderFolder(result)
        else:
            if isinstance(result, basestring):
                return self._renderResource(result)
            d = threads.deferToThread(result.render, self)
            d.addCallback(self._renderResource)
            d.addErrback(self._cbFailed)
            return server.NOT_DONE_YET

    def _cbFailed(self, failure):
        if not isinstance(failure, Failure):
            raise
        if 'seishub.exceptions.SeisHubError' not in failure.parents:
            self.env.log.error(failure.getTraceback())
            self.setResponseCode(http.INTERNAL_SERVER_ERROR)
        else:
            self.setResponseCode(failure.value.code, failure.value.message)
            self.env.log.http(failure.value.code, failure.value.message)
        self.write('')
        self.finish()

    def _renderFileResource(self, obj):
        """
        Renders a object implementing L{IFileResource}.
        """
        obj.restat()
        try:
            fp = obj.open()
        except IOError as e:
            if e[0] == errno.EACCES:
                msg = 'Can not access item %s.'
                raise ForbiddenError(msg % str(obj.path))
            raise

        last_modified = int(obj.getModificationTime())
        if self.setLastModified(last_modified) is http.CACHED:
            self.finish()
            return
        obj.type, obj.enc = static.getTypeAndEncoding(obj.basename(), obj.content_types, obj.content_encodings, obj.default_type)
        if obj.type:
            self.setHeader('content-type', obj.type)
        if obj.enc:
            self.setHeader('content-encoding', obj.enc)
        fsize = size = obj.getsize()
        self.setHeader('content-length', str(fsize))
        if self.method == HEAD:
            self.write('')
            self.finish()
            return
        self.setHeader('accept-ranges', 'bytes')
        range = self.getHeader('range')
        if range and 'bytes=' in range and '-' in range.split('=')[1]:
            parts = range.split('bytes=')[1].strip().split('-')
            if len(parts) == 2:
                start = parts[0]
                end = parts[1]
                if isInteger(start):
                    fp.seek(int(start))
                if isInteger(end):
                    end = int(end)
                    size = end
                else:
                    end = size
                self.setResponseCode(http.PARTIAL_CONTENT)
                self.setHeader('content-range', 'bytes %s-%s/%s ' % (
                 str(start), str(end), str(size)))
                fsize = end - int(start)
                self.setHeader('content-length', str(fsize))
                sp = static.SingleRangeStaticProducer(self, fp, start, fsize)
                sp.start()
        else:
            sp = static.NoRangeStaticProducer(self, fp)
            sp.start()
        return server.NOT_DONE_YET

    def _renderResource(self, data=''):
        """
        Renders a resource.
        
        @param data: content of the document to be rendered
        @return:     None
        """
        if 'content-type' not in self.headers:
            self.setHeader('content-type', 'application/xml; charset=UTF-8')
        encoding = self.getHeader('accept-encoding')
        if encoding and encoding.find('gzip') >= 0:
            zbuf = StringIO.StringIO()
            zfile = gzip.GzipFile(None, 'wb', 9, zbuf)
            zfile.write(data)
            zfile.close()
            self.setHeader('content-encoding', 'gzip')
            data = zbuf.getvalue()
        self.setHeader('content-length', str(len(data)))
        if self.method == HEAD:
            self.write('')
        else:
            self.write(data)
        self.finish()
        return

    def _renderFolder(self, children={}):
        """
        Renders a folderish resource.
        
        @param children: dict of child objects implementing L{IResource}
        @return:         None
        """
        ids = sorted(children)
        data = ''
        for id in ids:
            obj = children.get(id)
            tag = 'resource'
            category = obj.category
            if obj.hidden:
                continue
            if obj.folderish:
                tag = 'folder'
                size = ''
            else:
                size = ' size="%d"' % obj.getMetadata().get('size', 0)
            if isinstance(id, unicode):
                id = id.encode('utf-8')
            if not hasattr(obj, 'url'):
                url = urllib.quote(addBase(self.path, id))
            else:
                url = obj.url
            data += RESOURCELIST_NODE % (tag, category, size, url, id, tag)

        data = str(RESOURCELIST_ROOT % (str(self.env.getRestUrl()), data))
        if 'content-type' not in self.headers:
            self.setHeader('content-type', 'application/xml; charset=UTF-8')
        format = self.args.get('format', [None])[0] or self.args.get('output', [None])[0]
        if format:
            reg = self.env.registry
            xslt = reg.stylesheets.get(package_id='seishub', resourcetype_id='stylesheet', type='resourcelist.%s' % format)
            if len(xslt):
                xslt = xslt[0]
                data = xslt.transform(data)
                if xslt.content_type:
                    self.setHeader('content-type', xslt.content_type + '; charset=UTF-8')
            else:
                msg = 'There is no stylesheet for requested format %s.'
                self.env.log.debug(msg % format)
        encoding = self.getHeader('accept-encoding')
        if encoding and encoding.find('gzip') >= 0:
            zbuf = StringIO.StringIO()
            zfile = gzip.GzipFile(None, 'wb', 9, zbuf)
            zfile.write(data)
            zfile.close()
            self.setHeader('content-encoding', 'gzip')
            data = zbuf.getvalue()
        self.setHeader('content-length', str(len(data)))
        if self.method == HEAD:
            self.write('')
        else:
            self.write(data)
        self.finish()
        return

    def notifyFinish(self):
        """
        Notify when finishing the request
        
        @return: A deferred. The deferred will be triggered when the request 
            is finished -- with a C{None} value if the request finishes 
            successfully or with an error if the request is stopped by the 
            client.
        """
        self.notifications.append(defer.Deferred())
        return self.notifications[(-1)]

    def connectionLost(self, reason):
        for d in self.notifications:
            d.errback(reason)

        self.notifications = []

    def finish(self):
        if not self.finished:
            http.Request.finish(self)
        for d in self.notifications:
            d.callback(None)

        self.notifications = []
        return


class WebServiceFactory(http.HTTPFactory):
    """
    Factory for the HTTP/HTTPS Server.
    """

    def __init__(self, env, log_file='', timeout=None):
        self.env = env
        http.HTTPFactory.__init__(self, log_file, timeout)
        self.protocol.requestFactory = WebRequest


class HTTPService(TCPServer):
    """
    HTTP Service.
    """

    def __init__(self, env):
        self.env = env
        http_port = env.config.getint('web', 'http_port') or HTTP_PORT
        log_file = env.config.get('web', 'http_log_file') or None
        if not os.path.isabs(log_file):
            log_file = os.path.join(self.env.config.path, log_file)
        factory = WebServiceFactory(env, log_file)
        TCPServer.__init__(self, http_port, factory)
        return


class HTTPSService(SSLServer):
    """
    HTTPS Service.
    """

    def __init__(self, env):
        self.env = env
        https_port = env.config.getint('web', 'https_port') or HTTPS_PORT
        priv, cert = self._getCertificates()
        context = ssl.DefaultOpenSSLContextFactory(str(priv), str(cert))
        log_file = env.config.get('web', 'https_log_file') or None
        if not os.path.isabs(log_file):
            log_file = os.path.join(self.env.config.path, log_file)
        factory = WebServiceFactory(env, log_file)
        SSLServer.__init__(self, https_port, factory, context, 1)
        return

    def _getCertificates(self):
        """
        Fetch HTTPS certificate paths from configuration.
        
        return: Paths to pkey and cert files.
        """
        pkey_file = self.env.config.get('web', 'https_pkey_file')
        cert_file = self.env.config.get('web', 'https_cert_file')
        if not os.path.isabs(pkey_file):
            pkey_file = os.path.join(self.env.config.path, pkey_file)
        if not os.path.isabs(cert_file):
            cert_file = os.path.join(self.env.config.path, cert_file)
        msg = 'HTTPS certificate file %s is missing!'
        if not os.path.isfile(cert_file):
            self.env.log.warn(msg % cert_file)
            return self._generateCertificates()
        if not os.path.isfile(pkey_file):
            self.env.log.warn(msg % pkey_file)
            return self._generateCertificates()
        return (
         pkey_file, cert_file)

    def _generateCertificates(self):
        """
        Generates new self-signed certificates.
        
        return: Paths to pkey and cert files.
        """
        from seishub.core.util import certgen
        from OpenSSL import crypto
        msg = 'Generating new certificate files for the HTTPS service ...'
        self.env.log.warn(msg)
        timespan = (0, 157680000)
        pkey_file = os.path.join(self.env.config.path, HTTPS_PKEY_FILE)
        cert_file = os.path.join(self.env.config.path, HTTPS_CERT_FILE)
        cakey = certgen.createKeyPair(certgen.TYPE_RSA, 1024)
        careq = certgen.createCertRequest(cakey, CN='SeisHub CA')
        cacert = certgen.createCertificate(careq, (careq, cakey), 0, timespan)
        pkey = certgen.createKeyPair(certgen.TYPE_RSA, 1024)
        server_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
        file(pkey_file, 'w').write(server_pkey)
        msg = 'Private key file %s has been created.'
        self.env.log.warn(msg % pkey_file)
        req = certgen.createCertRequest(pkey, CN='localhost:8443')
        cert = certgen.createCertificate(req, (cacert, cakey), 1, timespan)
        server_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        file(cert_file, 'w').write(server_cert)
        msg = 'Certificate file %s has been created.'
        self.env.log.warn(msg % cert_file)
        self.env.config.set('web', 'https_pkey_file', pkey_file)
        self.env.config.set('web', 'https_cert_file', cert_file)
        self.env.config.save()
        return (pkey_file, cert_file)


class WebService(service.MultiService):
    """
    MultiService for the HTTP/HTTPS server.
    """
    service_id = 'web'
    BoolOption('web', 'autostart', True, 'Run HTTP/HTTPS service on start-up.')
    IntOption('web', 'http_port', HTTP_PORT, 'HTTP port number.')
    IntOption('web', 'https_port', HTTPS_PORT, 'HTTPS port number.')
    Option('web', 'http_log_file', HTTP_LOG_FILE, 'HTTP access log file.')
    Option('web', 'https_log_file', HTTPS_LOG_FILE, 'HTTPS access log file.')
    Option('web', 'https_pkey_file', HTTPS_PKEY_FILE, 'Private key file.')
    Option('web', 'https_cert_file', HTTPS_CERT_FILE, 'Certificate file.')
    Option('web', 'admin_theme', ADMIN_THEME, 'Default administration theme.')
    ListOption('web', 'default_pages', (',').join(DEFAULT_PAGES), 'Default pages.')
    Option('web', 'google_api_key', '', 'Google API key.')

    def __init__(self, env):
        self.env = env
        service.MultiService.__init__(self)
        self.setName('HTTP/HTTPS Server')
        self.setServiceParent(env.app)
        http_service = HTTPService(env)
        http_service.setName('HTTP Server')
        self.addService(http_service)
        https_service = HTTPSService(env)
        https_service.setName('HTTPS Server')
        self.addService(https_service)

    def privilegedStartService(self):
        if self.env.config.getbool('web', 'autostart'):
            service.MultiService.privilegedStartService(self)

    def startService(self):
        if self.env.config.getbool('web', 'autostart'):
            service.MultiService.startService(self)

    def stopService(self):
        if self.running:
            service.MultiService.stopService(self)