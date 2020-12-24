# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/jive_sdk/__init__.py
# Compiled at: 2015-10-16 16:53:03
import hmac, hashlib, base64, urllib, json, requests
from collections import OrderedDict
import logging

def is_valid_registration_notification(payload, clientSecret=None):
    """
    This method implements the Jive logic to validate if an add-on registration request originates from an authentic Jive instance.
     
    Arguments:
    1) payload (REQUIRED) - The JSON structure (not a string) Jive sends to the register_url and unregister_url defined in your add-on's meta.json
    { 
        "clientId" : "xxxxx",
        "tenantId" : "xxxxx",
        "jiveSignatureURL" : "xxxxx",
        "clientSecret" : "xxxxx",
        "jiveSignature" : "xxxxx",
        "jiveUrl" : "xxxxx",
        "timestamp" : "2015-10-16T18:11:11.113+0000"
    }
    
    2) clientSecret (OPTIONAL) - In the event of an UNREGISTER event, Jive will NOT send the clientSecret again.  To validate, you will need to provide the clientSecret with this argument. 

    Examples of calls to this method include:
        jive_sdk.is_valid_registration_notification(your_json) - Used for Register Events
        jive_sdk.is_valid_registration_notification(your_json, clientSecret="your_secret") - Used for UNregister Events
        
    For more details, check out the Jive Developer Community
        https://community.jivesoftware.com/docs/DOC-99941
        https://community.jivesoftware.com/docs/DOC-156557
        
    """
    jiveSignatureURL = payload['jiveSignatureURL']
    jiveSignature = payload['jiveSignature']
    payload.pop('jiveSignature')
    if not clientSecret:
        if not payload['clientSecret']:
            logging.warn('Registration Event with no Secret, Invalid Payload')
            return False
        payload['clientSecret'] = hashlib.sha256(payload['clientSecret']).hexdigest()
    else:
        if 'clientSecret' in payload:
            logging.warn('Client Secret already in payload, ignoring argument.  Make sure you are not passing in clientId on register events')
        else:
            payload['clientSecret'] = clientSecret
        data = ''
        for k, v in sorted(OrderedDict(payload).items()):
            data += k + ':' + v + '\n'

        logging.debug('Signature Validation URL: [%s]', jiveSignatureURL)
        logging.debug('Signature Data:\n%s', data)
        res = requests.post(jiveSignatureURL, data=data, headers={'X-Jive-MAC': jiveSignature})
        if res.status_code == 204:
            logging.info('Validation Successful [%d]', res.status_code)
            return True
    logging.warn('Validation Failed [%d]', res.status_code)
    return False


def is_valid_authorization(authorization, clientId, clientSecret):
    """
    This method implements the Jive logic to validate a signed-fetch request from the OpenSocial container in Jive request.
     
    Arguments:

    1) authorization (REQUIRED) - the value of the "Authorization" header on the request
    2) clientId (REQUIRED) - the shared clientId for the add-on
    3) clientSecret (REQUIRED) - the clientSecret for the add-on

    Examples of calls to this method include:
        jive_sdk.is_valid_authorization(your_authorization_header,your_clientId,your_clientSecret)
        
    For more details, check out the Jive Developer Community
        https://community.jivesoftware.com/docs/DOC-99941
        https://community.jivesoftware.com/docs/DOC-156557
        https://community.jivesoftware.com/docs/DOC-163586
        
    """
    if not authorization:
        logging.warn('Invalid Authorization (null/empty)')
        return False
    fields = authorization.split(' ')
    if fields[0] != 'JiveEXTN':
        logging.warn('Invalid Authorization Type [%s]', fields[0])
        return False
    if not fields[1]:
        logging.warn('Invalid Parameters [None]')
        return False
    flag = fields[0]
    message = ''
    signature = ''
    for kv in fields[1].split('&'):
        key, value = kv.split('=')
        if key == 'client_id' and value != clientId:
            logging.warn('ClientId [%s] did not match expected ClientId [%s]', key, clientId)
            return False
        if key == 'signature':
            signature = urllib.unquote(value).decode()
        else:
            message += '&' + key + '=' + value

    message = message[1:]
    if clientSecret.endswith('.s'):
        clientSecret = clientSecret[:-2]
    secret = base64.b64decode(clientSecret)
    dig = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
    expectedSignature = base64.b64encode(dig).decode()
    expectedSignature = urllib.unquote(expectedSignature).decode()
    if signature != expectedSignature:
        logging.warn('Signatures did NOT match! [expected: %s]  [actual: %s]', expectedSignature, signature)
        return False
    return True