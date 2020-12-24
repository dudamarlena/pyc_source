# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/_pay.py
# Compiled at: 2016-06-14 19:24:16
import braintree
from cantools.web import respond, succeed, fail, cgi_get
from cantools import config, util
braintree.Configuration.configure(braintree.Environment.Sandbox, merchant_id=config.pay.merchant, public_key=config.pay.public, private_key=config.pay.private)

def response():
    nonce = cgi_get('nonce', required=False)
    if nonce:
        result = braintree.Transaction.sale({'amount': cgi_get('amount'), 
           'payment_method_nonce': nonce, 
           'options': {'submit_for_settlement': True}})
        util.log(result)
        if not result.is_success:
            msg = result.errors.deep_errors
            if not msg:
                msg = '%s: %s' % (result.transaction.processor_settlement_response_code,
                 result.transaction.processor_settlement_response_text)
            fail('%s (%s)' % (result.message, msg))
    else:
        succeed(braintree.ClientToken.generate())


respond(response)