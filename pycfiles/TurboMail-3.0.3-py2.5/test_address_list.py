# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/tests/test_address_list.py
# Compiled at: 2009-11-06 20:43:19
"""Test the TurboMail Message class."""
import logging, unittest
from turbomail.util import Address, AddressList
logging.disable(logging.WARNING)

class TestAddress(unittest.TestCase):

    def test_punycode(self):
        addr = Address('Foo', 'foo@exámple.test')
        self.assertEqual('Foo <foo@xn--exmple-qta.test>', str(addr))

    def test_initialization_with_addresslist_which_contains_only_email(self):
        emailaddress = 'foo@example.com'
        address = Address(AddressList(emailaddress))
        self.assertEqual(emailaddress, str(address))

    def test_initialization_with_addresslist_which_contains_tuple(self):
        name = 'Foo'
        emailaddress = 'foo@example.com'
        address = Address(AddressList((name, emailaddress)))
        self.assertEqual('%s <%s>' % (name, emailaddress), str(address))

    def test_initialization_with_tuple(self):
        name = 'Foo'
        emailaddress = 'foo@example.com'
        address = Address((name, emailaddress))
        self.assertEqual('%s <%s>' % (name, emailaddress), str(address))

    def test_initialization_with_string(self):
        emailaddress = 'foo@example.com'
        address = Address(emailaddress)
        self.assertEqual('%s' % emailaddress, str(address))

    def test_validation_truncates_at_second_at_character(self):
        self.assertEqual('bad@user', Address('bad@user@example.com'))

    def test_validation_rejects_addresses_without_at(self):
        self.assertRaises(ValueError, Address, 'baduser.example.com')

    def test_validation_accepts_uncommon_local_parts(self):
        Address('good-u+s+er@example.com')
        Address('steve.blackmill.rules.for.all@bar.blackmill-goldworks.example')
        Address('customer/department=shipping@example.com')
        Address('$A12345@example.com ')
        Address('!def!xyz%abc@example.com ')
        Address('_somename@example.com')
        Address("!$&*-=^`|~#%'+/?_{}@example.com")

    def test_validation_accepts_multilevel_domains(self):
        Address('foo@my.my.company-name.com')
        Address('blah@foo-bar.example.com')
        Address('blah@duckburg.foo-bar.example.com')

    def test_validation_accepts_domain_without_tld(self):
        self.assertEqual('user@company', Address('user@company'))

    def test_validation_rejects_local_parts_starting_or_ending_with_dot(self):
        self.assertRaises(ValueError, Address, '.foo@example.com')
        self.assertRaises(ValueError, Address, 'foo.@example.com')

    def test_validation_rejects_double_dot(self):
        self.assertRaises(ValueError, Address, 'foo..bar@example.com')


class TestAddressList(unittest.TestCase):
    """Test the AddressList helper class."""
    addresses = AddressList.protected('_addresses')

    def setUp(self):
        self._addresses = AddressList()

    def tearDown(self):
        del self.addresses

    def test_assignment(self):
        self.assertEqual([], self.addresses)

    def test_assign_single_address(self):
        address = 'user@example.com'
        self.addresses = address
        self.assertEqual(self.addresses, [address])
        self.assertEqual(str(self.addresses), address)

    def test_assign_list_of_addresses(self):
        addresses = [
         'user1@example.com', 'user2@example.com']
        self.addresses = addresses
        self.assertEqual((', ').join(addresses), str(self.addresses))
        self.assertEqual(addresses, self.addresses)

    def test_assign_single_named_address(self):
        addresses = ('Test User', 'user@example.com')
        self.addresses = addresses
        string_value = '%s <%s>' % addresses
        self.assertEqual(string_value, str(self.addresses))
        self.assertEqual([string_value], self.addresses)

    def test_assign_list_of_named_addresses(self):
        addresses = [
         ('Test User 1', 'user1@example.com'),
         ('Test User 2', 'user2@example.com')]
        self.addresses = addresses
        string_addresses = map(lambda value: str(Address(*value)), addresses)
        self.assertEqual((', ').join(string_addresses), str(self.addresses))
        self.assertEqual(string_addresses, self.addresses)

    def test_init_accepts_string_list(self):
        addresses = 'user1@example.com, user2@example.com'
        self.addresses = addresses
        self.assertEqual(addresses, str(self.addresses))

    def test_validation_strips_multiline_addresses(self):
        self.addresses = 'user.name+test@info.example.com'
        evil_lines = ['eviluser@example.com', 'To: spammeduser@example.com',
         'From: spammeduser@example.com']
        evil_input = ('\n').join(evil_lines)
        self.addresses.append(evil_input)
        self.assertEqual(['user.name+test@info.example.com', evil_lines[0]], self.addresses)

    def test_return_addresses_as_strings(self):
        self.addresses = 'foo@exámple.test'
        encoded_address = 'foo@xn--exmple-qta.test'
        self.assertEqual([encoded_address], self.addresses.string_addresses)