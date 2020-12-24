# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/api/model.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 29, 2012\n\n@package: ally api\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides standard model objects.\n'
from ally.support.util_io import IInputStream
import abc

class Content(IInputStream):
    """
    Class that provides a bytes content, usually the raw content provided in a request.
    """
    __slots__ = ('name', 'type', 'charSet', 'length')

    def __init__(self, name=None, type=None, charSet=None, length=None):
        """
        Construct the content.
        
        @param name: string|None
            The name of the content, usually a file name.
        @param type: string|None
            The type of the content.
        @param charSet: string|None
            The character set specified for the content.
        @param length: integer|None
            The length in bytes for the content.
        """
        if not name is None:
            assert isinstance(name, str), 'Invalid name %s' % name
            if not type is None:
                assert isinstance(type, str), 'Invalid type %s' % type
                if not charSet is None:
                    assert isinstance(charSet, str), 'Invalid char set %s' % charSet
                    if not length is None:
                        assert isinstance(length, int), 'Invalid length %s' % length
                        self.name = name
                        self.type = type
                        self.charSet = charSet
                        self.length = length
                        return

    @abc.abstractclassmethod
    def next(self):
        """
        Only call this method after the content has been properly processed, it will act also as a close method. If
        there is additional content available this method will return the next Content object otherwise it will return
        None.
        
        @return: Content|None
            The next content or None, if there is no more available.
        """
        pass