# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/text_format_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 89921 bytes
"""Test for google.protobuf.text_format."""
import io, math, re, string, textwrap, six
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import any_pb2
from google.protobuf import any_test_pb2
from google.protobuf import map_unittest_pb2
from google.protobuf import unittest_custom_options_pb2
from google.protobuf import unittest_mset_pb2
from google.protobuf import unittest_pb2
from google.protobuf import unittest_proto3_arena_pb2
from google.protobuf import descriptor_pb2
from google.protobuf.internal import any_test_pb2 as test_extend_any
from google.protobuf.internal import message_set_extensions_pb2
from google.protobuf.internal import test_util
from google.protobuf import descriptor_pool
from google.protobuf import text_format
from google.protobuf.internal import _parameterized

class SimpleTextFormatTests(unittest.TestCase):

    def testQuoteMarksAreSingleChars(self):
        for quote in text_format._QUOTES:
            self.assertEqual(1, len(quote))


class TextFormatBase(unittest.TestCase):

    def ReadGolden(self, golden_filename):
        with test_util.GoldenFile(golden_filename) as (f):
            if str is bytes:
                return f.readlines()
            else:
                return [golden_line.decode('utf-8') for golden_line in f]

    def CompareToGoldenFile(self, text, golden_filename):
        golden_lines = self.ReadGolden(golden_filename)
        self.assertMultiLineEqual(text, ''.join(golden_lines))

    def CompareToGoldenText(self, text, golden_text):
        self.assertEqual(text, golden_text)

    def RemoveRedundantZeros(self, text):
        text = text.replace('e+0', 'e+').replace('e+0', 'e+').replace('e-0', 'e-').replace('e-0', 'e-')
        text = re.compile('\\.0$', re.MULTILINE).sub('', text)
        return text


@_parameterized.parameters(unittest_pb2, unittest_proto3_arena_pb2)
class TextFormatMessageToStringTests(TextFormatBase):

    def testPrintExotic(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_int64.append(-9223372036854775808)
        message.repeated_uint64.append(18446744073709551615)
        message.repeated_double.append(123.456)
        message.repeated_double.append(1.23e+22)
        message.repeated_double.append(1.23e-18)
        message.repeated_string.append('\x00\x01\x07\x08\x0c\n\r\t\x0b\\\'"')
        message.repeated_string.append('üꜟ')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_format.MessageToString(message)), 'repeated_int64: -9223372036854775808\nrepeated_uint64: 18446744073709551615\nrepeated_double: 123.456\nrepeated_double: 1.23e+22\nrepeated_double: 1.23e-18\nrepeated_string: "\\000\\001\\007\\010\\014\\n\\r\\t\\013\\\\\\\'\\""\nrepeated_string: "\\303\\274\\352\\234\\237"\n')

    def testPrintExoticUnicodeSubclass(self, message_module):

        class UnicodeSub(six.text_type):
            pass

        message = message_module.TestAllTypes()
        message.repeated_string.append(UnicodeSub('üꜟ'))
        self.CompareToGoldenText(text_format.MessageToString(message), 'repeated_string: "\\303\\274\\352\\234\\237"\n')

    def testPrintNestedMessageAsOneLine(self, message_module):
        message = message_module.TestAllTypes()
        msg = message.repeated_nested_message.add()
        msg.bb = 42
        self.CompareToGoldenText(text_format.MessageToString(message, as_one_line=True), 'repeated_nested_message { bb: 42 }')

    def testPrintRepeatedFieldsAsOneLine(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_int32.append(1)
        message.repeated_int32.append(1)
        message.repeated_int32.append(3)
        message.repeated_string.append('Google')
        message.repeated_string.append('Zurich')
        self.CompareToGoldenText(text_format.MessageToString(message, as_one_line=True), 'repeated_int32: 1 repeated_int32: 1 repeated_int32: 3 repeated_string: "Google" repeated_string: "Zurich"')

    def VerifyPrintShortFormatRepeatedFields(self, message_module, as_one_line):
        message = message_module.TestAllTypes()
        message.repeated_int32.append(1)
        message.repeated_string.append('Google')
        message.repeated_string.append('Hello,World')
        message.repeated_foreign_enum.append(unittest_pb2.FOREIGN_FOO)
        message.repeated_foreign_enum.append(unittest_pb2.FOREIGN_BAR)
        message.repeated_foreign_enum.append(unittest_pb2.FOREIGN_BAZ)
        message.optional_nested_message.bb = 3
        for i in (21, 32):
            msg = message.repeated_nested_message.add()
            msg.bb = i

        expected_ascii = 'optional_nested_message {\n  bb: 3\n}\nrepeated_int32: [1]\nrepeated_string: "Google"\nrepeated_string: "Hello,World"\nrepeated_nested_message {\n  bb: 21\n}\nrepeated_nested_message {\n  bb: 32\n}\nrepeated_foreign_enum: [FOREIGN_FOO, FOREIGN_BAR, FOREIGN_BAZ]\n'
        if as_one_line:
            expected_ascii = expected_ascii.replace('\n', ' ')
            expected_ascii = re.sub('\\s+', ' ', expected_ascii)
            expected_ascii = re.sub('\\s$', '', expected_ascii)
        actual_ascii = text_format.MessageToString(message,
          use_short_repeated_primitives=True, as_one_line=as_one_line)
        self.CompareToGoldenText(actual_ascii, expected_ascii)
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(actual_ascii, parsed_message)
        self.assertEqual(parsed_message, message)

    def testPrintShortFormatRepeatedFields(self, message_module):
        self.VerifyPrintShortFormatRepeatedFields(message_module, False)
        self.VerifyPrintShortFormatRepeatedFields(message_module, True)

    def testPrintNestedNewLineInStringAsOneLine(self, message_module):
        message = message_module.TestAllTypes()
        message.optional_string = 'a\nnew\nline'
        self.CompareToGoldenText(text_format.MessageToString(message, as_one_line=True), 'optional_string: "a\\nnew\\nline"')

    def testPrintExoticAsOneLine(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_int64.append(-9223372036854775808)
        message.repeated_uint64.append(18446744073709551615)
        message.repeated_double.append(123.456)
        message.repeated_double.append(1.23e+22)
        message.repeated_double.append(1.23e-18)
        message.repeated_string.append('\x00\x01\x07\x08\x0c\n\r\t\x0b\\\'"')
        message.repeated_string.append('üꜟ')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_format.MessageToString(message,
          as_one_line=True)), 'repeated_int64: -9223372036854775808 repeated_uint64: 18446744073709551615 repeated_double: 123.456 repeated_double: 1.23e+22 repeated_double: 1.23e-18 repeated_string: "\\000\\001\\007\\010\\014\\n\\r\\t\\013\\\\\\\'\\"" repeated_string: "\\303\\274\\352\\234\\237"')

    def testRoundTripExoticAsOneLine(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_int64.append(-9223372036854775808)
        message.repeated_uint64.append(18446744073709551615)
        message.repeated_double.append(123.456)
        message.repeated_double.append(1.23e+22)
        message.repeated_double.append(1.23e-18)
        message.repeated_string.append('\x00\x01\x07\x08\x0c\n\r\t\x0b\\\'"')
        message.repeated_string.append('üꜟ')
        wire_text = text_format.MessageToString(message, as_one_line=True,
          as_utf8=False)
        parsed_message = message_module.TestAllTypes()
        r = text_format.Parse(wire_text, parsed_message)
        self.assertIs(r, parsed_message)
        self.assertEqual(message, parsed_message)
        wire_text = text_format.MessageToString(message, as_one_line=True,
          as_utf8=True)
        parsed_message = message_module.TestAllTypes()
        r = text_format.Parse(wire_text, parsed_message)
        self.assertIs(r, parsed_message)
        self.assertEqual(message, parsed_message, '\n%s != %s' % (message, parsed_message))

    def testPrintRawUtf8String(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_string.append('ü\tꜟ')
        text = text_format.MessageToString(message, as_utf8=True)
        golden_unicode = 'repeated_string: "ü\\tꜟ"\n'
        golden_text = golden_unicode if six.PY3 else golden_unicode.encode('utf-8')
        self.CompareToGoldenText(text, golden_text)
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(text, parsed_message)
        self.assertEqual(message, parsed_message, '\n%s != %s  (%s != %s)' % (
         message, parsed_message, message.repeated_string[0],
         parsed_message.repeated_string[0]))

    def testPrintFloatFormat(self, message_module):
        message = message_module.NestedTestAllTypes()
        message.payload.optional_float = 1.25
        message.payload.optional_double = -3.456789012345678e-06
        message.payload.repeated_float.append(-5642)
        message.payload.repeated_double.append(7.89e-05)
        formatted_fields = ['optional_float: 1.25',
         'optional_double: -3.45678901234568e-6',
         'repeated_float: -5642', 'repeated_double: 7.89e-5']
        text_message = text_format.MessageToString(message, float_format='.15g')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_message), ('payload {{\n  {0}\n  {1}\n  {2}\n  {3}\n}}\n'.format)(*formatted_fields))
        text_message = text_format.MessageToString(message, as_one_line=True,
          float_format='.15g')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_message), ('payload {{ {0} {1} {2} {3} }}'.format)(*formatted_fields))
        message.payload.optional_float = 1.2000000476837158
        formatted_fields = ['optional_float: 1.2',
         'optional_double: -3.45678901234568e-6',
         'repeated_float: -5642', 'repeated_double: 7.89e-5']
        text_message = text_format.MessageToString(message, float_format='.7g', double_format='.15g')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_message), ('payload {{\n  {0}\n  {1}\n  {2}\n  {3}\n}}\n'.format)(*formatted_fields))
        formatted_fields = [
         'optional_float: 1.2',
         'optional_double: -3.456789e-6',
         'repeated_float: -5642', 'repeated_double: 7.89e-5']
        text_message = text_format.MessageToString(message, float_format='.7g')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_message), ('payload {{\n  {0}\n  {1}\n  {2}\n  {3}\n}}\n'.format)(*formatted_fields))
        message.payload.optional_float = 1.2345678912
        message.payload.optional_double = 1.2345678912
        formatted_fields = ['optional_float: 1.2345679',
         'optional_double: 1.2345678912',
         'repeated_float: -5642', 'repeated_double: 7.89e-5']
        text_message = text_format.MessageToString(message)
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_message), ('payload {{\n  {0}\n  {1}\n  {2}\n  {3}\n}}\n'.format)(*formatted_fields))

    def testMessageToString(self, message_module):
        message = message_module.ForeignMessage()
        message.c = 123
        self.assertEqual('c: 123\n', str(message))

    def testMessageToStringUnicode(self, message_module):
        golden_unicode = 'Á short desçription and a 🍌.'
        golden_bytes = golden_unicode.encode('utf-8')
        message = message_module.TestAllTypes()
        message.optional_string = golden_unicode
        message.optional_bytes = golden_bytes
        text = text_format.MessageToString(message, as_utf8=True)
        golden_message = textwrap.dedent('optional_string: "Á short desçription and a 🍌."\noptional_bytes: "\\303\\201 short des\\303\\247ription and a \\360\\237\\215\\214."\n')
        self.CompareToGoldenText(text, golden_message)

    def testMessageToStringASCII(self, message_module):
        golden_unicode = 'Á short desçription and a 🍌.'
        golden_bytes = golden_unicode.encode('utf-8')
        message = message_module.TestAllTypes()
        message.optional_string = golden_unicode
        message.optional_bytes = golden_bytes
        text = text_format.MessageToString(message, as_utf8=False)
        golden_message = 'optional_string: "\\303\\201 short des\\303\\247ription and a \\360\\237\\215\\214."\noptional_bytes: "\\303\\201 short des\\303\\247ription and a \\360\\237\\215\\214."\n'
        self.CompareToGoldenText(text, golden_message)

    def testPrintField(self, message_module):
        message = message_module.TestAllTypes()
        field = message.DESCRIPTOR.fields_by_name['optional_float']
        value = message.optional_float
        out = text_format.TextWriter(False)
        text_format.PrintField(field, value, out)
        self.assertEqual('optional_float: 0.0\n', out.getvalue())
        out.close()
        out = text_format.TextWriter(False)
        printer = text_format._Printer(out)
        printer.PrintField(field, value)
        self.assertEqual('optional_float: 0.0\n', out.getvalue())
        out.close()

    def testPrintFieldValue(self, message_module):
        message = message_module.TestAllTypes()
        field = message.DESCRIPTOR.fields_by_name['optional_float']
        value = message.optional_float
        out = text_format.TextWriter(False)
        text_format.PrintFieldValue(field, value, out)
        self.assertEqual('0.0', out.getvalue())
        out.close()
        out = text_format.TextWriter(False)
        printer = text_format._Printer(out)
        printer.PrintFieldValue(field, value)
        self.assertEqual('0.0', out.getvalue())
        out.close()

    def testCustomOptions(self, message_module):
        message_descriptor = unittest_custom_options_pb2.TestMessageWithCustomOptions.DESCRIPTOR
        message_proto = descriptor_pb2.DescriptorProto()
        message_descriptor.CopyToProto(message_proto)
        expected_text = 'name: "TestMessageWithCustomOptions"\nfield {\n  name: "field1"\n  number: 1\n  label: LABEL_OPTIONAL\n  type: TYPE_STRING\n  options {\n    ctype: CORD\n    [protobuf_unittest.field_opt1]: 8765432109\n  }\n}\nfield {\n  name: "oneof_field"\n  number: 2\n  label: LABEL_OPTIONAL\n  type: TYPE_INT32\n  oneof_index: 0\n}\nenum_type {\n  name: "AnEnum"\n  value {\n    name: "ANENUM_VAL1"\n    number: 1\n  }\n  value {\n    name: "ANENUM_VAL2"\n    number: 2\n    options {\n      [protobuf_unittest.enum_value_opt1]: 123\n    }\n  }\n  options {\n    [protobuf_unittest.enum_opt1]: -789\n  }\n}\noptions {\n  message_set_wire_format: false\n  [protobuf_unittest.message_opt1]: -56\n}\noneof_decl {\n  name: "AnOneof"\n  options {\n    [protobuf_unittest.oneof_opt1]: -99\n  }\n}\n'
        self.assertEqual(expected_text, text_format.MessageToString(message_proto))
        parsed_proto = descriptor_pb2.DescriptorProto()
        text_format.Parse(expected_text, parsed_proto)
        self.assertEqual(message_proto, parsed_proto)

    def testPrintUnknownFieldsEmbeddedMessageInBytes(self, message_module):
        inner_msg = message_module.TestAllTypes()
        inner_msg.optional_int32 = 101
        inner_msg.optional_double = 102.0
        inner_msg.optional_string = 'hello'
        inner_msg.optional_bytes = b'103'
        inner_msg.optional_nested_message.bb = 105
        inner_data = inner_msg.SerializeToString()
        outer_message = message_module.TestAllTypes()
        outer_message.optional_int32 = 101
        outer_message.optional_bytes = inner_data
        all_data = outer_message.SerializeToString()
        empty_message = message_module.TestEmptyMessage()
        empty_message.ParseFromString(all_data)
        self.assertEqual('  1: 101\n  15 {\n    1: 101\n    12: 4636878028842991616\n    14: "hello"\n    15: "103"\n    18 {\n      1: 105\n    }\n  }\n', text_format.MessageToString(empty_message, indent=2,
          print_unknown_fields=True))
        self.assertEqual('1: 101 15 { 1: 101 12: 4636878028842991616 14: "hello" 15: "103" 18 { 1: 105 } }', text_format.MessageToString(empty_message, print_unknown_fields=True,
          as_one_line=True))


