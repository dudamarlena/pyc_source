# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/1B9074BA60C16502/works/personal/corenlp-webclient/.venv/lib/python3.6/site-packages/corenlp_webclient/options.py
# Compiled at: 2019-03-08 23:05:53
# Size of source mod 2**32: 1066 bytes
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
__all__ = [
 'BaseOptions', 'NewlineIsSentenceBreak', 'WordsToSentenceOptions']

class BaseOptions(JsonSchemaMixin):
    pass


class NewlineIsSentenceBreak(Enum):
    __doc__ = 'Whether to treat newlines as sentence breaks\n    '
    ALWAYS = 'always'
    NEVER = 'never'
    TWO = 'two'


@dataclass(order=True, frozen=True)
class WordsToSentenceOptions(BaseOptions):
    __doc__ = 'Options of Words-To-Sentence Annotator\n\n    see: https://stanfordnlp.github.io/CoreNLP/ssplit.html\n    '
    eolonly = None
    eolonly: Optional[bool]
    is_one_sentence = None
    is_one_sentence: Optional[bool]
    newline_is_sentence_break = None
    newline_is_sentence_break: Optional[NewlineIsSentenceBreak]
    boundary_multi_token_regex = None
    boundary_multi_token_regex: Optional[str]
    boundary_token_regex = None
    boundary_token_regex: Optional[str]
    boundaries_to_discard = None
    boundaries_to_discard: Optional[str]
    html_boundaries_to_discard = None
    html_boundaries_to_discard: Optional[str]
    token_patterns_to_discard = None
    token_patterns_to_discard: Optional[str]
    boundary_followers_regex = None
    boundary_followers_regex: Optional[str]