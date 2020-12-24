# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bitpay_client/BitPay.py
# Compiled at: 2014-07-02 06:15:53
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

class API(object):

    def __init__(self, apiKey='', verifyPos='true', notificationEmail='', notificationURL='', redirectURL='', currency='BTC', physical='true', fullNotifications='true', transactionSpeed='low', logFile='/bplog.log', useLogging=False):
        self.apiKey = apiKey
        self.verifyPos = verifyPos
        self.notificationEmail = notificationEmail
        self.notificationURL = notificationURL
        self.redirectURL = redirectURL
        self.currency = currency
        self.physical = physical
        self.fullNotifications = fullNotifications
        self.transactionSpeed = transactionSpeed
        self.logFile = logFile
        self.useLogging = useLogging

    def log(self, contents):
        """
        Writes contents to a log file specified in the bp_options file or, if missing,
        defaults to a standard filename of 'bplog.log'.
        
        @param mixed contents
        @return
        """
        if self.logFile != '':
            file = os.path.realpath(os.path.dirname(__file__)) + self.logFile
        else:
            file = os.path.realpath(os.path.dirname(__file__)) + '/bplog.log'
        with open(file, 'a') as (log_file):
            log_file.write(time.strftime('%m-%d %H:%M:%S') + ': ')
            log_file.write(json.dumps(contents) + '\n')

    def curl(self, url, apiKey, post=False):
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
                if self.useLogging:
                    self.log(('Error: ').responseString)

        return response

    def createInvoice(self, orderId, price, posData, options={}):
        """
            Creates BitPay invoice via self.curl.
            
            @param string orderId, string price, string posData, array options
            @return array response
        """
        options = dict(bp_options.bpOptions.items() + options.items())
        pos = {'posData': posData}
        if self.verifyPos:
            pos['hash'] = self.hash(str(posData), options['apiKey'])
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
        response = self.curl('https://bitpay.com/api/invoice/', options['apiKey'], pos)
        if self.useLogging:
            self.log('Create Invoice: ')
            self.log(pos)
            self.log('Response: ')
            self.log(response)
        return response

    def verifyNotification(self, apiKey=False):
        """
        Call from your notification handler to convert _POST data to an object containing invoice data
        
        @param boolean apiKey
        @return mixed json
        """
        if not apiKey:
            apiKey = self.apiKey
        post = {}
        if not post:
            return 'No post data'
        jsondata = json.loads(post)
        if 'posData' not in jsondata:
            return 'no posData'
        posData = json.loads(jsondata['posData'])
        if self.verifyPos and posData['hash'] != self.hash(str(posData['posData']), apiKey):
            return 'authentication failed (bad hash)'
        jsondata['posData'] = posData['posData']
        return jsondata

    def getInvoice(self, invoiceId, apiKey=False):
        """
        Retrieves an invoice from BitPay.  options can include 'apiKey'
        
        @param string invoiceId, boolean apiKey
        @return mixed json
        """
        if not apiKey:
            apiKey = self.apiKey
        response = self.curl('https://bitpay.com/api/invoice/' + invoiceId, apiKey)
        response['posData'] = json.loads(response['posData'])
        response['posData'] = response['posData']['posData']
        return response

    def hash(self, data, key):
        """
        Generates a base64 encoded keyed hash.
        
        @param string data, string key
        @return string hmac
        """
        hashed = hmac.new(key, data, sha256)
        return binascii.b2a_base64(hashed.digest())[:-1]

    def decodeResponse(self, response):
        """
        Decodes JSON response and returns
        associative array.
        
        @param string response
        @return array arrResponse
        """
        if response == '' or response is None:
            return 'Error: decodeResponse expects a string parameter.'
        return json.loads(response)