@_parameterized.parameters(unittest_pb2, unittest_proto3_arena_pb2)
class TextFormatMessageToTextBytesTests(TextFormatBase):

    def testMessageToBytes(self, message_module):
        message = message_module.ForeignMessage()
        message.c = 123
        self.assertEqual(b'c: 123\n', text_format.MessageToBytes(message))

    def testRawUtf8RoundTrip(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_string.append('ü\tꜟ')
        utf8_text = text_format.MessageToBytes(message, as_utf8=True)
        golden_bytes = b'repeated_string: "\xc3\xbc\\t\xea\x9c\x9f"\n'
        self.CompareToGoldenText(utf8_text, golden_bytes)
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(utf8_text, parsed_message)
        self.assertEqual(message, parsed_message, '\n%s != %s  (%s != %s)' % (
         message, parsed_message, message.repeated_string[0],
         parsed_message.repeated_string[0]))

    def testEscapedUtf8ASCIIRoundTrip(self, message_module):
        message = message_module.TestAllTypes()
        message.repeated_string.append('ü\tꜟ')
        ascii_text = text_format.MessageToBytes(message)
        golden_bytes = b'repeated_string: "\\303\\274\\t\\352\\234\\237"\n'
        self.CompareToGoldenText(ascii_text, golden_bytes)
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(ascii_text, parsed_message)
        self.assertEqual(message, parsed_message, '\n%s != %s  (%s != %s)' % (
         message, parsed_message, message.repeated_string[0],
         parsed_message.repeated_string[0]))


@_parameterized.parameters(unittest_pb2, unittest_proto3_arena_pb2)
class TextFormatParserTests(TextFormatBase):

    def testParseAllFields(self, message_module):
        message = message_module.TestAllTypes()
        test_util.SetAllFields(message)
        ascii_text = text_format.MessageToString(message)
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(ascii_text, parsed_message)
        self.assertEqual(message, parsed_message)
        if message_module is unittest_pb2:
            test_util.ExpectAllFieldsSet(self, message)

    def testParseAndMergeUtf8(self, message_module):
        message = message_module.TestAllTypes()
        test_util.SetAllFields(message)
        ascii_text = text_format.MessageToString(message)
        ascii_text = ascii_text.encode('utf-8')
        parsed_message = message_module.TestAllTypes()
        text_format.Parse(ascii_text, parsed_message)
        self.assertEqual(message, parsed_message)
        if message_module is unittest_pb2:
            test_util.ExpectAllFieldsSet(self, message)
        parsed_message.Clear()
        text_format.Merge(ascii_text, parsed_message)
        self.assertEqual(message, parsed_message)
        if message_module is unittest_pb2:
            test_util.ExpectAllFieldsSet(self, message)
        msg2 = message_module.TestAllTypes()
        text = 'optional_string: "café"'
        text_format.Merge(text, msg2)
        self.assertEqual(msg2.optional_string, 'café')
        msg2.Clear()
        self.assertEqual(msg2.optional_string, '')
        text_format.Parse(text, msg2)
        self.assertEqual(msg2.optional_string, 'café')

    def testParseDoubleToFloat(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_float: 3.4028235e+39\nrepeated_float: 1.4028235e-39\n'
        text_format.Parse(text, message)
        self.assertEqual(message.repeated_float[0], float('inf'))
        self.assertAlmostEqual(message.repeated_float[1], 1.4028235e-39)

    def testParseExotic(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_int64: -9223372036854775808\nrepeated_uint64: 18446744073709551615\nrepeated_double: 123.456\nrepeated_double: 1.23e+22\nrepeated_double: 1.23e-18\nrepeated_string: \n"\\000\\001\\007\\010\\014\\n\\r\\t\\013\\\\\\\'\\""\nrepeated_string: "foo" \'corge\' "grault"\nrepeated_string: "\\303\\274\\352\\234\\237"\nrepeated_string: "\\xc3\\xbc"\nrepeated_string: "Ã¼"\n'
        text_format.Parse(text, message)
        self.assertEqual(-9223372036854775808, message.repeated_int64[0])
        self.assertEqual(18446744073709551615, message.repeated_uint64[0])
        self.assertEqual(123.456, message.repeated_double[0])
        self.assertEqual(1.23e+22, message.repeated_double[1])
        self.assertEqual(1.23e-18, message.repeated_double[2])
        self.assertEqual('\x00\x01\x07\x08\x0c\n\r\t\x0b\\\'"', message.repeated_string[0])
        self.assertEqual('foocorgegrault', message.repeated_string[1])
        self.assertEqual('üꜟ', message.repeated_string[2])
        self.assertEqual('ü', message.repeated_string[3])

    def testParseTrailingCommas(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_int64: 100;\nrepeated_int64: 200;\nrepeated_int64: 300,\nrepeated_string: "one",\nrepeated_string: "two";\n'
        text_format.Parse(text, message)
        self.assertEqual(100, message.repeated_int64[0])
        self.assertEqual(200, message.repeated_int64[1])
        self.assertEqual(300, message.repeated_int64[2])
        self.assertEqual('one', message.repeated_string[0])
        self.assertEqual('two', message.repeated_string[1])

    def testParseRepeatedScalarShortFormat(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_int64: [100, 200];\nrepeated_int64: []\nrepeated_int64: 300,\nrepeated_string: ["one", "two"];\n'
        text_format.Parse(text, message)
        self.assertEqual(100, message.repeated_int64[0])
        self.assertEqual(200, message.repeated_int64[1])
        self.assertEqual(300, message.repeated_int64[2])
        self.assertEqual('one', message.repeated_string[0])
        self.assertEqual('two', message.repeated_string[1])

    def testParseRepeatedMessageShortFormat(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_nested_message: [{bb: 100}, {bb: 200}],\nrepeated_nested_message: {bb: 300}\nrepeated_nested_message [{bb: 400}];\n'
        text_format.Parse(text, message)
        self.assertEqual(100, message.repeated_nested_message[0].bb)
        self.assertEqual(200, message.repeated_nested_message[1].bb)
        self.assertEqual(300, message.repeated_nested_message[2].bb)
        self.assertEqual(400, message.repeated_nested_message[3].bb)

    def testParseEmptyText(self, message_module):
        message = message_module.TestAllTypes()
        text = ''
        text_format.Parse(text, message)
        self.assertEqual(message_module.TestAllTypes(), message)

    def testParseInvalidUtf8(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_string: "\\xc3\\xc3"'
        with self.assertRaises(text_format.ParseError) as (e):
            text_format.Parse(text, message)
        self.assertEqual(e.exception.GetLine(), 1)
        self.assertEqual(e.exception.GetColumn(), 28)

    def testParseSingleWord(self, message_module):
        message = message_module.TestAllTypes()
        text = 'foo'
        six.assertRaisesRegex(self, text_format.ParseError, '1:1 : Message type "\\w+.TestAllTypes" has no field named "foo".', text_format.Parse, text, message)

    def testParseUnknownField(self, message_module):
        message = message_module.TestAllTypes()
        text = 'unknown_field: 8\n'
        six.assertRaisesRegex(self, text_format.ParseError, '1:1 : Message type "\\w+.TestAllTypes" has no field named "unknown_field".', text_format.Parse, text, message)
        text = 'optional_int32: 123\nunknown_field: 8\noptional_nested_message { bb: 45 }'
        text_format.Parse(text, message, allow_unknown_field=True)
        self.assertEqual(message.optional_nested_message.bb, 45)
        self.assertEqual(message.optional_int32, 123)

    def testParseBadEnumValue(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_nested_enum: BARR'
        six.assertRaisesRegex(self, text_format.ParseError, '1:23 : \\\'optional_nested_enum: BARR\\\': Enum type "\\w+.TestAllTypes.NestedEnum" has no value named BARR.', text_format.Parse, text, message)

    def testParseBadIntValue(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_int32: bork'
        six.assertRaisesRegex(self, text_format.ParseError, "1:17 : 'optional_int32: bork': Couldn't parse integer: bork", text_format.Parse, text, message)

    def testParseStringFieldUnescape(self, message_module):
        message = message_module.TestAllTypes()
        text = 'repeated_string: "\\xf\\x62"\n               repeated_string: "\\\\xf\\\\x62"\n               repeated_string: "\\\\\\xf\\\\\\x62"\n               repeated_string: "\\\\\\\\xf\\\\\\\\x62"\n               repeated_string: "\\\\\\\\\\xf\\\\\\\\\\x62"\n               repeated_string: "\\x5cx20"'
        text_format.Parse(text, message)
        SLASH = '\\'
        self.assertEqual('\x0fb', message.repeated_string[0])
        self.assertEqual(SLASH + 'xf' + SLASH + 'x62', message.repeated_string[1])
        self.assertEqual(SLASH + '\x0f' + SLASH + 'b', message.repeated_string[2])
        self.assertEqual(SLASH + SLASH + 'xf' + SLASH + SLASH + 'x62', message.repeated_string[3])
        self.assertEqual(SLASH + SLASH + '\x0f' + SLASH + SLASH + 'b', message.repeated_string[4])
        self.assertEqual(SLASH + 'x20', message.repeated_string[5])

    def testParseOneof(self, message_module):
        m = message_module.TestAllTypes()
        m.oneof_uint32 = 11
        m2 = message_module.TestAllTypes()
        text_format.Parse(text_format.MessageToString(m), m2)
        self.assertEqual('oneof_uint32', m2.WhichOneof('oneof_field'))

    def testParseMultipleOneof(self, message_module):
        m_string = '\n'.join(['oneof_uint32: 11', 'oneof_string: "foo"'])
        m2 = message_module.TestAllTypes()
        with six.assertRaisesRegex(self, text_format.ParseError, ' is specified along with field '):
            text_format.Parse(m_string, m2)

    _UNICODE_SAMPLE = "\n      optional_bytes: 'Á short desçription'\n      optional_string: 'Á short desçription'\n      repeated_bytes: '\\303\\201 short des\\303\\247ription'\n      repeated_bytes: '\\x12\\x34\\x56\\x78\\x90\\xab\\xcd\\xef'\n      repeated_string: '\\xd0\\x9f\\xd1\\x80\\xd0\\xb8\\xd0\\xb2\\xd0\\xb5\\xd1\\x82'\n      "
    _BYTES_SAMPLE = _UNICODE_SAMPLE.encode('utf-8')
    _GOLDEN_UNICODE = 'Á short desçription'
    _GOLDEN_BYTES = _GOLDEN_UNICODE.encode('utf-8')
    _GOLDEN_BYTES_1 = b'\x124Vx\x90\xab\xcd\xef'
    _GOLDEN_STR_0 = 'Привет'

    def testParseUnicode(self, message_module):
        m = message_module.TestAllTypes()
        text_format.Parse(self._UNICODE_SAMPLE, m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)
        self.assertEqual(m.repeated_bytes[1], self._GOLDEN_BYTES_1)
        self.assertEqual(m.repeated_string[0], self._GOLDEN_STR_0)

    def testParseBytes(self, message_module):
        m = message_module.TestAllTypes()
        text_format.Parse(self._BYTES_SAMPLE, m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)
        self.assertEqual(m.repeated_bytes[1], self._GOLDEN_BYTES_1)
        self.assertEqual(m.repeated_string[0], self._GOLDEN_STR_0)

    def testFromBytesFile(self, message_module):
        m = message_module.TestAllTypes()
        f = io.BytesIO(self._BYTES_SAMPLE)
        text_format.ParseLines(f, m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)

    def testFromUnicodeFile(self, message_module):
        m = message_module.TestAllTypes()
        f = io.StringIO(self._UNICODE_SAMPLE)
        text_format.ParseLines(f, m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)

    def testFromBytesLines(self, message_module):
        m = message_module.TestAllTypes()
        text_format.ParseLines(self._BYTES_SAMPLE.split(b'\n'), m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)

    def testFromUnicodeLines(self, message_module):
        m = message_module.TestAllTypes()
        text_format.ParseLines(self._UNICODE_SAMPLE.split('\n'), m)
        self.assertEqual(m.optional_bytes, self._GOLDEN_BYTES)
        self.assertEqual(m.optional_string, self._GOLDEN_UNICODE)
        self.assertEqual(m.repeated_bytes[0], self._GOLDEN_BYTES)

    def testParseDuplicateMessages(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_nested_message { bb: 1 } optional_nested_message { bb: 2 }'
        six.assertRaisesRegex(self, text_format.ParseError, '1:59 : Message type "\\w+.TestAllTypes" should not have multiple "optional_nested_message" fields.', text_format.Parse, text, message)

    def testParseDuplicateScalars(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_int32: 42 optional_int32: 67'
        six.assertRaisesRegex(self, text_format.ParseError, '1:36 : Message type "\\w+.TestAllTypes" should not have multiple "optional_int32" fields.', text_format.Parse, text, message)

    def testParseExistingScalarInMessage(self, message_module):
        message = message_module.TestAllTypes(optional_int32=42)
        text = 'optional_int32: 67'
        six.assertRaisesRegex(self, text_format.ParseError, 'Message type "\\w+.TestAllTypes" should not have multiple "optional_int32" fields.', text_format.Parse, text, message)


@_parameterized.parameters(unittest_pb2, unittest_proto3_arena_pb2)
class TextFormatMergeTests(TextFormatBase):

    def testMergeDuplicateScalarsInText(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_int32: 42 optional_int32: 67'
        r = text_format.Merge(text, message)
        self.assertIs(r, message)
        self.assertEqual(67, message.optional_int32)

    def testMergeDuplicateNestedMessageScalars(self, message_module):
        message = message_module.TestAllTypes()
        text = 'optional_nested_message { bb: 1 } optional_nested_message { bb: 2 }'
        r = text_format.Merge(text, message)
        self.assertTrue(r is message)
        self.assertEqual(2, message.optional_nested_message.bb)

    def testReplaceScalarInMessage(self, message_module):
        message = message_module.TestAllTypes(optional_int32=42)
        text = 'optional_int32: 67'
        r = text_format.Merge(text, message)
        self.assertIs(r, message)
        self.assertEqual(67, message.optional_int32)

    def testReplaceMessageInMessage(self, message_module):
        message = message_module.TestAllTypes(optional_int32=42,
          optional_nested_message=(dict()))
        self.assertTrue(message.HasField('optional_nested_message'))
        text = 'optional_nested_message{ bb: 3 }'
        r = text_format.Merge(text, message)
        self.assertIs(r, message)
        self.assertEqual(3, message.optional_nested_message.bb)

    def testMergeMultipleOneof(self, message_module):
        m_string = '\n'.join(['oneof_uint32: 11', 'oneof_string: "foo"'])
        m2 = message_module.TestAllTypes()
        text_format.Merge(m_string, m2)
        self.assertEqual('oneof_string', m2.WhichOneof('oneof_field'))


class OnlyWorksWithProto2RightNowTests(TextFormatBase):

    def testPrintAllFieldsPointy(self):
        message = unittest_pb2.TestAllTypes()
        test_util.SetAllFields(message)
        self.CompareToGoldenFile(self.RemoveRedundantZeros(text_format.MessageToString(message,
          pointy_brackets=True)), 'text_format_unittest_data_pointy_oneof.txt')

    def testParseGolden(self):
        golden_text = '\n'.join(self.ReadGolden('text_format_unittest_data_oneof_implemented.txt'))
        parsed_message = unittest_pb2.TestAllTypes()
        r = text_format.Parse(golden_text, parsed_message)
        self.assertIs(r, parsed_message)
        message = unittest_pb2.TestAllTypes()
        test_util.SetAllFields(message)
        self.assertEqual(message, parsed_message)

    def testPrintAllFields(self):
        message = unittest_pb2.TestAllTypes()
        test_util.SetAllFields(message)
        self.CompareToGoldenFile(self.RemoveRedundantZeros(text_format.MessageToString(message)), 'text_format_unittest_data_oneof_implemented.txt')

    def testPrintUnknownFields(self):
        message = unittest_pb2.TestAllTypes()
        message.optional_int32 = 101
        message.optional_double = 102.0
        message.optional_string = 'hello'
        message.optional_bytes = b'103'
        message.optionalgroup.a = 104
        message.optional_nested_message.bb = 105
        all_data = message.SerializeToString()
        empty_message = unittest_pb2.TestEmptyMessage()
        empty_message.ParseFromString(all_data)
        self.assertEqual('  1: 101\n  12: 4636878028842991616\n  14: "hello"\n  15: "103"\n  16 {\n    17: 104\n  }\n  18 {\n    1: 105\n  }\n', text_format.MessageToString(empty_message, indent=2,
          print_unknown_fields=True))
        self.assertEqual('1: 101 12: 4636878028842991616 14: "hello" 15: "103" 16 { 17: 104 } 18 { 1: 105 }', text_format.MessageToString(empty_message, print_unknown_fields=True,
          as_one_line=True))

    def testPrintInIndexOrder(self):
        message = unittest_pb2.TestFieldOrderings()
        message.my_string = 'str'
        message.my_int = 101
        message.my_float = 111
        message.optional_nested_message.oo = 0
        message.optional_nested_message.bb = 1
        message.Extensions[unittest_pb2.my_extension_string] = 'ext_str0'
        message.Extensions[unittest_pb2.TestExtensionOrderings2.test_ext_orderings2].my_string = 'ext_str2'
        message.Extensions[unittest_pb2.TestExtensionOrderings1.test_ext_orderings1].my_string = 'ext_str1'
        message.Extensions[unittest_pb2.TestExtensionOrderings2.TestExtensionOrderings3.test_ext_orderings3].my_string = 'ext_str3'
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_format.MessageToString(message, use_index_order=True)), 'my_string: "str"\nmy_int: 101\nmy_float: 111\noptional_nested_message {\n  oo: 0\n  bb: 1\n}\n[protobuf_unittest.TestExtensionOrderings2.test_ext_orderings2] {\n  my_string: "ext_str2"\n}\n[protobuf_unittest.TestExtensionOrderings1.test_ext_orderings1] {\n  my_string: "ext_str1"\n}\n[protobuf_unittest.TestExtensionOrderings2.TestExtensionOrderings3.test_ext_orderings3] {\n  my_string: "ext_str3"\n}\n[protobuf_unittest.my_extension_string]: "ext_str0"\n')
        self.CompareToGoldenText(self.RemoveRedundantZeros(text_format.MessageToString(message)), 'my_int: 101\nmy_string: "str"\n[protobuf_unittest.TestExtensionOrderings2.test_ext_orderings2] {\n  my_string: "ext_str2"\n}\n[protobuf_unittest.TestExtensionOrderings1.test_ext_orderings1] {\n  my_string: "ext_str1"\n}\n[protobuf_unittest.TestExtensionOrderings2.TestExtensionOrderings3.test_ext_orderings3] {\n  my_string: "ext_str3"\n}\n[protobuf_unittest.my_extension_string]: "ext_str0"\nmy_float: 111\noptional_nested_message {\n  bb: 1\n  oo: 0\n}\n')

    def testMergeLinesGolden(self):
        opened = self.ReadGolden('text_format_unittest_data_oneof_implemented.txt')
        parsed_message = unittest_pb2.TestAllTypes()
        r = text_format.MergeLines(opened, parsed_message)
        self.assertIs(r, parsed_message)
        message = unittest_pb2.TestAllTypes()
        test_util.SetAllFields(message)
        self.assertEqual(message, parsed_message)

    def testParseLinesGolden(self):
        opened = self.ReadGolden('text_format_unittest_data_oneof_implemented.txt')
        parsed_message = unittest_pb2.TestAllTypes()
        r = text_format.ParseLines(opened, parsed_message)
        self.assertIs(r, parsed_message)
        message = unittest_pb2.TestAllTypes()
        test_util.SetAllFields(message)
        self.assertEqual(message, parsed_message)

    def testPrintMap(self):
        message = map_unittest_pb2.TestMap()
        message.map_int32_int32[-123] = -456
        message.map_int64_int64[-8589934592] = -17179869184
        message.map_uint32_uint32[123] = 456
        message.map_uint64_uint64[8589934592] = 17179869184
        message.map_string_string['abc'] = '123'
        message.map_int32_foreign_message[111].c = 5
        self.CompareToGoldenText(text_format.MessageToString(message), 'map_int32_int32 {\n  key: -123\n  value: -456\n}\nmap_int64_int64 {\n  key: -8589934592\n  value: -17179869184\n}\nmap_uint32_uint32 {\n  key: 123\n  value: 456\n}\nmap_uint64_uint64 {\n  key: 8589934592\n  value: 17179869184\n}\nmap_string_string {\n  key: "abc"\n  value: "123"\n}\nmap_int32_foreign_message {\n  key: 111\n  value {\n    c: 5\n  }\n}\n')

    def testPrintMapUsingCppImplementation(self):
        message = map_unittest_pb2.TestMap()
        inner_msg = message.map_int32_foreign_message[111]
        inner_msg.c = 1
        self.assertEqual(str(message), 'map_int32_foreign_message {\n  key: 111\n  value {\n    c: 1\n  }\n}\n')
        inner_msg.c = 2
        self.assertEqual(str(message), 'map_int32_foreign_message {\n  key: 111\n  value {\n    c: 2\n  }\n}\n')

    def testMapOrderEnforcement(self):
        message = map_unittest_pb2.TestMap()
        for letter in string.ascii_uppercase[13:26]:
            message.map_string_string[letter] = 'dummy'

        for letter in reversed(string.ascii_uppercase[0:13]):
            message.map_string_string[letter] = 'dummy'

        golden = ''.join('map_string_string {\n  key: "%c"\n  value: "dummy"\n}\n' % (letter,) for letter in string.ascii_uppercase)
        self.CompareToGoldenText(text_format.MessageToString(message), golden)


class Proto2Tests(TextFormatBase):

    def testPrintMessageSet(self):
        message = unittest_mset_pb2.TestMessageSetContainer()
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        message.message_set.Extensions[ext1].i = 23
        message.message_set.Extensions[ext2].str = 'foo'
        self.CompareToGoldenText(text_format.MessageToString(message), 'message_set {\n  [protobuf_unittest.TestMessageSetExtension1] {\n    i: 23\n  }\n  [protobuf_unittest.TestMessageSetExtension2] {\n    str: "foo"\n  }\n}\n')
        message = message_set_extensions_pb2.TestMessageSet()
        ext = message_set_extensions_pb2.message_set_extension3
        message.Extensions[ext].text = 'bar'
        self.CompareToGoldenText(text_format.MessageToString(message), '[google.protobuf.internal.TestMessageSetExtension3] {\n  text: "bar"\n}\n')

    def testPrintMessageSetByFieldNumber(self):
        out = text_format.TextWriter(False)
        message = unittest_mset_pb2.TestMessageSetContainer()
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        message.message_set.Extensions[ext1].i = 23
        message.message_set.Extensions[ext2].str = 'foo'
        text_format.PrintMessage(message, out, use_field_number=True)
        self.CompareToGoldenText(out.getvalue(), '1 {\n  1545008 {\n    15: 23\n  }\n  1547769 {\n    25: "foo"\n  }\n}\n')
        out.close()

    def testPrintMessageSetAsOneLine(self):
        message = unittest_mset_pb2.TestMessageSetContainer()
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        message.message_set.Extensions[ext1].i = 23
        message.message_set.Extensions[ext2].str = 'foo'
        self.CompareToGoldenText(text_format.MessageToString(message, as_one_line=True), 'message_set { [protobuf_unittest.TestMessageSetExtension1] { i: 23 } [protobuf_unittest.TestMessageSetExtension2] { str: "foo" } }')

    def testParseMessageSet(self):
        message = unittest_pb2.TestAllTypes()
        text = 'repeated_uint64: 1\nrepeated_uint64: 2\n'
        text_format.Parse(text, message)
        self.assertEqual(1, message.repeated_uint64[0])
        self.assertEqual(2, message.repeated_uint64[1])
        message = unittest_mset_pb2.TestMessageSetContainer()
        text = 'message_set {\n  [protobuf_unittest.TestMessageSetExtension1] {\n    i: 23\n  }\n  [protobuf_unittest.TestMessageSetExtension2] {\n    str: "foo"\n  }\n}\n'
        text_format.Parse(text, message)
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        self.assertEqual(23, message.message_set.Extensions[ext1].i)
        self.assertEqual('foo', message.message_set.Extensions[ext2].str)

    def testExtensionInsideAnyMessage(self):
        message = test_extend_any.TestAny()
        text = 'value {\n  [type.googleapis.com/google.protobuf.internal.TestAny] {\n    [google.protobuf.internal.TestAnyExtension1.extension1] {\n      i: 10\n    }\n  }\n}\n'
        text_format.Merge(text, message, descriptor_pool=(descriptor_pool.Default()))
        self.CompareToGoldenText(text_format.MessageToString(message,
          descriptor_pool=(descriptor_pool.Default())), text)

    def testParseMessageByFieldNumber(self):
        message = unittest_pb2.TestAllTypes()
        text = '34: 1\nrepeated_uint64: 2\n'
        text_format.Parse(text, message, allow_field_number=True)
        self.assertEqual(1, message.repeated_uint64[0])
        self.assertEqual(2, message.repeated_uint64[1])
        message = unittest_mset_pb2.TestMessageSetContainer()
        text = '1 {\n  1545008 {\n    15: 23\n  }\n  1547769 {\n    25: "foo"\n  }\n}\n'
        text_format.Parse(text, message, allow_field_number=True)
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        self.assertEqual(23, message.message_set.Extensions[ext1].i)
        self.assertEqual('foo', message.message_set.Extensions[ext2].str)
        message = unittest_pb2.TestAllTypes()
        text = '34:1\n'
        six.assertRaisesRegex(self, text_format.ParseError, '1:1 : Message type "\\w+.TestAllTypes" has no field named "34".', text_format.Parse, text, message)
        text = '1234:1\n'
        six.assertRaisesRegex(self,
          (text_format.ParseError),
          '1:1 : Message type "\\w+.TestAllTypes" has no field named "1234".',
          (text_format.Parse),
          text,
          message,
          allow_field_number=True)

    def testPrintAllExtensions(self):
        message = unittest_pb2.TestAllExtensions()
        test_util.SetAllExtensions(message)
        self.CompareToGoldenFile(self.RemoveRedundantZeros(text_format.MessageToString(message)), 'text_format_unittest_extensions_data.txt')

    def testPrintAllExtensionsPointy(self):
        message = unittest_pb2.TestAllExtensions()
        test_util.SetAllExtensions(message)
        self.CompareToGoldenFile(self.RemoveRedundantZeros(text_format.MessageToString(message,
          pointy_brackets=True)), 'text_format_unittest_extensions_data_pointy.txt')

    def testParseGoldenExtensions(self):
        golden_text = '\n'.join(self.ReadGolden('text_format_unittest_extensions_data.txt'))
        parsed_message = unittest_pb2.TestAllExtensions()
        text_format.Parse(golden_text, parsed_message)
        message = unittest_pb2.TestAllExtensions()
        test_util.SetAllExtensions(message)
        self.assertEqual(message, parsed_message)

    def testParseAllExtensions(self):
        message = unittest_pb2.TestAllExtensions()
        test_util.SetAllExtensions(message)
        ascii_text = text_format.MessageToString(message)
        parsed_message = unittest_pb2.TestAllExtensions()
        text_format.Parse(ascii_text, parsed_message)
        self.assertEqual(message, parsed_message)

    def testParseAllowedUnknownExtension(self):
        message = unittest_mset_pb2.TestMessageSetContainer()
        text = 'message_set {\n  [unknown_extension] {\n    i: 23\n    bin: "à"    [nested_unknown_ext]: {\n      i: 23\n      x: x\n      test: "test_string"\n      floaty_float: -0.315\n      num: -inf\n      multiline_str: "abc"\n          "def"\n          "xyz."\n      [nested_unknown_ext.ext]: <\n        i: 23\n        i: 24\n        pointfloat: .3\n        test: "test_string"\n        floaty_float: -0.315\n        num: -inf\n        long_string: "test" "test2" \n      >\n    }\n  }\n  [unknown_extension]: 5\n  [unknown_extension_with_number_field] {\n    1: "some_field"\n    2: -0.451\n  }\n}\n'
        text_format.Parse(text, message, allow_unknown_extension=True)
        golden = 'message_set {\n}\n'
        self.CompareToGoldenText(text_format.MessageToString(message), golden)
        message = unittest_mset_pb2.TestMessageSetContainer()
        malformed = 'message_set {\n  [unknown_extension] {\n    i:\n  }\n}\n'
        six.assertRaisesRegex(self, (text_format.ParseError),
          'Invalid field value: }',
          (text_format.Parse),
          malformed,
          message,
          allow_unknown_extension=True)
        message = unittest_mset_pb2.TestMessageSetContainer()
        malformed = 'message_set {\n  [unknown_extension] {\n    str: "malformed string\n  }\n}\n'
        six.assertRaisesRegex(self, (text_format.ParseError),
          'Invalid field value: "',
          (text_format.Parse),
          malformed,
          message,
          allow_unknown_extension=True)
        message = unittest_mset_pb2.TestMessageSetContainer()
        malformed = 'message_set {\n  [unknown_extension] {\n    str: "malformed\n multiline\n string\n  }\n}\n'
        six.assertRaisesRegex(self, (text_format.ParseError),
          'Invalid field value: "',
          (text_format.Parse),
          malformed,
          message,
          allow_unknown_extension=True)
        message = unittest_mset_pb2.TestMessageSetContainer()
        malformed = 'message_set {\n  [malformed_extension] <\n    i: -5\n  \n}\n'
        six.assertRaisesRegex(self, (text_format.ParseError),
          '5:1 : \'}\': Expected ">".',
          (text_format.Parse),
          malformed,
          message,
          allow_unknown_extension=True)
        message = unittest_mset_pb2.TestMessageSetContainer()
        malformed = 'message_set {\n  unknown_field: true\n}\n'
        six.assertRaisesRegex(self, (text_format.ParseError),
          '2:3 : Message type "proto2_wireformat_unittest.TestMessageSet" has no field named "unknown_field".',
          (text_format.Parse),
          malformed,
          message,
          allow_unknown_extension=True)
        message = unittest_mset_pb2.TestMessageSetContainer()
        text = 'message_set {\n  [protobuf_unittest.TestMessageSetExtension1] {\n    i: 23\n  }\n  [protobuf_unittest.TestMessageSetExtension2] {\n    str: "foo"\n  }\n}\n'
        text_format.Parse(text, message, allow_unknown_extension=True)
        ext1 = unittest_mset_pb2.TestMessageSetExtension1.message_set_extension
        ext2 = unittest_mset_pb2.TestMessageSetExtension2.message_set_extension
        self.assertEqual(23, message.message_set.Extensions[ext1].i)
        self.assertEqual('foo', message.message_set.Extensions[ext2].str)

    def testParseBadIdentifier(self):
        message = unittest_pb2.TestAllTypes()
        text = 'optional_nested_message { "bb": 1 }'
        with self.assertRaises(text_format.ParseError) as (e):
            text_format.Parse(text, message)
        self.assertEqual(str(e.exception), '1:27 : \'optional_nested_message { "bb": 1 }\': Expected identifier or number, got "bb".')

    def testParseBadExtension(self):
        message = unittest_pb2.TestAllExtensions()
        text = '[unknown_extension]: 8\n'
        six.assertRaisesRegex(self, text_format.ParseError, '1:2 : Extension "unknown_extension" not registered.', text_format.Parse, text, message)
        message = unittest_pb2.TestAllTypes()
        six.assertRaisesRegex(self, text_format.ParseError, '1:2 : Message type "protobuf_unittest.TestAllTypes" does not have extensions.', text_format.Parse, text, message)

    def testParseNumericUnknownEnum(self):
        message = unittest_pb2.TestAllTypes()
        text = 'optional_nested_enum: 100'
        six.assertRaisesRegex(self, text_format.ParseError, '1:23 : \\\'optional_nested_enum: 100\\\': Enum type "\\w+.TestAllTypes.NestedEnum" has no value with number 100.', text_format.Parse, text, message)

    def testMergeDuplicateExtensionScalars(self):
        message = unittest_pb2.TestAllExtensions()
        text = '[protobuf_unittest.optional_int32_extension]: 42 [protobuf_unittest.optional_int32_extension]: 67'
        text_format.Merge(text, message)
        self.assertEqual(67, message.Extensions[unittest_pb2.optional_int32_extension])

    def testParseDuplicateExtensionScalars(self):
        message = unittest_pb2.TestAllExtensions()
        text = '[protobuf_unittest.optional_int32_extension]: 42 [protobuf_unittest.optional_int32_extension]: 67'
        six.assertRaisesRegex(self, text_format.ParseError, '1:96 : Message type "protobuf_unittest.TestAllExtensions" should not have multiple "protobuf_unittest.optional_int32_extension" extensions.', text_format.Parse, text, message)

    def testParseDuplicateExtensionMessages(self):
        message = unittest_pb2.TestAllExtensions()
        text = '[protobuf_unittest.optional_nested_message_extension]: {} [protobuf_unittest.optional_nested_message_extension]: {}'
        six.assertRaisesRegex(self, text_format.ParseError, '1:114 : Message type "protobuf_unittest.TestAllExtensions" should not have multiple "protobuf_unittest.optional_nested_message_extension" extensions.', text_format.Parse, text, message)

    def testParseGroupNotClosed(self):
        message = unittest_pb2.TestAllTypes()
        text = 'RepeatedGroup: <'
        six.assertRaisesRegex(self, text_format.ParseError, '1:16 : Expected ">".', text_format.Parse, text, message)
        text = 'RepeatedGroup: {'
        six.assertRaisesRegex(self, text_format.ParseError, '1:16 : Expected "}".', text_format.Parse, text, message)

    def testParseEmptyGroup(self):
        message = unittest_pb2.TestAllTypes()
        text = 'OptionalGroup: {}'
        text_format.Parse(text, message)
        self.assertTrue(message.HasField('optionalgroup'))
        message.Clear()
        message = unittest_pb2.TestAllTypes()
        text = 'OptionalGroup: <>'
        text_format.Parse(text, message)
        self.assertTrue(message.HasField('optionalgroup'))

    def testParseMap(self):
        text = 'map_int32_int32 {\n  key: -123\n  value: -456\n}\nmap_int64_int64 {\n  key: -8589934592\n  value: -17179869184\n}\nmap_uint32_uint32 {\n  key: 123\n  value: 456\n}\nmap_uint64_uint64 {\n  key: 8589934592\n  value: 17179869184\n}\nmap_string_string {\n  key: "abc"\n  value: "123"\n}\nmap_int32_foreign_message {\n  key: 111\n  value {\n    c: 5\n  }\n}\n'
        message = map_unittest_pb2.TestMap()
        text_format.Parse(text, message)
        self.assertEqual(-456, message.map_int32_int32[(-123)])
        self.assertEqual(-17179869184, message.map_int64_int64[(-8589934592)])
        self.assertEqual(456, message.map_uint32_uint32[123])
        self.assertEqual(17179869184, message.map_uint64_uint64[8589934592])
        self.assertEqual('123', message.map_string_string['abc'])
        self.assertEqual(5, message.map_int32_foreign_message[111].c)


class Proto3Tests(unittest.TestCase):

    def testPrintMessageExpandAny(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        self.assertEqual(text_format.MessageToString(message, descriptor_pool=(descriptor_pool.Default())), 'any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string"\n  }\n}\n')

    def testTopAnyMessage(self):
        packed_msg = unittest_pb2.OneString()
        msg = any_pb2.Any()
        msg.Pack(packed_msg)
        text = text_format.MessageToString(msg)
        other_msg = text_format.Parse(text, any_pb2.Any())
        self.assertEqual(msg, other_msg)

    def testPrintMessageExpandAnyRepeated(self):
        packed_message = unittest_pb2.OneString()
        message = any_test_pb2.TestAny()
        packed_message.data = 'string0'
        message.repeated_any_value.add().Pack(packed_message)
        packed_message.data = 'string1'
        message.repeated_any_value.add().Pack(packed_message)
        self.assertEqual(text_format.MessageToString(message), 'repeated_any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string0"\n  }\n}\nrepeated_any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string1"\n  }\n}\n')

    def testPrintMessageExpandAnyDescriptorPoolMissingType(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        empty_pool = descriptor_pool.DescriptorPool()
        self.assertEqual(text_format.MessageToString(message, descriptor_pool=empty_pool), 'any_value {\n  type_url: "type.googleapis.com/protobuf_unittest.OneString"\n  value: "\\n\\006string"\n}\n')

    def testPrintMessageExpandAnyPointyBrackets(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        self.assertEqual(text_format.MessageToString(message, pointy_brackets=True), 'any_value <\n  [type.googleapis.com/protobuf_unittest.OneString] <\n    data: "string"\n  >\n>\n')

    def testPrintMessageExpandAnyAsOneLine(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        self.assertEqual(text_format.MessageToString(message, as_one_line=True), 'any_value { [type.googleapis.com/protobuf_unittest.OneString] { data: "string" } }')

    def testPrintMessageExpandAnyAsOneLinePointyBrackets(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        self.assertEqual(text_format.MessageToString(message, as_one_line=True,
          pointy_brackets=True,
          descriptor_pool=(descriptor_pool.Default())), 'any_value < [type.googleapis.com/protobuf_unittest.OneString] < data: "string" > >')

    def testPrintAndParseMessageInvalidAny(self):
        packed_message = unittest_pb2.OneString()
        packed_message.data = 'string'
        message = any_test_pb2.TestAny()
        message.any_value.Pack(packed_message)
        message.any_value.type_url = message.any_value.TypeName()
        text = text_format.MessageToString(message)
        self.assertEqual(text, 'any_value {\n  type_url: "protobuf_unittest.OneString"\n  value: "\\n\\006string"\n}\n')
        parsed_message = any_test_pb2.TestAny()
        text_format.Parse(text, parsed_message)
        self.assertEqual(message, parsed_message)

    def testUnknownEnums(self):
        message = unittest_proto3_arena_pb2.TestAllTypes()
        message2 = unittest_proto3_arena_pb2.TestAllTypes()
        message.optional_nested_enum = 999
        text_string = text_format.MessageToString(message)
        text_format.Parse(text_string, message2)
        self.assertEqual(999, message2.optional_nested_enum)

    def testMergeExpandedAny(self):
        message = any_test_pb2.TestAny()
        text = 'any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string"\n  }\n}\n'
        text_format.Merge(text, message)
        packed_message = unittest_pb2.OneString()
        message.any_value.Unpack(packed_message)
        self.assertEqual('string', packed_message.data)
        message.Clear()
        text_format.Parse(text, message)
        packed_message = unittest_pb2.OneString()
        message.any_value.Unpack(packed_message)
        self.assertEqual('string', packed_message.data)

    def testMergeExpandedAnyRepeated(self):
        message = any_test_pb2.TestAny()
        text = 'repeated_any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string0"\n  }\n}\nrepeated_any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string1"\n  }\n}\n'
        text_format.Merge(text, message)
        packed_message = unittest_pb2.OneString()
        message.repeated_any_value[0].Unpack(packed_message)
        self.assertEqual('string0', packed_message.data)
        message.repeated_any_value[1].Unpack(packed_message)
        self.assertEqual('string1', packed_message.data)

    def testMergeExpandedAnyPointyBrackets(self):
        message = any_test_pb2.TestAny()
        text = 'any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] <\n    data: "string"\n  >\n}\n'
        text_format.Merge(text, message)
        packed_message = unittest_pb2.OneString()
        message.any_value.Unpack(packed_message)
        self.assertEqual('string', packed_message.data)

    def testMergeAlternativeUrl(self):
        message = any_test_pb2.TestAny()
        text = 'any_value {\n  [type.otherapi.com/protobuf_unittest.OneString] {\n    data: "string"\n  }\n}\n'
        text_format.Merge(text, message)
        packed_message = unittest_pb2.OneString()
        self.assertEqual('type.otherapi.com/protobuf_unittest.OneString', message.any_value.type_url)

    def testMergeExpandedAnyDescriptorPoolMissingType(self):
        message = any_test_pb2.TestAny()
        text = 'any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string"\n  }\n}\n'
        with self.assertRaises(text_format.ParseError) as (e):
            empty_pool = descriptor_pool.DescriptorPool()
            text_format.Merge(text, message, descriptor_pool=empty_pool)
        self.assertEqual(str(e.exception), 'Type protobuf_unittest.OneString not found in descriptor pool')

    def testMergeUnexpandedAny(self):
        text = 'any_value {\n  type_url: "type.googleapis.com/protobuf_unittest.OneString"\n  value: "\\n\\006string"\n}\n'
        message = any_test_pb2.TestAny()
        text_format.Merge(text, message)
        packed_message = unittest_pb2.OneString()
        message.any_value.Unpack(packed_message)
        self.assertEqual('string', packed_message.data)

    def testMergeMissingAnyEndToken(self):
        message = any_test_pb2.TestAny()
        text = 'any_value {\n  [type.googleapis.com/protobuf_unittest.OneString] {\n    data: "string"\n'
        with self.assertRaises(text_format.ParseError) as (e):
            text_format.Merge(text, message)
        self.assertEqual(str(e.exception), '3:11 : Expected "}".')


class TokenizerTest(unittest.TestCase):

    def testSimpleTokenCases(self):
        text = 'identifier1:"string1"\n     \n\nidentifier2 : \n \n123  \n  identifier3 :\'string\'\nidentifiER_4 : 1.1e+2 ID5:-0.23 ID6:\'aaaa\\\'bbbb\'\nID7 : "aa\\"bb"\n\n\n\n ID8: {A:inf B:-inf C:true D:false}\nID9: 22 ID10: -111111111111111111 ID11: -22\nID12: 2222222222222222222 ID13: 1.23456f ID14: 1.2e+2f false_bool:  0 true_BOOL:t \n true_bool1:  1 false_BOOL1:f False_bool: False True_bool: True X:iNf Y:-inF Z:nAN'
        tokenizer = text_format.Tokenizer(text.splitlines())
        methods = [(tokenizer.ConsumeIdentifier, 'identifier1'), ':',
         (
          tokenizer.ConsumeString, 'string1'),
         (
          tokenizer.ConsumeIdentifier, 'identifier2'), ':',
         (
          tokenizer.ConsumeInteger, 123),
         (
          tokenizer.ConsumeIdentifier, 'identifier3'), ':',
         (
          tokenizer.ConsumeString, 'string'),
         (
          tokenizer.ConsumeIdentifier, 'identifiER_4'), ':',
         (
          tokenizer.ConsumeFloat, 110.0),
         (
          tokenizer.ConsumeIdentifier, 'ID5'), ':',
         (
          tokenizer.ConsumeFloat, -0.23),
         (
          tokenizer.ConsumeIdentifier, 'ID6'), ':',
         (
          tokenizer.ConsumeString, "aaaa'bbbb"),
         (
          tokenizer.ConsumeIdentifier, 'ID7'), ':',
         (
          tokenizer.ConsumeString, 'aa"bb'),
         (
          tokenizer.ConsumeIdentifier, 'ID8'), ':', '{',
         (
          tokenizer.ConsumeIdentifier, 'A'), ':',
         (
          tokenizer.ConsumeFloat, float('inf')),
         (
          tokenizer.ConsumeIdentifier, 'B'), ':',
         (
          tokenizer.ConsumeFloat, -float('inf')),
         (
          tokenizer.ConsumeIdentifier, 'C'), ':',
         (
          tokenizer.ConsumeBool, True),
         (
          tokenizer.ConsumeIdentifier, 'D'), ':',
         (
          tokenizer.ConsumeBool, False), '}',
         (
          tokenizer.ConsumeIdentifier, 'ID9'), ':',
         (
          tokenizer.ConsumeInteger, 22),
         (
          tokenizer.ConsumeIdentifier, 'ID10'), ':',
         (
          tokenizer.ConsumeInteger, -111111111111111111),
         (
          tokenizer.ConsumeIdentifier, 'ID11'), ':',
         (
          tokenizer.ConsumeInteger, -22),
         (
          tokenizer.ConsumeIdentifier, 'ID12'), ':',
         (
          tokenizer.ConsumeInteger, 2222222222222222222),
         (
          tokenizer.ConsumeIdentifier, 'ID13'), ':',
         (
          tokenizer.ConsumeFloat, 1.23456),
         (
          tokenizer.ConsumeIdentifier, 'ID14'), ':',
         (
          tokenizer.ConsumeFloat, 120.0),
         (
          tokenizer.ConsumeIdentifier, 'false_bool'), ':',
         (
          tokenizer.ConsumeBool, False),
         (
          tokenizer.ConsumeIdentifier, 'true_BOOL'), ':',
         (
          tokenizer.ConsumeBool, True),
         (
          tokenizer.ConsumeIdentifier, 'true_bool1'), ':',
         (
          tokenizer.ConsumeBool, True),
         (
          tokenizer.ConsumeIdentifier, 'false_BOOL1'), ':',
         (
          tokenizer.ConsumeBool, False),
         (
          tokenizer.ConsumeIdentifier, 'False_bool'), ':',
         (
          tokenizer.ConsumeBool, False),
         (
          tokenizer.ConsumeIdentifier, 'True_bool'), ':',
         (
          tokenizer.ConsumeBool, True),
         (
          tokenizer.ConsumeIdentifier, 'X'), ':',
         (
          tokenizer.ConsumeFloat, float('inf')),
         (
          tokenizer.ConsumeIdentifier, 'Y'), ':',
         (
          tokenizer.ConsumeFloat, float('-inf')),
         (
          tokenizer.ConsumeIdentifier, 'Z'), ':',
         (
          tokenizer.ConsumeFloat, float('nan'))]
        i = 0
        while not tokenizer.AtEnd():
            m = methods[i]
            if isinstance(m, str):
                token = tokenizer.token
                self.assertEqual(token, m)
                tokenizer.NextToken()
            elif isinstance(m[1], float):
                if math.isnan(m[1]):
                    self.assertTrue(math.isnan(m[0]()))
            else:
                self.assertEqual(m[1], m[0]())
            i += 1

    def testConsumeAbstractIntegers(self):
        int64_max = 9223372036854775807
        uint32_max = 4294967295
        text = '-1 %d %d' % (uint32_max + 1, int64_max + 1)
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertEqual(-1, tokenizer.ConsumeInteger())
        self.assertEqual(uint32_max + 1, tokenizer.ConsumeInteger())
        self.assertEqual(int64_max + 1, tokenizer.ConsumeInteger())
        self.assertTrue(tokenizer.AtEnd())
        text = '-0 0 0 1.2'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertEqual(0, tokenizer.ConsumeInteger())
        self.assertEqual(0, tokenizer.ConsumeInteger())
        self.assertEqual(True, tokenizer.TryConsumeInteger())
        self.assertEqual(False, tokenizer.TryConsumeInteger())
        with self.assertRaises(text_format.ParseError):
            tokenizer.ConsumeInteger()
        self.assertEqual(1.2, tokenizer.ConsumeFloat())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeIntegers(self):
        int64_max = 9223372036854775807
        uint32_max = 4294967295
        text = '-1 %d %d' % (uint32_max + 1, int64_max + 1)
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, text_format._ConsumeUint32, tokenizer)
        self.assertRaises(text_format.ParseError, text_format._ConsumeUint64, tokenizer)
        self.assertEqual(-1, text_format._ConsumeInt32(tokenizer))
        self.assertRaises(text_format.ParseError, text_format._ConsumeUint32, tokenizer)
        self.assertRaises(text_format.ParseError, text_format._ConsumeInt32, tokenizer)
        self.assertEqual(uint32_max + 1, text_format._ConsumeInt64(tokenizer))
        self.assertRaises(text_format.ParseError, text_format._ConsumeInt64, tokenizer)
        self.assertEqual(int64_max + 1, text_format._ConsumeUint64(tokenizer))
        self.assertTrue(tokenizer.AtEnd())
        text = '-0 -0 0 0'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertEqual(0, text_format._ConsumeUint32(tokenizer))
        self.assertEqual(0, text_format._ConsumeUint64(tokenizer))
        self.assertEqual(0, text_format._ConsumeUint32(tokenizer))
        self.assertEqual(0, text_format._ConsumeUint64(tokenizer))
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeOctalIntegers(self):
        """Test support for C style octal integers."""
        text = '00 -00 04 0755 -010 007 -0033 08 -09 01'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertEqual(0, tokenizer.ConsumeInteger())
        self.assertEqual(0, tokenizer.ConsumeInteger())
        self.assertEqual(4, tokenizer.ConsumeInteger())
        self.assertEqual(493, tokenizer.ConsumeInteger())
        self.assertEqual(-8, tokenizer.ConsumeInteger())
        self.assertEqual(7, tokenizer.ConsumeInteger())
        self.assertEqual(-27, tokenizer.ConsumeInteger())
        with self.assertRaises(text_format.ParseError):
            tokenizer.ConsumeInteger()
        tokenizer.NextToken()
        with self.assertRaises(text_format.ParseError):
            tokenizer.ConsumeInteger()
        tokenizer.NextToken()
        self.assertEqual(1, tokenizer.ConsumeInteger())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeByteString(self):
        text = '"string1\''
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeByteString)
        text = 'string1"'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeByteString)
        text = '\n"\\xt"'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeByteString)
        text = '\n"\\"'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeByteString)
        text = '\n"\\x"'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeByteString)

    def testConsumeBool(self):
        text = 'not-a-bool'
        tokenizer = text_format.Tokenizer(text.splitlines())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeBool)

    def testSkipComment(self):
        tokenizer = text_format.Tokenizer('# some comment'.splitlines())
        self.assertTrue(tokenizer.AtEnd())
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeComment)

    def testConsumeComment(self):
        tokenizer = text_format.Tokenizer(('# some comment'.splitlines()), skip_comments=False)
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual('# some comment', tokenizer.ConsumeComment())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeTwoComments(self):
        text = '# some comment\n# another comment'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        self.assertEqual('# some comment', tokenizer.ConsumeComment())
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual('# another comment', tokenizer.ConsumeComment())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeTrailingComment(self):
        text = 'some_number: 4\n# some comment'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeComment)
        self.assertEqual('some_number', tokenizer.ConsumeIdentifier())
        self.assertEqual(tokenizer.token, ':')
        tokenizer.NextToken()
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeComment)
        self.assertEqual(4, tokenizer.ConsumeInteger())
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual('# some comment', tokenizer.ConsumeComment())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeLineComment(self):
        tokenizer = text_format.Tokenizer(('# some comment'.splitlines()), skip_comments=False)
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual((False, '# some comment'), tokenizer.ConsumeCommentOrTrailingComment())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeTwoLineComments(self):
        text = '# some comment\n# another comment'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        self.assertEqual((False, '# some comment'), tokenizer.ConsumeCommentOrTrailingComment())
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual((False, '# another comment'), tokenizer.ConsumeCommentOrTrailingComment())
        self.assertTrue(tokenizer.AtEnd())

    def testConsumeAndCheckTrailingComment(self):
        text = 'some_number: 4  # some comment'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeCommentOrTrailingComment)
        self.assertEqual('some_number', tokenizer.ConsumeIdentifier())
        self.assertEqual(tokenizer.token, ':')
        tokenizer.NextToken()
        self.assertRaises(text_format.ParseError, tokenizer.ConsumeCommentOrTrailingComment)
        self.assertEqual(4, tokenizer.ConsumeInteger())
        self.assertFalse(tokenizer.AtEnd())
        self.assertEqual((True, '# some comment'), tokenizer.ConsumeCommentOrTrailingComment())
        self.assertTrue(tokenizer.AtEnd())

    def testHashinComment(self):
        text = 'some_number: 4  # some comment # not a new comment'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        self.assertEqual('some_number', tokenizer.ConsumeIdentifier())
        self.assertEqual(tokenizer.token, ':')
        tokenizer.NextToken()
        self.assertEqual(4, tokenizer.ConsumeInteger())
        self.assertEqual((True, '# some comment # not a new comment'), tokenizer.ConsumeCommentOrTrailingComment())
        self.assertTrue(tokenizer.AtEnd())

    def testHugeString(self):
        text = '"' + 'a' * 10485760 + '"'
        tokenizer = text_format.Tokenizer((text.splitlines()), skip_comments=False)
        tokenizer.ConsumeString()


@_parameterized.parameters(unittest_pb2, unittest_proto3_arena_pb2)
class PrettyPrinterTest(TextFormatBase):

    def testPrettyPrintNoMatch(self, message_module):

        def printer(message, indent, as_one_line):
            del message
            del indent
            del as_one_line

        message = message_module.TestAllTypes()
        msg = message.repeated_nested_message.add()
        msg.bb = 42
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=True, message_formatter=printer), 'repeated_nested_message { bb: 42 }')

    def testPrettyPrintOneLine(self, message_module):

        def printer(m, indent, as_one_line):
            del indent
            del as_one_line
            if m.DESCRIPTOR == message_module.TestAllTypes.NestedMessage.DESCRIPTOR:
                return 'My lucky number is %s' % m.bb

        message = message_module.TestAllTypes()
        msg = message.repeated_nested_message.add()
        msg.bb = 42
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=True, message_formatter=printer), 'repeated_nested_message { My lucky number is 42 }')

    def testPrettyPrintMultiLine(self, message_module):

        def printer(m, indent, as_one_line):
            if m.DESCRIPTOR == message_module.TestAllTypes.NestedMessage.DESCRIPTOR:
                line_deliminator = (' ' if as_one_line else '\n') + ' ' * indent
                return 'My lucky number is:%s%s' % (line_deliminator, m.bb)

        message = message_module.TestAllTypes()
        msg = message.repeated_nested_message.add()
        msg.bb = 42
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=True, message_formatter=printer), 'repeated_nested_message { My lucky number is: 42 }')
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=False, message_formatter=printer), 'repeated_nested_message {\n  My lucky number is:\n  42\n}\n')

    def testPrettyPrintEntireMessage(self, message_module):

        def printer(m, indent, as_one_line):
            del indent
            del as_one_line
            if m.DESCRIPTOR == message_module.TestAllTypes.DESCRIPTOR:
                return 'The is the message!'

        message = message_module.TestAllTypes()
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=False, message_formatter=printer), 'The is the message!\n')
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=True, message_formatter=printer), 'The is the message!')

    def testPrettyPrintMultipleParts(self, message_module):

        def printer(m, indent, as_one_line):
            del indent
            del as_one_line
            if m.DESCRIPTOR == message_module.TestAllTypes.NestedMessage.DESCRIPTOR:
                return 'My lucky number is %s' % m.bb

        message = message_module.TestAllTypes()
        message.optional_int32 = 61
        msg = message.repeated_nested_message.add()
        msg.bb = 42
        msg = message.repeated_nested_message.add()
        msg.bb = 99
        msg = message.optional_nested_message
        msg.bb = 1
        self.CompareToGoldenText(text_format.MessageToString(message,
          as_one_line=True, message_formatter=printer), 'optional_int32: 61 optional_nested_message { My lucky number is 1 } repeated_nested_message { My lucky number is 42 } repeated_nested_message { My lucky number is 99 }')
        out = text_format.TextWriter(False)
        text_format.PrintField((message_module.TestAllTypes.DESCRIPTOR.fields_by_name['optional_nested_message']),
          (message.optional_nested_message),
          out,
          message_formatter=printer)
        self.assertEqual('optional_nested_message {\n  My lucky number is 1\n}\n', out.getvalue())
        out.close()
        out = text_format.TextWriter(False)
        text_format.PrintFieldValue((message_module.TestAllTypes.DESCRIPTOR.fields_by_name['optional_nested_message']),
          (message.optional_nested_message),
          out,
          message_formatter=printer)
        self.assertEqual('{\n  My lucky number is 1\n}', out.getvalue())
        out.close()


