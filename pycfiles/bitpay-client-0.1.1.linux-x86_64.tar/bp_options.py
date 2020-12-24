# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bitpay_client/bp_options.py
# Compiled at: 2014-07-01 11:22:58
"""
(c) 2014 BitPay, Inc.

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
bpOptions = {}
bpOptions['apiKey'] = ''
bpOptions['verifyPos'] = 'true'
bpOptions['notificationEmail'] = ''
bpOptions['notificationURL'] = ''
bpOptions['redirectURL'] = ''
bpOptions['currency'] = 'BTC'
bpOptions['physical'] = 'true'
bpOptions['fullNotifications'] = 'true'
bpOptions['transactionSpeed'] = 'low'
bpOptions['logFile'] = '/bplog.txt'
bpOptions['useLogging'] = False