# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bitpay_client/bp_lib.py
# Compiled at: 2014-07-01 11:22:58
"""
Permission is hereby granted to any person obtaining a copy of this software
and associated documentation for use and/or modification in association with
the bitpay.com service.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Bitcoin Python payment library using the bitpay.com service.
Version 1.0
"""
import bp_options, os, time, json, base64
from hashlib import sha256
import hmac, binascii, urllib2, urllib

def bpLog(contents):
    """
    Writes contents to a log file specified in the bp_options file or, if missing,
    defaults to a standard filename of 'bplog.txt'.
    
    @param mixed contents
    @return
    """
    if bp_options.bpOptions['logFile'] != '':
        file = os.path.realpath(__file__) + bp_options.bpOptions['logFile']
    else:
        file = os.path.realpath(__file__) + '/bplog.txt'
    with open(file, 'a') as (log_file):
        log_file.write(time.strftime('%m-%d %H:%M:%S') + ': ')
        log_file.write(json.dumps(contents) + '\n')


def bpCurl(url, apiKey, post=False):
    global response
    response = ''
    if url.strip() != '' and apiKey.strip() != '':
        cookie_handler = urllib2.HTTPCookieProcessor()
        redirect_handler = urllib2.HTTPRedirectHandler()
        opener = urllib2.build_opener(redirect_handler, cookie_handler)
        uname = base64.b64encode(apiKey)
        opener.addheaders = [
         ('Content-Type', 'application/json'),
         (
          'Authorization', 'Basic ' + uname),
         ('X-BitPay-Plugin-Info', 'pythonlib1.1')]
        if post:
            responseString = opener.open(url, urllib.urlencode(json.loads(post))).read()
        else:
            responseString = opener.open(url).read()
        try:
            response = json.loads(responseString)
        except ValueError:
            response = {'error': responseString}
            if bp_options.bpOptions['useLogging']:
                bpLog(('Error: ').responseString)

    return response


def bpCreateInvoice(orderId, price, posData, options={}):
    """
        Creates BitPay invoice via bpCurl.
        
        @param string orderId, string price, string posData, array options
        @return array response
    """
    options = dict(bp_options.bpOptions.items() + options.items())
    pos = {'posData': posData}
    if bp_options.bpOptions['verifyPos']:
        pos['hash'] = bpHash(str(posData), options['apiKey'])
    options['posData'] = json.dumps(pos)
    if len(options['posData']) > 100:
        return {'error': 'posData > 100 character limit. Are you using the posData hash?'}
    options['orderID'] = orderId
    options['price'] = price
    postOptions = [
     'orderID', 'itemDesc', 'itemCode', 'notificationEmail', 'notificationURL', 'redirectURL',
     'posData', 'price', 'currency', 'physical', 'fullNotifications', 'transactionSpeed', 'buyerName',
     'buyerAddress1', 'buyerAddress2', 'buyerCity', 'buyerState', 'buyerZip', 'buyerEmail', 'buyerPhone']
    for o in postOptions:
        if o in options:
            pos[o] = options[o]

    pos = json.dumps(pos)
    response = bpCurl('https://bitpay.com/api/invoice/', options['apiKey'], pos)
    if bp_options.bpOptions['useLogging']:
        bpLog('Create Invoice: ')
        bpLog(pos)
        bpLog('Response: ')
        bpLog(response)
    return response


def bpVerifyNotification(apiKey=False):
    """
    Call from your notification handler to convert _POST data to an object containing invoice data
    
    @param boolean apiKey
    @return mixed json
    """
    if not apiKey:
        apiKey = bp_options.bpOptions['apiKey']
    post = {}
    if not post:
        return 'No post data'
    jsondata = json.loads(post)
    if 'posData' not in jsondata:
        return 'no posData'
    posData = json.loads(jsondata['posData'])
    if bp_options.bpOptions['verifyPos'] and posData['hash'] != bpHash(str(posData['posData']), apiKey):
        return 'authentication failed (bad hash)'
    jsondata['posData'] = posData['posData']
    return jsondata


def bpGetInvoice(invoiceId, apiKey=False):
    """
    Retrieves an invoice from BitPay.  options can include 'apiKey'
    
    @param string invoiceId, boolean apiKey
    @return mixed json
    """
    if not apiKey:
        apiKey = bp_options.bpOptions['apiKey']
    response = bpCurl('https://bitpay.com/api/invoice/' + invoiceId, apiKey)
    response['posData'] = json.loads(response['posData'])
    response['posData'] = response['posData']['posData']
    return response


def bpHash(data, key):
    """
    Generates a base64 encoded keyed hash.
    
    @param string data, string key
    @return string hmac
    """
    hashed = hmac.new(key, data, sha256)
    return binascii.b2a_base64(hashed.digest())[:-1]


def bpDecodeResponse(response):
    """
    Decodes JSON response and returns
    associative array.
    
    @param string response
    @return array arrResponse
    """
    if response == '' or response is None:
        return 'Error: decodeResponse expects a string parameter.'
    return json.loads(response)