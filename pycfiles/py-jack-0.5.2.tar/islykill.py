# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/islykill.py
# Compiled at: 2013-08-15 06:58:28
import urllib2, xml.etree.ElementTree as ET, logging
wsdl_url = 'https://egov.webservice.is/sst/runtime.asvc/com.actional.soapstation.eGOVDKM_AuthConsumer.AccessPoint?WSDL'
username = ''
password = ''
service_id = ''
logger = logging.getLogger(__name__)

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


def generate_saml_from_token(token, ipAddress):
    if username == '' or password == '' or service_id == '':
        return {'error': 'You must set `username`, `password` and `service_id` fields!'}
    else:
        xml = '<?xml version="1.0" ?>\n    <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:egov="http://www.kogun.is/eGov/eGovSAMLGenerator.webServices">\n        <soapenv:Header/>\n        <soapenv:Body>\n            <egov:generateSAMLFromToken soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n                <token xsi:type="xsd:string">%(token)s</token>\n                <ipAddress xsi:type="xsd:string">%(ipAddress)s</ipAddress>\n            </egov:generateSAMLFromToken>\n        </soapenv:Body>\n    </soapenv:Envelope>' % {'token': token, 'ipAddress': ipAddress}
        headers = {'Soapaction': 'generateSAMLFromToken', 
           'Content-Type': 'text/xml', 
           'Host': service_id, 
           'User-Agent': service_id}
        req = urllib2.Request(wsdl_url, headers=headers)
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, wsdl_url, username, password)
        auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(auth_manager)
        urllib2.install_opener(opener)
        try:
            handler = urllib2.urlopen(req, xml)
        except urllib2.HTTPError as e:
            return {'error': 'HTTPError = ' + str(e.code)}
        except urllib2.URLError as e:
            return {'error': 'URLError = ' + str(e.reason)}
        except httplib.HTTPException as e:
            return {'error': 'HTTPException'}
        except Exception:
            import traceback
            return {'error': 'generic exception: ' + traceback.format_exc()}

        status_code = handler.getcode()
        response = to_unicode_or_bust(handler.read())
        logger.debug('status code: ', status_code)
        logger.debug(response)
        try:
            saml_raw = ET.fromstring(response.encode('utf-8')).find('.//saml').text
        except AttributeError:
            error = ET.fromstring(response.encode('utf-8')).find('.//message').text
            return {'error': error}

        saml_tree = ET.fromstring(saml_raw.encode('utf-8'))
        name_node = saml_tree.find('.//{urn:oasis:names:tc:SAML:1.0:assertion}NameIdentifier')
        name = name_node.text
        subject_locality_node = saml_tree.find('.//{urn:oasis:names:tc:SAML:1.0:assertion}SubjectLocality')
        ip_address = subject_locality_node.attrib['IPAddress']
        ssn_attribute_node = saml_tree.find('.//{urn:oasis:names:tc:SAML:1.0:assertion}AttributeValue')
        ssn = ssn_attribute_node.text
        result = {'name': name, 
           'ip_address': ip_address, 
           'ssn': ssn}
        return result
        return