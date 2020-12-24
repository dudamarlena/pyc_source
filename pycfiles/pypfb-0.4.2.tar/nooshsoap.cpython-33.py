# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/nooshsoap.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 2078 bytes
__doc__ = '\nCreated on Nov 5, 2013\n\n@author: "Colin Manning"\n'
import cgi, urllib.request, urllib.parse, urllib.error

def createNooshSOAPMessage(noosh_soap_api, body):
    message = '\n    <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"\n        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"\n        xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n        xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"\n        xmlns:SOAP-XML="http://xml.apache.org/xml-soap"\n        xmlns:noosh="Noosh">\n'
    message += '\n    <SOAP-ENV:Header>\n        <authentication domain="%s" identity="%s" sharedPassword="%s"></authentication>\n    </SOAP-ENV:Header>\n' % (noosh_soap_api['domain'], noosh_soap_api['identity'], noosh_soap_api['sharedPassword'])
    message += body
    message += '</SOAP-ENV:Envelope>'
    return message


def createRemoteFileUploadBody(noosh_soap_api, upload_by, project_id, file_name, file_url):
    file_url_bits = file_url.split('?')
    encoded_file_url = file_url_bits[0]
    if len(file_url_bits) == 2:
        query_params = {}
        query_bits = file_url_bits[1].split('&')
        for query_bit in query_bits:
            p = query_bit.split('=')
            query_params[p[0]] = p[1]

        encoded_file_url += '?' + urllib.parse.urlencode(query_params)
    return '\n    <SOAP-ENV:Body>\n        <attachRemoteFile xmlns="DocumentService">\n            <creator xsi:type="noosh:ServiceEntity">\n                <domain xsi:type="xsd:string">%s</domain>\n                <identity xsi:type="xsd:string">%s</identity>\n            </creator>\n            <prjId xsi:type="xsd:long">%s</prjId>\n            <fileTitle xsi:type="xsd:string">%s</fileTitle>\n            <remoteFileURI xsi:type="xsd:string">%s</remoteFileURI>\n            <isPublic xsi:type="xsd:boolean">true</isPublic>\n        </attachRemoteFile>\n    </SOAP-ENV:Body>\n' % (noosh_soap_api['domain'], upload_by, project_id, file_name, cgi.escape(encoded_file_url))