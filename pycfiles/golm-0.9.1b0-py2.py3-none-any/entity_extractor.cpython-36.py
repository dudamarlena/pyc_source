# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/parsing/entity_extractor.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 890 bytes
from abc import ABC, abstractmethod

class EntityExtractor(ABC):
    __doc__ = '\n    Abstract class for entity extractors.\n    Responsible for processing text and extracting entities such as names, dates, places etc.\n    '

    def __init__(self):
        pass

    @abstractmethod
    def extract_entities(self, text: str, max_retries=5):
        """
        Extracts entities from text (a message from user).
        :param text:        a string.
        :param max_retries: how many times to retry on error.
        :return: A dict of extracted entities.
                 For example:
                 {
                    "place": [
                        {"value": "Prague"},
                        {"value": "New York", "metadata": {}}
                    ],
                    "name": [{"value": "Golem"}],
                    ...
                 }
        """
        return dict()