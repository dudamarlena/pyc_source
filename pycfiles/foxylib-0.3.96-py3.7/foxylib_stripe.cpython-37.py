# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/finance/payment/stripe/foxylib_stripe.py
# Compiled at: 2020-01-15 23:57:40
# Size of source mod 2**32: 349 bytes
import stripe
from foxylib.tools.env.env_tool import EnvTool

class FoxylibStripe:

    @classmethod
    def publishable_key(cls):
        return EnvTool.k2v('STRIPE_API_PUBLISHABLE_KEY')

    @classmethod
    def secret_key(cls):
        return EnvTool.k2v('STRIPE_API_SECRET_KEY')