class WhitespaceTest(TextFormatBase):

    def setUp(self):
        self.out = text_format.TextWriter(False)
        self.addCleanup(self.out.close)
        self.message = unittest_pb2.NestedTestAllTypes()
        self.message.child.payload.optional_string = 'value'
        self.field = self.message.DESCRIPTOR.fields_by_name['child']
        self.value = self.message.child

    def testMessageToString(self):
        self.CompareToGoldenText(text_format.MessageToString(self.message), textwrap.dedent('            child {\n              payload {\n                optional_string: "value"\n              }\n            }\n            '))

    def testPrintMessage(self):
        text_format.PrintMessage(self.message, self.out)
        self.CompareToGoldenText(self.out.getvalue(), textwrap.dedent('            child {\n              payload {\n                optional_string: "value"\n              }\n            }\n            '))

    def testPrintField(self):
        text_format.PrintField(self.field, self.value, self.out)
        self.CompareToGoldenText(self.out.getvalue(), textwrap.dedent('            child {\n              payload {\n                optional_string: "value"\n              }\n            }\n            '))

    def testPrintFieldValue(self):
        text_format.PrintFieldValue(self.field, self.value, self.out)
        self.CompareToGoldenText(self.out.getvalue(), textwrap.dedent('            {\n              payload {\n                optional_string: "value"\n              }\n            }'))


if __name__ == '__main__':
    unittest.main()