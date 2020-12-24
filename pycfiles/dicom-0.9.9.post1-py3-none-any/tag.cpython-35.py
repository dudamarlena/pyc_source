# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\tag.py
# Compiled at: 2017-01-26 21:09:38
# Size of source mod 2**32: 4825 bytes
"""Define Tag class to hold a dicom (group, element) tag"""

def Tag(arg, arg2=None):
    """General function for creating a Tag in any of the standard forms:
    e.g.  Tag(0x00100010), Tag(0x10,0x10), Tag((0x10, 0x10))
    """
    if arg2 is not None:
        arg = (
         arg, arg2)
    if isinstance(arg, (tuple, list)):
        if len(arg) != 2:
            raise ValueError('Tag must be an int or a 2-tuple')
        if isinstance(arg[0], str):
            if not isinstance(arg[1], str):
                raise ValueError('Both arguments must be hex strings if one is')
            arg = (
             int(arg[0], 16), int(arg[1], 16))
        if arg[0] > 65535 or arg[1] > 65535:
            raise OverflowError('Groups and elements of tags must each be <=2 byte integers')
        long_value = arg[0] << 16 | arg[1]
    else:
        if isinstance(arg, str):
            raise ValueError('Tags cannot be instantiated from a single string')
        else:
            long_value = arg
    if long_value > 4294967295:
        raise OverflowError('Tags are limited to 32-bit length; tag {0!r}'.format(arg))
    return BaseTag(long_value)


BaseTag_base_class = int

class BaseTag(BaseTag_base_class):
    __doc__ = 'Class for storing the dicom (group, element) tag'

    def __lt__(self, other):
        if not isinstance(other, BaseTag):
            try:
                other = Tag(other)
            except:
                raise TypeError('Cannot compare Tag with non-Tag item')

            return int(self) < int(other)

    def __eq__(self, other):
        if not isinstance(other, BaseTag):
            try:
                other = Tag(other)
            except:
                raise TypeError('Cannot compare Tag with non-Tag item')

            return int(self) == int(other)

    def __ne__(self, other):
        if not isinstance(other, BaseTag):
            try:
                other = Tag(other)
            except:
                raise TypeError('Cannot compare Tag with non-Tag item')

            return int(self) != int(other)

    __hash__ = int.__hash__

    def __str__(self):
        """String of tag value as (gggg, eeee)"""
        return '({0:04x}, {1:04x})'.format(self.group, self.element)

    __repr__ = __str__

    @property
    def group(self):
        return self >> 16

    @property
    def element(self):
        """Return the element part of the (group,element) tag"""
        return self & 65535

    elem = element

    @property
    def is_private(self):
        """Return a boolean to indicate whether the tag is a private tag (odd group number)"""
        return self.group % 2 == 1


def TupleTag(group_elem):
    """Fast factory for BaseTag object with known safe (group, element) tuple"""
    long_value = group_elem[0] << 16 | group_elem[1]
    return BaseTag(long_value)


ItemTag = TupleTag((65534, 57344))
ItemDelimiterTag = TupleTag((65534, 57357))
SequenceDelimiterTag = TupleTag((65534, 57565))