# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/Axon.py
# Compiled at: 2008-10-19 12:19:52
"""=================
Axon base classes
=================

What is defined here is a metaclass that is used as a base class for some key
classes in Axon.

It was originally created to allow super class calling in a slightly nicer
manner in terms of syntactic sugar easier to get right that still
has the good effects of "super" in a multiple inheritance scenario. **Use of
this particular feature has been deprecated** because of more subtle issues in
inheritance situations.

However this metaclass has been retained (and is still used) for possible future
uses.

* AxonObject is the base class for Axon.Microprocess.microprocess and
  Axon.Linkage.linkage

"""

class AxonType(type):
    """   Metaclass for Axon objects.
   """

    def __init__(cls, name, bases, dict):
        """      Override creation of class to set a 'super' attribute to what you get
      when you call super().

      **Note** that this 'super' attribute is deprecated - there are some subtle
      issues with it and it should therefore be avoided.
      """
        super(AxonType, cls).__init__(name, bases, dict)
        setattr(cls, '_%s__super' % name, super(cls))


class AxonObject(object):
    """   Base class for axon objects.

   Uses AxonType as its metaclass.
   """
    __metaclass__ = AxonType


if __name__ == '__main__':

    class foo(AxonObject):

        def __init__(self):
            self.gah = 1
            print 'foo', self


    class bar(foo):

        def __init__(self):
            super(bar, self).__init__()
            self.gee = 1
            self.gah += 1
            print 'bar', self


    class bla(foo):

        def __init__(self):
            super(bla, self).__init__()
            self.goo = 2
            self.gah += 1
            print 'bla', self


    class barbla(bar, bla):

        def __init__(self):
            super(barbla, self).__init__()
            self.gee += 1
            self.goo += 2
            self.gah += 1
            print 'barbla', self


    a = foo()
    assert a.gah == 1, "Foo's initialisation failed"
    b = bar()
    assert (b.gee, b.gah) == (1, 2), "Bar & Foo's chained initialisation failed"
    c = bla()
    assert (c.goo, c.gah) == (2, 2), "Bla & Foo's chained initialisation failed"
    d = barbla()
    assert (d.gee, d.goo, d.gah) == (2, 4, 4), "BarBla, Bla, Bar & Foo's chained initialisation failed"