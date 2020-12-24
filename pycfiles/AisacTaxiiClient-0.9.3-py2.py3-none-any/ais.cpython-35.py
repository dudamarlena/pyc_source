# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/ais.py
# Compiled at: 2018-10-22 10:39:31
# Size of source mod 2**32: 5065 bytes
__doc__ = '\nAIS.py - A Python interface for the Swisscom All-in Signing Service.\n\n:copyright: (c) 2016 by Camptocamp\n:license: AGPLv3, see README and LICENSE for more details\n\n'
import base64, json, re, uuid, requests
from .pdf import PDF
from . import exceptions
url = 'https://ais.swisscom.com/AIS-Server/rs/v1.0/sign'

class AIS(object):
    """AIS"""

    def __init__(self, customer, key_static, cert_file, cert_key):
        """Initialize an AIS client with authentication information."""
        self.customer = customer
        self.key_static = key_static
        self.cert_file = cert_file
        self.cert_key = cert_key
        self.byte_range = None
        self.last_request_id = None

    def _request_id(self):
        request_id = self.last_request_id = uuid.uuid4().hex
        return request_id

    def post(self, payload):
        """ Do the post request for this payload and return the signature part
        of the json response.

        :type payload: str
        :rtype: dict
        """
        headers = {'Accept': 'application/json', 
         'Content-Type': 'application/json;charset=UTF-8'}
        cert = (
         self.cert_file, self.cert_key)
        response = requests.post(url, data=payload, headers=headers, cert=cert)
        sign_resp = response.json()['SignResponse']
        result = sign_resp['Result']
        if 'Error' in result['ResultMajor']:
            raise exceptions.error_for(response)
        return sign_resp

    def sign_batch(self, pdfs):
        """Sign a batch of files.

        :type pdfs: list(PDF)
        """
        PDF.prepare_batch(pdfs)
        payload_documents = {'DocumentHash' + str(count):{'@ID': count, 'dsig.DigestMethod': {'@Algorithm': 'http://www.w3.org/2001/04/xmlenc#sha256'}, 'dsig.DigestValue': pdf.digest()} for count, pdf in enumerate(pdfs)}
        payload = {'SignRequest': {'@RequestID': self._request_id(), 
                         '@Profile': 'http://ais.swisscom.ch/1.0', 
                         'OptionalInputs': {'ClaimedIdentity': {'Name': ':'.join((self.customer, self.key_static))}, 
                                            
                                            'SignatureType': 'urn:ietf:rfc:3369', 
                                            'AdditionalProfile': 'http://ais.swisscom.ch/1.0/profiles/batchprocessing', 
                                            
                                            'AddTimestamp': {'@Type': 'urn:ietf:rfc:3161'}, 
                                            'sc.AddRevocationInformation': {'@Type': 'BOTH'}}, 
                         
                         'InputDocuments': payload_documents}}
        payload_json = json.dumps(payload, indent=4)
        payload_json = re.sub('"DocumentHash\\d+"', '"DocumentHash"', payload_json)
        sign_resp = self.post(payload_json)
        other = sign_resp['SignatureObject']['Other']['sc.SignatureObjects']
        for signature_object in other['sc.ExtendedSignatureObject']:
            signature = Signature(base64.b64decode(signature_object['Base64Signature']['$']))
            which_document = int(signature_object['@WhichDocument'])
            pdf = pdfs[which_document]
            pdf.write_signature(signature)

    def sign_one_pdf(self, pdf):
        """Sign the given pdf file.

        :type pdf: PDF
        """
        pdf.prepare()
        payload = {'SignRequest': {'@RequestID': self._request_id(), 
                         '@Profile': 'http://ais.swisscom.ch/1.0', 
                         'OptionalInputs': {'ClaimedIdentity': {'Name': ':'.join((self.customer, self.key_static))}, 
                                            
                                            'SignatureType': 'urn:ietf:rfc:3369', 
                                            'AddTimestamp': {'@Type': 'urn:ietf:rfc:3161'}, 
                                            'sc.AddRevocationInformation': {'@Type': 'BOTH'}}, 
                         
                         'InputDocuments': {'DocumentHash': {'dsig.DigestMethod': {'@Algorithm': 'http://www.w3.org/2001/04/xmlenc#sha256'}, 
                                                             
                                                             'dsig.DigestValue': pdf.digest()}}}}
        sign_response = self.post(json.dumps(payload))
        signature = Signature(base64.b64decode(sign_response['SignatureObject']['Base64Signature']['$']))
        pdf.write_signature(signature)


class Signature(object):
    """Signature"""

    def __init__(self, contents):
        """Build a Signature."""
        self.contents = contents