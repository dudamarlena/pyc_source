# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat64/egg/authorize/tests/test_xml.py
# Compiled at: 2009-08-21 14:09:21
from unittest import TestCase
import os, decimal
up = os.path.dirname
j = os.path.join
from schema import SCHEMA
try:
    from lxml.etree import XMLSchema, XMLParser, fromstring
except ImportError:
    raise Exception('lxml 2.0.3+ is needed to run authorize tests')

from authorize import gen_xml as x, responses, cim, arb
parser = XMLParser()
schema_validator = XMLSchema(fromstring(SCHEMA, parser))
DELIMITER = '---------------------------------------------------------------------------------------'

def to_tree(s):
    return fromstring(s, parser)


def assertValid(s):
    schema_validator.assertValid(to_tree(s))


class TestXML(TestCase):

    def setUp(self):
        self.cim_old = cim.Api.request

        def validateRequest(self, body):
            assertValid(body)
            assert_other = getattr(self, 'assert_other', None)
            if assert_other is not None:
                assert_other(body)
            return

        cim.Api.request = validateRequest
        self.cim = cim.Api('foo', 'bar', is_test=True)
        self.arb_old = arb.Api.request
        arb.Api.request = lambda self, body: assertValid(body)
        self.arb = arb.Api('foo', 'bar', is_test=True)

    def tearDown(self):
        cim.Api.request = self.cim_old
        arb.Api.request = self.arb_old

    def test_general_examples(self):
        """
        Test that response parser don't break with example patterns
        given by Authorize.Net
        """
        examples = file(j(up(os.path.abspath(__file__)), 'CIMXMLExamples.txt')).read().split(DELIMITER)
        for example in examples:
            example = example.strip()
            try:
                resp = x.to_dict(example, responses.cim_map)
            except responses.AuthorizeError:
                resp = x.to_dict(example, responses.cim_map, do_raise=False)
                assert resp.messages.message.code.text_ in responses.cim_map
            else:
                assert resp.messages.message.code.text_ == 'I00001'

    def test_parse_direct_response(self):
        """
        The direct response string returned by Authorize.net can be
        quite interesting to parse. We verify that it is correctly
        handled.
        """
        response = '<?xml version="1.0" encoding="utf-8"?>\n<createCustomerProfileTransactionResponse xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">\n  <messages>\n    <resultCode>Ok</resultCode>\n    <message>\n      <code>I00001</code>\n      <text>Successful.</text>\n    </message>\n  </messages>\n  <directResponse>*1*;*1*;*1*;*This transaction has been approved.*;*000000*;*Y*;*2000000001*;*INV000001*;*description of transaction*;*10.95*;*CC*;*auth_capture*;*custId123*;*John*;*Doe*;**;*123 Main St., foo*;*Bellevue*;*WA*;*98004*;*USA*;*000-000-0000*;**;*mark@example.com*;*John*;*Doe*;**;*123 Main St.*;*Bellevue*;*WA*;*98004*;*USA*;*1.00*;*0.00*;*2.00*;*FALSE*;*PONUM000001*;*D18EB6B211FE0BBF556B271FDA6F92EE*;*M*;*buaaahahah , *;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;**;*wallers,*</directResponse>\n</createCustomerProfileTransactionResponse>'
        resp = x.to_dict(response, responses.cim_map, delimiter=';', encapsulator='*')
        assert resp.direct_response.code == '1'
        assert resp.direct_response.address == '123 Main St., foo'
        assert resp.direct_response.holder_verification == 'buaaahahah , '

    def test_parser_to_dict(self):
        """
        Test that the dict parser works as expected
        """
        xml = '<foo>\n    <bar>baz</bar>\n    <quz>\n        <wow>works!</wow>\n    </quz>\n</foo>\n'
        d = x.to_dict(xml, {})
        assert d.bar.text_ == 'baz'
        assert d.quz.wow.text_ == 'works!'

    def test_create_profile(self):
        """
        Test that the XML generated for create_profile is valid according
        to the XMLSchema.
        """
        self.cim.create_profile(card_number='42222222222', expiration_date='2010-04', customer_id='dialtone')

        def assert_other(message):
            assert 'creditCardNumber' not in message
            assert 'bankAccount' in message

        self.assert_other = assert_other
        try:
            self.cim.create_profile(customer_id='dialtone', profile_type='bank', name_on_account='John Doe', routing_number='12345678', account_number='1234567890')
        finally:
            del self.assert_other

        self.cim.create_profile(card_number='42222222222', expiration_date='2010-04', customer_id='dialtone', ship_phone='415-415-4154', ship_first_name='valentino')
        payment_profiles = [
         dict(card_number='43333333333', expiration_date='2010-04'),
         dict(profile_type='bank', name_on_account='John Doeð', routing_number='12345678', account_number='1234567890')]

        def assert_other(message):
            assert 'John Doe' in message
            assert '43333333333' in message
            assert 'valentino' in message

        self.assert_other = assert_other
        try:
            self.cim.create_profile(customer_id='dialtone', payment_profiles=payment_profiles, ship_phone='415-415-4154', ship_first_name='valentino')
        finally:
            del self.assert_other

    def test_create_payment_profile(self):
        """
        Test that the XML generated for create_payment_profile is valid
        according to the XMLSchema.
        """
        self.cim.create_payment_profile(customer_profile_id='300', customer_type='individual', card_number='42222222222', expiration_date='2009-10')

    def test_create_shipping_address(self):
        """
        Test that the XML generated for create_shipping_address is valid
        according to the XMLSchema.
        """
        self.cim.create_shipping_address(customer_profile_id=100, ship_phone='415-415-4154', ship_first_name='valentino')

    def test_create_profile_transaction(self):
        """
        Test that the XML generated for create_profile_transaction is
        valid according to the XMLSchema, and that approval_code is
        only required when capture_only is used as profile_type.
        """
        line_items = [
         {'item_id': '45', 'name': 'hello', 
            'description': 'foobar', 
            'quantity': 5, 
            'unit_price': decimal.Decimal('30.4')}]
        self.cim.create_profile_transaction(profile_type='auth_only', amount=12.34, tax_amount=3.0, ship_amount=3.0, duty_amount=3.0, line_items=line_items, customer_profile_id='123', customer_payment_profile_id='123', invoice_number='12345', tax_exempt=True)
        try:
            self.cim.create_profile_transaction(profile_type='capture_only', amount=12.34, tax_amount=3.0, ship_amount=3.0, duty_amount=3.0, line_items=line_items, customer_profile_id=123, customer_payment_profile_id=223, invoice_number=12345, tax_exempt=True)
        except KeyError, e:
            assert 'approval_code' in str(e)
            self.cim.create_profile_transaction(profile_type='capture_only', amount=12.34, tax_amount=3.0, ship_amount=3.0, duty_amount=3.0, line_items=line_items, customer_profile_id=123, customer_payment_profile_id=223, invoice_number=12345, tax_exempt=True, approval_code=134323)

    def test_delete_profile(self):
        """
        Test that the XML generated for delete_profile is valid
        according to the XMLSchema.
        """
        self.cim.delete_profile(customer_profile_id='123')

    def test_delete_payment_profile(self):
        """
        Test that the XML generated for delete_payment_profile is valid
        according to the XMLSchema.
        """
        self.cim.delete_payment_profile(customer_profile_id='123', customer_payment_profile_id='432')

    def test_delete_shipping_address(self):
        """
        Test that the XML generated for delete_shipping_address is valid
        according to the XMLSchema.
        """
        self.cim.delete_shipping_address(customer_profile_id='123', customer_address_id='543')

    def test_get_profile(self):
        """
        Test that the XML generated for get_profile is valid
        according to the XMLSchema.
        """
        self.cim.get_profile(customer_profile_id='123')

    def test_get_payment_profile(self):
        """
        Test that the XML generated for get_payment_profile is valid
        according to the XMLSchema.
        """
        self.cim.get_payment_profile(customer_profile_id='655', customer_payment_profile_id='999')

    def test_get_shipping_address(self):
        """
        Test that the XML generated for get_shipping_address is valid
        according to the XMLSchema.
        """
        self.cim.get_shipping_address(customer_profile_id='900', customer_address_id='344')

    def test_update_profile(self):
        """
        Test that the XML generated for update_profile is valid
        according to the XMLSchema.
        """
        self.cim.update_profile(customer_id='222', description='Foo bar baz quz', email='dialtone@gmail.com', customer_profile_id='122')

    def test_update_payment_profile(self):
        """
        Test that the XML generated for update_payment_profile is valid
        according to the XMLSchema.
        """
        self.cim.update_payment_profile(customer_profile_id='122', customer_payment_profile_id='444', card_number='422222222222', expiration_date='2009-10')

    def test_update_shipping_address(self):
        """
        Test that the XML generated for update_shipping_address is valid
        according to the XMLSchema.
        """
        self.cim.update_shipping_address(customer_profile_id='222', customer_address_id='444', first_name='pippo', phone='415-415-4154')

    def test_validate_payment_profile(self):
        """
        Test that the XML generated for validate_payment_profile is valid
        according to the XMLSchema.
        """
        self.cim.validate_payment_profile(customer_profile_id='222', customer_payment_profile_id='444', customer_address_id='555')

    def test_create_subscription(self):
        """
        Test that XML generated for arb subscription creation is valid
        according to XMLSchema.
        """
        try:
            self.arb.create_subscription(trial_occurrences=4, interval_length=1, interval_unit=arb.MONTHS_INTERVAL, start_date='2008-09-09', amount=39.99, card_number='4222222222222', expiration_date='2009-10', bill_first_name='Michael', bill_last_name='Pool')
        except KeyError:
            pass

        self.arb.create_subscription(trial_amount=5.0, trial_occurrences=4, interval_length=1, interval_unit=arb.MONTHS_INTERVAL, start_date='2008-09-09', amount=39.99, card_number='4222222222222', expiration_date='2009-10', bill_first_name='Michael', bill_last_name='Pool')
        self.arb.create_subscription(trial_amount=5.0, trial_occurrences=4, interval_length=1, interval_unit=arb.MONTHS_INTERVAL, start_date='2008-09-09', amount=39.99, card_number='4222222222222', expiration_date='2009-10', ship_first_name='valentino', first_name='valentino', bill_first_name='valentino', bill_last_name='Pool', driver_number='55555', driver_state='CA', driver_birth='1990-09-09')

    def test_update_subscription(self):
        """
        Test that XML generated for arb subscription creation is valid
        according to XMLSchema.
        """
        args = dict(trial_amount=5.0, trial_occurrences=4, interval_length=1, interval_unit=arb.MONTHS_INTERVAL, start_date='2008-09-09', amount=39.99, card_number='4222222222222', expiration_date='2009-10', ship_first_name='valentino', first_name='valentino', bill_first_name='valentino', bill_last_name='pool', driver_number='55555', driver_state='CA', driver_birth='1990-09-09')
        try:
            self.arb.update_subscription(**args)
        except KeyError:
            self.arb.update_subscription(subscription_id='1234', **args)

    def test_cancel_subscription(self):
        """
        Cancel subscription is a generated correctly
        """
        try:
            self.arb.cancel_subscription()
        except KeyError:
            self.arb.cancel_subscription(subscription_id='1234')