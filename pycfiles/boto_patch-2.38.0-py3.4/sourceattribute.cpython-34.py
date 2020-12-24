# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudsearch/sourceattribute.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3156 bytes


class SourceAttribute(object):
    __doc__ = '\n    Provide information about attributes for an index field.\n    A maximum of 20 source attributes can be configured for\n    each index field.\n\n    :ivar default: Optional default value if the source attribute\n        is not specified in a document.\n        \n    :ivar name: The name of the document source field to add\n        to this ``IndexField``.\n\n    :ivar data_function: Identifies the transformation to apply\n        when copying data from a source attribute.\n        \n    :ivar data_map: The value is a dict with the following keys:\n        * cases - A dict that translates source field values\n            to custom values.\n        * default - An optional default value to use if the\n            source attribute is not specified in a document.\n        * name - the name of the document source field to add\n            to this ``IndexField``\n    :ivar data_trim_title: Trims common title words from a source\n        document attribute when populating an ``IndexField``.\n        This can be used to create an ``IndexField`` you can\n        use for sorting.  The value is a dict with the following\n        fields:\n        * default - An optional default value.\n        * language - an IETF RFC 4646 language code.\n        * separator - The separator that follows the text to trim.\n        * name - The name of the document source field to add.\n    '
    ValidDataFunctions = ('Copy', 'TrimTitle', 'Map')

    def __init__(self):
        self.data_copy = {}
        self._data_function = self.ValidDataFunctions[0]
        self.data_map = {}
        self.data_trim_title = {}

    @property
    def data_function(self):
        return self._data_function

    @data_function.setter
    def data_function(self, value):
        if value not in self.ValidDataFunctions:
            valid = '|'.join(self.ValidDataFunctions)
            raise ValueError('data_function must be one of: %s' % valid)
        self._data_function = value