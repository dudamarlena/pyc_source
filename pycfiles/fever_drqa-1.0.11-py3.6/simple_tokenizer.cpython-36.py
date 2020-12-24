# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/tokenizers/simple_tokenizer.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 1695 bytes
"""Basic tokenizer that splits text into alpha-numeric tokens and
non-whitespace tokens.
"""
import regex, logging
from .tokenizer import Tokens, Tokenizer
logger = logging.getLogger(__name__)

class SimpleTokenizer(Tokenizer):
    ALPHA_NUM = '[\\p{L}\\p{N}\\p{M}]+'
    NON_WS = '[^\\p{Z}\\p{C}]'

    def __init__(self, **kwargs):
        """
        Args:
            annotators: None or empty set (only tokenizes).
        """
        self._regexp = regex.compile(('(%s)|(%s)' % (self.ALPHA_NUM, self.NON_WS)),
          flags=(regex.IGNORECASE + regex.UNICODE + regex.MULTILINE))
        if len(kwargs.get('annotators', {})) > 0:
            logger.warning('%s only tokenizes! Skipping annotators: %s' % (
             type(self).__name__, kwargs.get('annotators')))
        self.annotators = set()

    def tokenize(self, text):
        data = []
        matches = [m for m in self._regexp.finditer(text)]
        for i in range(len(matches)):
            token = matches[i].group()
            span = matches[i].span()
            start_ws = span[0]
            if i + 1 < len(matches):
                end_ws = matches[(i + 1)].span()[0]
            else:
                end_ws = span[1]
            data.append((
             token,
             text[start_ws:end_ws],
             span))

        return Tokens(data, self.annotators)