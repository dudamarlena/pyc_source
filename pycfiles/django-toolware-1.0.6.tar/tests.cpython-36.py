# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/tests/tests.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 467 bytes
from django.test import TestCase
from django.conf import settings
from ..utils.query import get_text_tokenizer

class TestStringTokenizerCase(TestCase):
    __doc__ = '\n    Tokenized Test\n    '

    def test_tokenizer_test(self):
        text = 'This is a test -This -is -NOT -a -test'
        includes, excludes = get_text_tokenizer(text)
        self.assertEquals('-'.join(includes), 'This-is-a-test')
        self.assertEquals('-'.join(excludes), 'This-is-NOT-a-test')