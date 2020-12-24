# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/client.py
# Compiled at: 2016-09-19 07:37:17
import logging, urlparse
from django.conf import settings as django_settings
from django.utils import timezone
import lxml.etree, requests
logger = logging.getLogger(__name__)

class ClientError(Exception):
    pass


class ResponseParseError(ClientError):
    pass


class ResponseStatusError(ClientError):
    pass


class RequestError(ClientError):

    def __init__(self, message, response):
        super(RequestError, self).__init__(message)
        self.response = response


class UnknownStatusError(ResponseParseError):
    pass


class Response(object):
    ns_namespace = 'http://uri.etsi.org/TS102204/v1.1.2#'

    def __init__(self, content):
        etree = lxml.etree.fromstring(content)
        self.init_response_attributes(etree)

    def init_response_attributes(self, etree):
        """ Define response attributes based on valimo request content """
        raise NotImplementedError


class Request(object):
    url = NotImplemented
    template = NotImplemented
    response_class = NotImplemented
    settings = getattr(django_settings, 'NODECONCUTOR_AUTH_VALIMO', {})

    @classmethod
    def execute(cls, **kwargs):
        url = cls._get_url()
        headers = {'content-type': 'text/xml', 
           'SOAPAction': url}
        data = cls.template.strip().format(AP_ID=cls.settings['AP_ID'], AP_PWD=cls.settings['AP_PWD'], Instant=cls._format_datetime(timezone.now()), DNSName=cls.settings['DNSName'], **kwargs)
        cert = (
         cls.settings['cert_path'], cls.settings['key_path'])
        logger.debug('Executing POST request to %s with data:\n %s \nheaders: %s', url, data, headers)
        response = requests.post(url, data=data, headers=headers, cert=cert, verify=False)
        if response.ok:
            return cls.response_class(response.content)
        message = 'Failed to execute POST request against %s endpoint. Response [%s]: %s' % (
         url, response.status_code, response.content)
        raise RequestError(message, response)

    @classmethod
    def _format_datetime(cls, d):
        return d.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    @classmethod
    def _format_transaction_id(cls, transaction_id):
        return ('_' + transaction_id)[:32]

    @classmethod
    def _get_url(cls):
        return urlparse.urljoin(cls.settings['URL'], cls.url)


class SignatureResponse(Response):

    def init_response_attributes(self, etree):
        try:
            self.backend_transaction_id = etree.xpath('//MSS_SignatureResp')[0].attrib['MSSP_TransID']
            self.status = etree.xpath('//ns6:StatusCode', namespaces={'ns6': self.ns_namespace})[0].attrib['Value']
        except (IndexError, KeyError, lxml.etree.XMLSchemaError) as e:
            raise ResponseParseError('Cannot parse signature response: %s. Response content: %s' % (
             e, lxml.etree.tostring(etree)))


class SignatureRequest(Request):
    url = '/MSSP/services/MSS_Signature'
    template = '\n        <?xml version="1.0" encoding="UTF-8"?>\n        <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"\n                          xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n                          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n            <soapenv:Body>\n                <MSS_Signature xmlns="">\n                <MSS_SignatureReq MajorVersion="1" MessagingMode="{MessagingMode}" MinorVersion="1" TimeOut="300">\n                    <ns1:AP_Info AP_ID="{AP_ID}" AP_PWD="{AP_PWD}" AP_TransID="{AP_TransID}"\n                                 Instant="{Instant}" xmlns:ns1="http://uri.etsi.org/TS102204/v1.1.2#"/>\n                    <ns2:MSSP_Info xmlns:ns2="http://uri.etsi.org/TS102204/v1.1.2#">\n                        <ns2:MSSP_ID>\n                            <ns2:DNSName>{DNSName}</ns2:DNSName>\n                        </ns2:MSSP_ID>\n                    </ns2:MSSP_Info>\n                    <ns3:MobileUser xmlns:ns3="http://uri.etsi.org/TS102204/v1.1.2#">\n                        <ns3:MSISDN>{MSISDN}</ns3:MSISDN>\n                    </ns3:MobileUser>\n                    <ns4:DataToBeSigned Encoding="UTF-8" MimeType="text/plain" xmlns:ns4="http://uri.etsi.org/TS102204/v1.1.2#">\n                        {DataToBeSigned}\n                    </ns4:DataToBeSigned>\n                    <ns5:SignatureProfile xmlns:ns5="http://uri.etsi.org/TS102204/v1.1.2#">\n                        <ns5:mssURI>{SignatureProfile}</ns5:mssURI>\n                    </ns5:SignatureProfile>\n                    <ns6:MSS_Format xmlns:ns6="http://uri.etsi.org/TS102204/v1.1.2#">\n                        <ns6:mssURI>http://uri.etsi.org/TS102204/v1.1.2#PKCS7</ns6:mssURI>\n                    </ns6:MSS_Format>\n                </MSS_SignatureReq>\n                </MSS_Signature>\n            </soapenv:Body>\n        </soapenv:Envelope>\n    '
    response_class = SignatureResponse

    @classmethod
    def execute(cls, transaction_id, phone, message):
        kwargs = {'MessagingMode': 'asynchClientServer', 
           'AP_TransID': cls._format_transaction_id(transaction_id), 
           'MSISDN': phone, 
           'DataToBeSigned': '%s %s' % (cls.settings['message_prefix'], message), 
           'SignatureProfile': cls.settings['SignatureProfile']}
        return super(SignatureRequest, cls).execute(**kwargs)


