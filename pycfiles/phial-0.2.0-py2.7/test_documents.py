# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/phial/tests/test_documents.py
# Compiled at: 2014-04-22 23:03:09
from .. import documents
import pytest, StringIO, tempfile, os, codecs
UNICODE_TEST_PONY = 'TH̘Ë͖́̉ ͠P̯͍̭O̚\u200bN̐Y̡'
SAMPLE_FILES = [
 {'raw': 'key1: value1\nkey2: value2\n...\n\nDestruction.', 
    'frontmatter': {'key1': 'value1', 'key2': 'value2'}, 'body': '\nDestruction.'},
 {'raw': '', 
    'frontmatter': None, 
    'body': ''},
 {'raw': UNICODE_TEST_PONY, 
    'frontmatter': None, 
    'body': UNICODE_TEST_PONY}]
TEST_ENCODINGS = [
 ('utf_8', '', 'utf_8'),
 ('utf_8_sig', '', 'utf_8_sig'),
 ('utf_16', '', 'utf_16'),
 (
  'utf_16_be', codecs.BOM_UTF16_BE, 'utf_16'),
 (
  'utf_16_le', codecs.BOM_UTF16_LE, 'utf_16')]

class TestDocuments:

    @pytest.mark.parametrize('sample', SAMPLE_FILES)
    def test_frontmatter_parsing(self, sample):
        """Ensure that frontmatter is parsed correctly."""
        fake_file = StringIO.StringIO(sample['raw'])
        f = documents.Document(fake_file)
        assert f.frontmatter == sample['frontmatter']

    @pytest.mark.parametrize('encoding', TEST_ENCODINGS)
    def test_open_file(self, encoding):
        encoded_pony = encoding[1] + UNICODE_TEST_PONY.encode(encoding[0])
        print repr(encoded_pony)
        with tempfile.NamedTemporaryFile(delete=False) as (f):
            f.write(encoded_pony)
            delete_path = f.name
        try:
            with documents.open_file(f.name) as (f):
                result = f.read()
                result_encoding = f.encoding
        finally:
            os.remove(delete_path)

        assert f.encoding == encoding[2]
        assert result == UNICODE_TEST_PONY