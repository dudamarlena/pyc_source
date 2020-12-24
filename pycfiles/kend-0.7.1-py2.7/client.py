# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/kend/client.py
# Compiled at: 2017-06-19 12:03:51
import collections, kend.converter.XML, kend.model, sys, urllib, urllib2
from kend.log import logger
from lxml import etree

class Client:
    """Client stub for talking to a Utopia service"""

    def __init__(self, service=None, loginCallback=None):
        if isinstance(service, Service):
            self.service = service
        elif isinstance(service, basestring):
            self.service = Service(service)
        else:
            self.service = Service()
        self.agent = ('Kend/{} Python-urllib2/{}.{}.{}').format(kend.model.VERSION, *sys.version_info[:3])
        self.loginCallback = loginCallback
        if self.loginCallback is None:
            try:
                from utopia import bridge, auth
                self.loginCallback = auth.TokenGenerator(self.service.resources['auth']['href'])
                self.agent = '%s %s' % (bridge.agent_string, self.agent)
            except:
                import traceback
                traceback.print_exc()

                def null_token(old_token):
                    return

                self.loginCallback = null_token
                logger.warning('No login callback set - authentication impossible')

        self.authToken = None
        self._login()
        return

    def _login(self):
        if self.loginCallback is not None:
            self.authToken = self.loginCallback(self.authToken)
            if isinstance(self.authToken, tuple):
                url = 'https://utopia.cs.manchester.ac.uk/auth/0.1/users/signin'
                data = self._urlencode({'email': self.authToken[0], 'password': self.authToken[1]})
                result = json.loads(urllib2.urlopen(url, data).read())
                self.authToken = result.get('token')
            return self.authToken
        else:
            logger.warning('Login unsuccessful - authentication impossible [loginCallback == None]')
            return
            return

    def _urlencode(self, formData, doseq=True):
        if isinstance(formData, collections.Mapping):
            formData = formData.items()
        encodedFormData = []
        for key, values in formData:
            if isinstance(values, basestring):
                values = [
                 values]
            values = [ value.encode('utf8') for value in values ]
            encodedFormData.append((key.encode('utf8'), values))

        return urllib.urlencode(encodedFormData, doseq)

    def _encode(self, data, json=False):
        if json:
            return (json.dumps(data), 'application/json')
        if isinstance(data, kend.model.__classes__):
            return kend.converter.XML.serialise(data)
        if isinstance(data, basestring):
            return (data.encode('utf8'), 'text/plain')
        if isinstance(data, collections.Sequence) or isinstance(data, collections.Mapping):
            return (self._urlencode(data), 'application/x-www-form-urlencoded')

    def _makeRequest(self, url, method='GET', body_data=None, query_data=None, headers={}):
        headers['User-Agent'] = self.agent
        body = None
        if body_data is not None:
            body, mime_type = self._encode(body_data)
            headers['Content-Type'] = mime_type
        if query_data is not None:
            url = ('{}?{}').format(url, self._urlencode(query_data))
        logger.debug(('Client request: {}').format(url))
        return urllib2.Request(url, body, headers)

    def _request(self, url, method=None, body_data=None, query_data=None, headers={}):
        loginAttempts = 3
        response = None
        headers = {}
        while loginAttempts > 0:
            loginAttempts = loginAttempts - 1
            if self.authToken is not None:
                if isinstance(self.authToken, basestring):
                    headers['Authorization'] = 'Kend %s' % self.authToken
                elif len(self.authToken) == 2:
                    try:
                        headers['Authorization'] = 'Basic %s' % base64.standard_b64encode('%s:%s' % self.authToken)
                    except:
                        pass

            if method is None:
                if body_data is None:
                    method = 'GET'
                else:
                    method = 'POST'
            request = self._makeRequest(url, method=method, body_data=body_data, query_data=query_data, headers=headers)
            try:
                response = urllib2.urlopen(request, timeout=15)
            except urllib2.HTTPError as e:
                if e.code == 401:
                    self._login()
                    continue
                else:
                    raise

            break

        if response is not None:
            mime_type = response.info().gettype()
            params = response.info().getplist()
            if mime_type == kend.converter.XML.MIME_TYPE:
                for cls in kend.model.__classes__:
                    if 'type=%s' % cls.__mime__ in params or cls.__mime__ in params:
                        response = response.read()
                        response = kend.converter.XML.parse(response, cls)
                        break

        return response

    def documents(self, documentref):
        try:
            from utopia import auth
            return self._request(auth._getServiceBaseUri('documents'), method='POST', body_data=documentref)
        except ImportError:
            return self._request(self.service.resources['documents']['href'], method='POST', body_data=documentref)

    def document(self, uri):
        try:
            from utopia import auth
            return self._request(auth._getServiceBaseUri('documents'), query_data={'document': uri})
        except ImportError:
            return self._request(self.service.resources['documents']['href'], query_data={'document': uri})

    def searchDocuments(self, **kwargs):
        from utopia import auth
        return self._request(auth._getServiceBaseUri('documents'), query_data=kwargs)

    def submitMetadata(self, edit_uri, document):
        return self._request(edit_uri, method='PUT', body_data=document)

    def annotations(self, **kwargs):
        try:
            from utopia import auth
            return self._request(auth._getServiceBaseUri('annotations'), query_data=kwargs)
        except ImportError:
            return self._request(self.service.resources['annotations']['href'], query_data=kwargs)

    def lookup(self, **kwargs):
        return self._request('https://utopia.cs.manchester.ac.uk/kend/0.7/define/lookup', query_data=kwargs)

    def lookupDBpedia(self, **kwargs):
        return self._request('https://utopia.cs.manchester.ac.uk/kend/0.7/define/dbpedia', query_data=kwargs)

    def persistDocument(self, ann, **kwargs):
        try:
            from utopia import auth
            kwargs['annotation'] = ann
            self._request(auth._getServiceBaseUri('documents'), method='POST', body_data=kwargs)
        except urllib2.HTTPError as e:
            logger.error('Failed to save annotations to server: %s' % repr(e))

    def persistAnnotation(self, annotation, **kwargs):
        try:
            from utopia import auth
            if annotation.edit is not None:
                return self._request(annotation.edit, method='PUT', body_data=annotation, query_data=kwargs)
            return self._request(auth._getServiceBaseUri('annotations'), method='POST', body_data=annotation, query_data=kwargs)
        except urllib2.HTTPError as e:
            logger.error('Failed to save annotation to server: %s' % repr(e))

        return

    def deleteAnnotation(self, annotation, **kwargs):
        try:
            from utopia import auth
            if annotation.edit is not None:
                return self._request(annotation.edit, method='DELETE')
        except urllib2.HTTPError as e:
            logger.error('Failed to delete annotation from server: %s' % repr(e))
            raise

        return

    def lookupIdentifier(self, **kwargs):
        return self._request('define/identifier', query_data=kwargs)


class Service:
    """Service object representing a Utopia service"""

    def __init__(self, serviceUri='https://utopia.cs.manchester.ac.uk/kend/0.7/services'):
        response = urllib2.urlopen(serviceUri)
        xml = etree.parse(response)
        services = xml.getroot()
        service = services.xpath('kend:service', namespaces=kend.model.NS)[0]
        self.serviceUri = serviceUri
        self.version = services.attrib['version']
        self.name = service.attrib['name']
        logger.debug(('Found service: "{}" v{} ({})').format(self.name, self.version, serviceUri))
        self.resources = {}
        resources = service.xpath('kend:resource', namespaces=kend.model.NS)
        _type_max_length = max(len(resource.attrib.get('type', '')) for resource in resources)
        for resource in resources:
            key = resource.attrib['type']
            value = {k:v for k, v in resource.attrib.items() if k != 'type' if k != 'type'}
            self.resources[key] = value
            logger.debug((' - {{:>{}}}: {{}}').format(_type_max_length).format(key, value))

    def client(self, *args, **kwargs):
        return Client(self, *args, **kwargs)