# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/customer_tests.py
# Compiled at: 2014-09-23 02:57:43
# Size of source mod 2**32: 4389 bytes
import vcr, tests
from thunderhead.builder import customers

class CustomerTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_all_customers.yaml', cassette_library_dir=tests.fixtures_path, record_mode='none')
    def test_get_all_customers(self):
        usage_customers = customers.get_all_customers(tests.CONNECTION)
        self.assertEquals(isinstance(usage_customers, list), True)
        self.assertEquals(len(usage_customers), 3)

    @vcr.use_cassette('get_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode='none')
    def test_get_single_customer(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1)
        c1_dict = {'country': 'United States',  'customer_id': '1',  'postal_code': '78232', 
         'name': '1018700'}
        self.assertDictEqual(usage_customer, c1_dict)

    @vcr.use_cassette('get_customer_not_found.yaml', cassette_library_dir=tests.fixtures_path, record_mode='none')
    def test_get_single_customer_not_found(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1000000)
        self.assertIsNone(usage_customer)

    @vcr.use_cassette('create_new_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_new_customer(self):
        customer_info = {'name': '15551212', 
         'country': 'US', 
         'postal_code': '79762'}
        new_customer = customers.create_customer(tests.CONNECTION, customer_info)
        customer_info['country'] = 'United States'
        self.assertDictContainsSubset(customer_info, new_customer)

    @vcr.use_cassette('create_new_customer_no_country_code.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_new_customer_no_country_code(self):
        customer_info = {'name': '15551212', 
         'postal_code': 'Unknown'}
        with self.assertRaises(customers.MissingProperty):
            customers.create_customer(tests.CONNECTION, customer_info)

    @vcr.use_cassette('create_new_customer_duplicate_bad_request.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_create_new_customer_duplicate_found(self):
        customer_info = {'name': '5551212', 
         'country': 'US', 
         'postal_code': '79762'}
        with self.assertRaises(customers.DuplicateCustomerException):
            customers.create_customer(tests.CONNECTION, customer_info)

    @vcr.use_cassette('delete_customer.yaml', cassette_library_dir=tests.fixtures_path, record_mode='none')
    def test_delete_customer(self):
        deleted_customer = customers.delete_customer(tests.CONNECTION, 1)
        self.assertEquals(deleted_customer, True)

    @vcr.use_cassette('get_customer_rules.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def no_test_get_customer_rules(self):
        rules = customers.get_customer_rules(tests.CONNECTION, 2)
        self.assertEquals(rules, list)