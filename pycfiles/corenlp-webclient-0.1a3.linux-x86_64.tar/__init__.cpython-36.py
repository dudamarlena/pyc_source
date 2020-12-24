# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/1B9074BA60C16502/works/personal/corenlp-webclient/.venv/lib/python3.6/site-packages/corenlp_webclient/__init__.py
# Compiled at: 2019-03-15 00:33:02
# Size of source mod 2**32: 302 bytes
from .annotators import WordsToSentenceAnnotator
from .client import CoreNlpWebClient
from .helpers import create_annotator, chain_words, join_chain_words, extract_words, join_extract_words
from .options import NewlineIsSentenceBreak, WordsToSentenceOptions
from .version import version as __version__