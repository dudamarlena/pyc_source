# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/payjp/test/test_integration.py
# Compiled at: 2018-06-22 02:45:13
# Size of source mod 2**32: 1880 bytes
import unittest, payjp
from six import string_types
from payjp.test.helper import PayjpTestCase, NOW, DUMMY_CARD

class AuthenticationErrorTest(PayjpTestCase):

    def test_invalid_credentials(self):
        key = payjp.api_key
        try:
            try:
                payjp.api_key = 'invalid'
                payjp.Customer.create()
            except payjp.error.AuthenticationError as e:
                self.assertEqual(401, e.http_status)
                self.assertTrue(isinstance(e.http_body, string_types))
                self.assertTrue(isinstance(e.json_body, dict))

        finally:
            payjp.api_key = key


class CardErrorTest(PayjpTestCase):

    def test_expired_card_props(self):
        EXPIRED_CARD = DUMMY_CARD.copy()
        EXPIRED_CARD['exp_month'] = NOW.month - 2
        EXPIRED_CARD['exp_year'] = NOW.year - 2
        try:
            payjp.Charge.create(amount=100, currency='jpy', card=EXPIRED_CARD)
        except payjp.error.CardError as e:
            self.assertEqual(402, e.http_status)
            self.assertTrue(isinstance(e.http_body, string_types))
            self.assertTrue(isinstance(e.json_body, dict))


class InvalidRequestErrorTest(PayjpTestCase):

    def test_nonexistent_object(self):
        try:
            payjp.Charge.retrieve('invalid')
        except payjp.error.InvalidRequestError as e:
            self.assertEqual(404, e.http_status)
            self.assertTrue(isinstance(e.http_body, string_types))
            self.assertTrue(isinstance(e.json_body, dict))

    def test_invalid_data(self):
        try:
            payjp.Charge.create()
        except payjp.error.InvalidRequestError as e:
            self.assertEqual(400, e.http_status)
            self.assertTrue(isinstance(e.http_body, string_types))
            self.assertTrue(isinstance(e.json_body, dict))


if __name__ == '__main__':
    unittest.main()