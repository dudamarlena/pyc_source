# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\xmlreader.py
# Compiled at: 2020-01-13 13:07:08
# Size of source mod 2**32: 2421 bytes
import sys
from xml import sax
from .textnormalize import text_normalize_filter
import pdb

class label_dict_handler(sax.ContentHandler):
    CAPTURE_KEY = 1
    CAPTURE_LABEL_ITEM = 2
    CAPTURE_ADDRESS_ITEM = 3

    def __init__(self):
        self.label_dict = {}
        self._item_to_create = None
        self._state = None

    def startElement(self, name, attributes):
        if name == 'label':
            self._curr_label = {}
        else:
            if name == 'address':
                self._address = {}
            else:
                if name == 'name':
                    self._state = self.CAPTURE_KEY
                if name == 'quote':
                    self._item_to_create = name
                    self._state = self.CAPTURE_LABEL_ITEM
            if name in ('street', 'city', 'state'):
                self._item_to_create = name
                self._state = self.CAPTURE_ADDRESS_ITEM

    def endElement(self, name):
        if name == 'address':
            self._curr_label['address'] = self._address
        if name in ('quote', 'name', 'street', 'city', 'state'):
            self._state = None

    def characters(self, text):
        if self._state == self.CAPTURE_KEY:
            self.label_dict[text] = self._curr_label
        else:
            curr_dict = None
            if self._state == self.CAPTURE_ADDRESS_ITEM:
                curr_dict = self._address
            if self._state == self.CAPTURE_LABEL_ITEM:
                curr_dict = self._curr_label
            print(repr(text), curr_dict)
            if curr_dict is not None:
                if self._item_to_create in curr_dict:
                    curr_dict[self._item_to_create] += text
                else:
                    curr_dict[self._item_to_create] = text


if __name__ == '__main__':
    parser = sax.make_parser()
    downstream_handler = label_dict_handler()
    filter_handler = text_normalize_filter(parser, downstream_handler)
    filter_handler.parse(sys.argv[1])
    label_dict = downstream_handler.label_dict
    pdb.set_trace()