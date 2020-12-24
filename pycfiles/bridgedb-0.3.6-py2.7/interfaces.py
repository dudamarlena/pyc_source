# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/interfaces.py
# Compiled at: 2015-11-05 10:40:17
"""All available `Zope`_ interfaces in BridgeDB.

.. _Zope: http://docs.zope.org/zope.interface/index.html
"""
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer

class IName(Interface):
    """An interface specification for a named object."""
    name = Attribute('A string which identifies this object.')


@implementer(IName)
class Named(object):
    """A named object."""
    separator = ' '

    def __init__(self):
        self._name = str()

    @property
    def name(self):
        """Get the name of this object.

        :rtype: str
        :returns: A string which identifies this object.
        """
        return self._name

    @name.setter
    def name(self, name):
        """Set a **name** for identifying this object.

        This is used to identify the object in log messages; the **name**
        doesn't necessarily need to be unique. Other :class:`Named` objects
        which are properties of a :class:`Named` object may inherit their
        parents' **name**s.

        >>> from bridgedb.distribute import Named
        >>> named = Named()
        >>> named.name = 'Excellent Super-Awesome Thing'
        >>> named.name
        'Excellent Super-Awesome Thing'

        :param str name: A name for this object.
        """
        self._name = name
        for attr in self.__dict__.values():
            if IName.providedBy(attr):
                attr.name = self.separator.join([name, attr.name])