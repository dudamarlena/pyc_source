# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\sequence.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 2332 bytes
"""Hold the Sequence class, which stores a dicom sequence (list of Datasets)"""
from dicom.dataset import Dataset
from dicom.multival import MultiValue

def validate_dataset(elem):
    """Ensures that the value is a Dataset instance"""
    if not isinstance(elem, Dataset):
        raise TypeError('Sequence contents must be a Dataset instance')
    return elem


class Sequence(MultiValue):
    __doc__ = 'Class to hold multiple Datasets in a list\n\n    This class is derived from MultiValue and as such enforces that all items\n    added to the list are Dataset instances. In order to due this, a validator\n    is substituted for type_constructor when constructing the MultiValue super\n    class\n    '

    def __init__(self, iterable=None):
        """Initialize a list of Datasets

        :param iterable: an iterable (e.g. list, tuple) of Datasets. If no
                        value is provided, an empty Sequence is generated
        """
        if isinstance(iterable, Dataset):
            raise TypeError('The Sequence constructor requires an iterable')
        if not iterable:
            iterable = list()
        super(Sequence, self).__init__(validate_dataset, iterable)

    def __str__(self):
        lines = [str(x) for x in self]
        return '[' + ''.join(lines) + ']'

    def __repr__(self):
        """Sequence-specific string representation"""
        formatstr = '<%(classname)s, length %(count)d, at %(id)X>'
        return formatstr % {'classname': self.__class__.__name__, 
         'id': id(self), 'count': len(self)}