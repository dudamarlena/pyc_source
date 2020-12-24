# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/customer_tests.py
# Compiled at: 2015-03-05 16:14:12
from __future__ import unicode_literals
import vcr, tests
from thunderhead.builder import customers

class CustomerTests(tests.VCRBasedTests):

    @vcr.use_cassette(b'get_all_customers.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'none')
    def test_get_all_customers(self):
        usage_customers = customers.get_all_customers(tests.CONNECTION)
        self.assertEquals(isinstance(usage_customers, list), True)
        self.assertEquals(len(usage_customers), 3)

    @vcr.use_cassette(b'get_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'none')
    def test_get_single_customer(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1)
        c1_dict = {b'country': b'United States', b'customer_id': b'1', b'postal_code': b'78232', 
           b'name': b'1018700'}
        self.assertDictEqual(usage_customer, c1_dict)

    @vcr.use_cassette(b'get_customer_not_found.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'none')
    def test_get_single_customer_not_found(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1000000)
        self.assertIsNone(usage_customer)

    @vcr.use_cassette(b'create_new_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def test_create_new_customer(self):
        customer_info = {b'name': b'15551212', 
           b'country': b'US', 
           b'postal_code': b'79762'}
        new_customer = customers.create_customer(tests.CONNECTION, customer_info)
        customer_info[b'country'] = b'United States'
        self.assertDictContainsSubset(customer_info, new_customer)

    @vcr.use_cassette(b'create_new_customer_using_country_name.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def test_create_new_customer_using_country_name(self):
        customer_info = {b'name': b'15551212111', 
           b'country': b'United States', 
           b'postal_code': b'79762'}
        with self.assertRaises(customers.InvalidCountryCodeException):
            customers.create_customer(tests.CONNECTION, customer_info)

    @vcr.use_cassette(b'create_new_customer_no_country_code.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def test_create_new_customer_no_country_code(self):
        customer_info = {b'name': b'15551212', 
           b'postal_code': b'Unknown'}
        with self.assertRaises(customers.MissingProperty):
            customers.create_customer(tests.CONNECTION, customer_info)

    @vcr.use_cassette(b'create_new_customer_duplicate_bad_request.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def test_create_new_customer_duplicate_found(self):
        customer_info = {b'name': b'5551212', 
           b'country': b'US', 
           b'postal_code': b'79762'}
        with self.assertRaises(customers.DuplicateCustomerException):
            customers.create_customer(tests.CONNECTION, customer_info)

    @vcr.use_cassette(b'delete_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'none')
    def test_delete_customer(self):
        deleted_customer = customers.delete_customer(tests.CONNECTION, 1)
        self.assertEquals(deleted_customer, True)

    @vcr.use_cassette(b'get_customer_rules.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def no_test_get_customer_rules(self):
        rules = customers.get_customer_rules(tests.CONNECTION, 2)
        self.assertEquals(rules, list)

    @vcr.use_cassette(b'update_customer_name.yaml', cassette_library_dir=tests.fixtures_path, record_mode=b'once')
    def test_update_customer_name(self):
        customer_info = {b'name': b'123333-updated', 
           b'country': b'US', 
           b'postal_code': b'79762'}
        customer_id = 10
        updated_customer = customers.update_customer(tests.CONNECTION, customer_id, customer_info)
        self.assertIsInstance(updated_customer, dict)

    def test_customer_builder(self):
        customer = {b'country': b'US', 
           b'name': b'¿Cómo', 
           b'postal_code': b'78555'}
        xml = customers._build_customer_payload(customer)
        res = b'<customer xmlns="http://www.vmware.com/UM"><name>&#191;C&#243;mo</name><country>US</country><postalCode>78555</postalCode></customer>'
        self.assertEqual(xml, res)