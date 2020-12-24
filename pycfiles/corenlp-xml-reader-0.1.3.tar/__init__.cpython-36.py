# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1B9074BA60C16502/works/personal/corenlp-webclient/.venv/lib/python3.6/site-packages/corenlp_webclient/__init__.py
# Compiled at: 2019-03-15 00:33:02
# Size of source mod 2**32: 302 bytes
from .annotators import WordsToSentenceAnnotator
from .client import CoreNlpWebClient
from .helpers import create_annotator, chain_words, join_chain_words, extract_words, join_extract_words
from .options import NewlineIsSentenceBreak, WordsToSentenceOptions
from .version import version as __version__