# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/idGen.py
# Compiled at: 2008-10-19 12:19:52
"""====================
Unique ID generation
====================

The methods of the idGen class are used to generate unique IDs in various forms
(numbers, strings, etc) which are used to give microprocesses and other Axon
objects a unique identifier and name.

* Every Axon.Microprocess.microprocess gets a unique ID
* Axon.ThreadedComponent.threadedcomponent uses unique IDs to identify threads

Generating a new unique ID
--------------------------

Do not use the idGen class defined in this module directly. Instead, use any
of these module methods to obtain a unique ID:

* **Axon.idGen.newId(thing)** - returns a unique identifier as a string based on
  the class name of the object provided

* **Axon.idGen.strId(thing)** - returns a unique identifier as a string based on
  the class name of the object provided

* **Axon.idGen.numId()** - returns a unique identifier as a number

* **Axon.idGen.tupleId(thing)** - returns both the numeric and string versions
  of a new unique id as a tuple (where the string version is based on the class
  name of the object provided)

Calling tupleId(thing) is *not* equivalent to calling numId() then strId(thing)
because doing that would return two different id values! 

Examples::

    >>> x=Component.component()
    >>> idGen.newId(x)
    'Component.component_4'
    >>> idGen.strId(x)
    'Component.component_5'
    >>> idGen.numId()
    6
    >>> idGen.tupleId(x)
    (7, 'Component.component_7')

"""
import debug
debugger = debug.debug()
debugger.useConfig()
Debug = debugger.debug

class idGen(object):
    """   Unique ID creator.

   Use numId(), strId(), and tupleId() methods to obtain unique IDs.
   """
    lowestAllocatedId = 0

    def nextId(self):
        """      **INTERNAL**

      Returns the next unique id, incrementing the private class variable
      """
        idGen.lowestAllocatedId = idGen.lowestAllocatedId + 1
        return idGen.lowestAllocatedId

    next = nextId

    def idToString(self, thing, aNumId):
        """      **INTERNAL**
       
      Combines the 'str()' of the object's class with the id to form a string id
      """
        r = str(thing.__class__)[8:][:-2] + '_' + str(aNumId)
        return r

    def numId(self):
        """Allocates & returns the next available id"""
        result = self.nextId()
        assert Debug('idGen.numId', 1, 'idGen.numId:', result)
        return result

    def strId(self, thing):
        """      Allocates & returns the next available id combined with the object's
      class name, in string form
      """
        theId = self.nextId()
        strid = self.idToString(thing, theId)
        assert Debug('idGen.strId', 1, 'idGen.strId:', strid)
        return strid

    def tupleId(self, thing):
        """      Allocates the next available id and returns it both as a tuple (num,str)
      containing both the numeric version and a string version where it is
      combined with the object's class name.
      """
        theId = self.nextId()
        strId = self.idToString(thing, theId)
        assert Debug('idGen.tupleId', 1, 'idGen.tupleId:', theId, strId)
        return (theId, strId)


newId = idGen().strId
strId = idGen().strId
numId = idGen().numId
tupleId = idGen().tupleId
if __name__ == '__main__':

    class foo:
        pass


    class bar:
        pass


    class bibble:
        pass


    print newId(foo())
    print newId(bar())
    print newId(bibble())