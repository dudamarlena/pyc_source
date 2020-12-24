# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_strings_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 9788 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsStringsAssertions(unittest.TestCase):

    def test_is_string_pass(self):
        self.assertIsInstance(Is('Hello').string, Is)

    def test_is_subtype_of_fail(self):
        with self.assertRaises(CheckError):
            Is(123).string

    def test_is_not_string_pass(self):
        self.assertIsInstance(Is(123).not_string, Is)

    def test_is_not_subtype_of_fail(self):
        obj = 'I actually am a string'
        with self.assertRaises(CheckError):
            Is(obj).not_string

    def test_is_contains_numbers_pass(self):
        obj = 'Hello123World'
        self.assertIsInstance(Is(obj).contains_numbers, Is)

    def test_is_contains_numbers_fail(self):
        obj = 'Hello world'
        with self.assertRaises(CheckError):
            Is(obj).contains_numbers

    def test_is_not_contains_numbers_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).not_contains_numbers, Is)

    def test_is_not_contains_numbers_fail(self):
        obj = 'Hello123World'
        with self.assertRaises(CheckError):
            Is(obj).not_contains_numbers

    def test_is_only_numbers_pass(self):
        obj = '12399'
        self.assertIsInstance(Is(obj).only_numbers, Is)

    def test_is_only_numbers_fail(self):
        with self.assertRaises(CheckError):
            Is('123Hello123World').only_numbers
        with self.assertRaises(CheckError):
            Is('Hello World').only_numbers

    def test_is_contains_chars_pass(self):
        obj = '12a3'
        self.assertIsInstance(Is(obj).contains_chars, Is)

    def test_is_contains_chars_fail(self):
        with self.assertRaises(CheckError):
            Is('01234').contains_chars

    def test_is_not_contains_chars_pass(self):
        obj = '123'
        self.assertIsInstance(Is(obj).not_contains_chars, Is)

    def test_is_not_contains_chars_fail(self):
        with self.assertRaises(CheckError):
            Is('012a34').not_contains_chars

    def test_is_contains_chars_only_pass(self):
        obj = 'abc'
        self.assertIsInstance(Is(obj).only_chars, Is)

    def test_is_contains_chars_only_fail(self):
        with self.assertRaises(CheckError):
            Is('012a34').only_chars

    def test_is_contains_spaces_pass(self):
        obj = 'hello world'
        self.assertIsInstance(Is(obj).contains_spaces, Is)

    def test_is_contains_spaces_fail(self):
        with self.assertRaises(CheckError):
            Is('goodbye').contains_spaces

    def test_is_contains_char_pass(self):
        obj = 'hello world'
        self.assertIsInstance(Is(obj).contains_char('w'), Is)

    def test_is_contains_char_fail(self):
        with self.assertRaises(CheckError):
            Is('goodbye').contains_char('z')

    def test_is_not_contains_char_pass(self):
        obj = 'hello world'
        self.assertIsInstance(Is(obj).not_contains_char('z'), Is)

    def test_is_not_contains_char_fail(self):
        with self.assertRaises(CheckError):
            Is('goodbye').not_contains_char('y')

    def test_is_shorter_than_pass(self):
        obj = 'Hi'
        self.assertIsInstance(Is(obj).shorter_than(5), Is)

    def test_is_shorter_than_fail(self):
        with self.assertRaises(CheckError):
            Is('goodbye').shorter_than(4)

    def test_is_longer_than_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).longer_than(5), Is)

    def test_is_longer_than_fail(self):
        with self.assertRaises(CheckError):
            Is('goodbye').longer_than(7)

    def test_is_length_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).length(len(obj)), Is)

    def test_is_length_fail(self):
        obj = 'goodbye'
        with self.assertRaises(CheckError):
            Is(obj).length(len(obj) - 1)
        with self.assertRaises(CheckError):
            Is(obj).length(len(obj) + 1)

    def test_is_not_length_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).not_length(len(obj) + 1), Is)
        self.assertIsInstance(Is(obj).not_length(len(obj) - 1), Is)

    def test_is_not_length_fail(self):
        obj = 'goodbye'
        with self.assertRaises(CheckError):
            Is(obj).not_length(len(obj))

    def test_is_lowercase_fail(self):
        obj = 'good Bye'
        with self.assertRaises(CheckError):
            Is(obj).lowercase

    def test_is_not_lowercase_fail(self):
        obj = 'Goodbye'
        with self.assertRaises(CheckError):
            Is(obj).not_lowercase

    def test_is_uppercase_fail(self):
        obj = 'Goodbye'
        with self.assertRaises(CheckError):
            Is(obj).uppercase

    def test_is_not_uppercase_fail(self):
        obj = 'good Bye'
        with self.assertRaises(CheckError):
            Is(obj).not_uppercase

    def test_is_camelcase_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).camelcase, Is)

    def test_is_camelcase_fail(self):
        obj = 'goodbye'
        with self.assertRaises(CheckError):
            Is(obj).camelcase

    def test_is_not_camelcase_pass(self):
        obj = 'hello world'
        self.assertIsInstance(Is(obj).not_camelcase, Is)

    def test_is_not_camelcase_fail(self):
        obj = 'GoodBye'
        with self.assertRaises(CheckError):
            Is(obj).not_camelcase

    def test_is_snakecase_fail(self):
        obj = 'goodbye'
        with self.assertRaises(CheckError):
            Is(obj).snakecase

    def test_is_not_snakecase_fail(self):
        obj = 'good_bye'
        with self.assertRaises(CheckError):
            Is(obj).not_snakecase

    def test_is_json_pass(self):
        obj = '{"name": "pass"}'
        self.assertIsInstance(Is(obj).json, Is)

    def test_is_json_fail(self):
        obj = 'goodbye'
        with self.assertRaises(CheckError):
            Is(obj).json

    def test_is_not_json_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).not_json, Is)

    def test_is_not_json_fail(self):
        obj = '{"name": "pass"}'
        with self.assertRaises(CheckError):
            Is(obj).not_json

    def test_is_yaml_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).yaml, Is)

    def test_is_yaml_fail(self):
        obj = 'xxx: {'
        with self.assertRaises(CheckError):
            Is(obj).yaml

    def test_is_not_yaml_pass(self):
        obj = 'xxx: {'
        self.assertIsInstance(Is(obj).not_yaml, Is)

    def test_is_not_yaml_fail(self):
        obj = '\n     ---\n      doe: "a deer, a female deer"\n      calling-birds:\n        - louie\n        - fred\n     '.strip()
        with self.assertRaises(CheckError):
            Is(obj).not_yaml

    def test_is_xml_pass(self):
        obj = '<Agenda>\n     <type>gardening</type>\n     <Activity>\n       <type>cooking</type>\n     </Activity>\n    </Agenda>'
        self.assertIsInstance(Is(obj).xml, Is)

    def test_is_xml_fail(self):
        obj = 'not xml'
        with self.assertRaises(CheckError):
            Is(obj).xml

    def test_is_not_xml_pass(self):
        obj = 'Hello world'
        self.assertIsInstance(Is(obj).not_xml, Is)

    def test_is_not_xml_fail(self):
        obj = '<Agenda></Agenda>'
        with self.assertRaises(CheckError):
            Is(obj).not_xml

    def test_is_matches_pass(self):
        obj = 'abyss'
        pattern = '^a...s$'
        self.assertIsInstance(Is(obj).matches(pattern), Is)

    def test_is_matches_fail(self):
        obj = 'goodbye'
        pattern = '^a...s$'
        with self.assertRaises(CheckError):
            Is(obj).matches(pattern)

    def test_is_not_matches_pass(self):
        obj = 'goodbye'
        pattern = '^a...s$'
        self.assertIsInstance(Is(obj).not_matches(pattern), Is)

    def test_is_not_matches_fail(self):
        obj = 'abyss'
        pattern = '^a...s$'
        with self.assertRaises(CheckError):
            Is(obj).not_matches(pattern)