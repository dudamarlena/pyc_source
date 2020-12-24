# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/api/model.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 29, 2012

@package: ally api
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides standard model objects.
"""
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