class Statuses(object):
    OK = 'OK'
    PROCESSING = 'Processing'
    ERRED = 'Erred'

    @classmethod
    def map(cls, status_code):
        if status_code == '502':
            return cls.OK
        if status_code == '504':
            return cls.PROCESSING
        raise UnknownStatusError('Received unsupported status in response: %s' % status_code)


class StatusResponse(Response):

    def init_response_attributes(self, etree):
        try:
            status_code = etree.xpath('//ns5:StatusCode', namespaces={'ns5': self.ns_namespace})[0].attrib['Value']
        except (IndexError, KeyError, lxml.etree.XMLSchemaError) as e:
            raise ResponseParseError('Cannot parse status response: %s. Response content: %s' % (
             e, lxml.etree.tostring(etree)))

        self.status = Statuses.map(status_code)
        try:
            civil_number_tag = etree.xpath('//ns4:UserIdentifier', namespaces={'ns4': self.ns_namespace})[0]
        except IndexError:
            return

        try:
            self.civil_number = civil_number_tag.text.split('=')[1]
        except IndexError:
            raise ResponseParseError('Cannot get civil_number from tag text: %s' % civil_number_tag.text)


class ErredStatusResponse(Response):
    soapenv_namespace = 'http://www.w3.org/2003/05/soap-envelope'

    def init_response_attributes(self, etree):
        self.status = Statuses.ERRED
        try:
            self.details = etree.xpath('//soapenv:Text', namespaces={'soapenv': self.soapenv_namespace})[0].text
        except (IndexError, lxml.etree.XMLSchemaError) as e:
            raise ResponseParseError('Cannot parse error status response: %s. Response content: %s' % (
             e, lxml.etree.tostring(etree)))


class StatusRequest(Request):
    url = '/MSSP/services/MSS_StatusPort'
    template = '\n        <?xml version="1.0" encoding="UTF-8"?>\n        <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"\n                              xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n                              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n            <soapenv:Body>\n            <MSS_StatusQuery xmlns="">\n            <MSS_StatusReq MajorVersion="1" MinorVersion="1">\n                <ns1:AP_Info AP_ID="{AP_ID}" AP_PWD="{AP_PWD}" AP_TransID="{AP_TransID}"\n                                 Instant="{Instant}" xmlns:ns1="http://uri.etsi.org/TS102204/v1.1.2#"/>\n                <ns2:MSSP_Info xmlns:ns2="http://uri.etsi.org/TS102204/v1.1.2#">\n                    <ns2:MSSP_ID>\n                        <ns2:DNSName>{DNSName}</ns2:DNSName>\n                    </ns2:MSSP_ID>\n                </ns2:MSSP_Info>\n                <ns3:MSSP_TransID xmlns:ns3="http://uri.etsi.org/TS102204/v1.1.2#">{MSSP_TransID}</ns3:MSSP_TransID>\n            </MSS_StatusReq>\n            </MSS_StatusQuery>\n            </soapenv:Body>\n        </soapenv:Envelope>\n    '
    response_class = StatusResponse

    @classmethod
    def execute(cls, transaction_id, backend_transaction_id):
        kwargs = {'AP_TransID': cls._format_transaction_id(transaction_id), 
           'MSSP_TransID': backend_transaction_id}
        try:
            return super(StatusRequest, cls).execute(**kwargs)
        except RequestError as e:
            return ErredStatusResponse(e.response.content)