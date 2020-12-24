# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1B9074BA60C16502/works/personal/corenlp-webclient/.venv/lib/python3.6/site-packages/corenlp_webclient/annotators.py
# Compiled at: 2019-03-08 23:05:53
# Size of source mod 2**32: 1021 bytes
from typing import Any, Dict, Type
from .options import BaseOptions, WordsToSentenceOptions
__all__ = [
 'BaseAnnotator', 'WordsToSentenceAnnotator']

def _snake_to_camel(s):
    parts = s.strip().split('_')
    return parts[0] + ''.join([w.title() for w in parts])


class BaseAnnotator:
    name: str = ''
    options_class = BaseOptions
    options_class: Type[BaseOptions]

    def __init__(self, options: BaseOptions=None):
        self._options = options
        self._options_dict = self.make_options_dict()

    def make_options_dict(self) -> Dict[(str, Any)]:
        if self._options:
            return {'.'.join([self.name, _snake_to_camel(k)]):v for k, v in self._options.to_dict().items()}
        else:
            return {}

    @property
    def options_dict(self) -> Dict[(str, Any)]:
        return self._options_dict


class WordsToSentenceAnnotator(BaseAnnotator):
    name = 'ssplit'
    options_class = WordsToSentenceOptions