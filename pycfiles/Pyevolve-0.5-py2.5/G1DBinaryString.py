# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyevolve\G1DBinaryString.py
# Compiled at: 2009-01-21 20:09:24
"""
:mod:`G1DBinaryString` -- the classical binary string chromosome
=====================================================================

This is the classical chromosome representation on GAs, it is the 1D
Binary String. This string looks like "00011101010".

"""
from GenomeBase import GenomeBase
import Consts, Util

class G1DBinaryString(GenomeBase):
    """ G1DBinaryString Class - The 1D Binary String chromosome
   
   Example:
      >>> g = G1DBinaryString(5)

   :param length: the 1D Binary String size

   """
    evaluator = None
    initializator = None
    mutator = None
    crossover = None

    def __init__(self, length=10):
        """ The initializator of G1DList representation, size parameter must be specified """
        GenomeBase.__init__(self)
        self.genomeString = []
        self.stringLength = length
        self.initializator.set(Consts.CDefG1DBinaryStringInit)
        self.mutator.set(Consts.CDefG1DBinaryStringMutator)
        self.crossover.set(Consts.CDefG1DBinaryStringCrossover)

    def __eq__(self, other):
        """ Compares one chromosome with another
      
      :param other: the other G1DBinaryString instance
      :rtype: True or False

      """
        cond1 = self.genomeString == other.genomeString
        cond2 = self.stringLength == other.stringLength
        return True if cond1 and cond2 else False

    def __getslice__(self, a, b):
        """ Return the sliced part of chromosome 

      >>> g = G1DBinaryString(5)
      >>> for i in xrange(len(g)):
      ...    g.append(1)
      >>> g[2:4]
      [1, 1]

      """
        return self.genomeString[a:b]

    def __setslice__(self, a, b, val):
        """ Sets the slice part of chromosome 

      >>> g = G1DBinaryString(5)
      >>> for i in xrange(len(g)):
      ...    g.append(0)
      >>> g[1:3] = [1, 1]
      >>> g.getBinary()
      '01100'

      """
        self.genomeString[a:b] = val

    def __getitem__(self, key):
        """ Return the specified gene of List

      >>> g = G1DBinaryString(5)
      >>> for i in xrange(len(g)):
      ...    g.append(1)
      >>> g[4]
      1
      >>> g[20]
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      IndexError: list index out of range
      
      """
        return self.genomeString[key]

    def __setitem__(self, key, value):
        """ Set the specified value for an gene of List

      >>> g = G1DBinaryString(5)
      >>> for i in xrange(len(g)):
      ...    g.append(1)
      >>> g[4] = 0
      >>> g[4]
      0

      """
        if len(self.genomeString) <= 0:
            Util.raiseException('The string is not initialized !')
        if value not in (0, 1):
            Util.raiseException('The value must be zero (0) or one (1)', ValueError)
        self.genomeString[key] = value

    def __iter__(self):
        """ Iterator support to the list
      
      >>> g = G1DBinaryString(5)
      >>> for i in xrange(len(g)):
      ...   g.append(1)
      >>> for v in g:
      ...   print v,
      1 1 1 1 1

      """
        return iter(self.genomeString)

    def __len__(self):
        """ Return the size of the List

      >>> g = G1DBinaryString(5)
      >>> len(g)
      5

      """
        return self.stringLength

    def __repr__(self):
        """ Return a string representation of Genome """
        ret = GenomeBase.__repr__(self)
        ret += '- G1DBinaryString\n'
        ret += '\tString length:\t %s\n' % (self.stringLength,)
        ret += '\tString:\t\t %s\n\n' % (self.getBinary(),)
        return ret

    def getDecimal(self):
        """ Converts the binary string to decimal representation

      Example:
         >>> g = G1DBinaryString(5)
         >>> for i in xrange(len(g)):
         ...    g.append(0)
         >>> g[3] = 1
         >>> g.getDecimal()
         2

      :rtype: decimal value

      """
        return int(self.getBinary(), 2)

    def getBinary(self):
        """ Returns the binary string representation

      Example:
         >>> g = G1DBinaryString(2)
         >>> g.append(0)
         >>> g.append(1)
         >>> g.getBinary()
         '01'

      :rtype: the binary string

      """
        return ('').join(map(str, self))

    def append(self, value):
        """ Appends an item to the list

      Example:
         >>> g = G1DBinaryString(2)
         >>> g.append(0)

      :param value: value to be added, 0 or 1

      """
        if value not in (0, 1):
            Util.raiseException('The value must be 0 or 1', ValueError)
        self.genomeString.append(value)

    def clearString(self):
        """ Remove all genes from Genome """
        del self.genomeString[:]

    def copy(self, g):
        """ Copy genome to 'g'

      Example:
         >>> g1 = G1DBinaryString(2)
         >>> g1.append(0)
         >>> g1.append(1)
         >>> g2 = G1DBinaryString(2)
         >>> g1.copy(g2)
         >>> g2[1]
         1

      :param g: the destination genome

      """
        GenomeBase.copy(self, g)
        g.stringLength = self.stringLength
        g.genomeString = self.genomeString[:]

    def clone(self):
        """ Return a new instace copy of the genome
      
      Example:
         >>> g = G1DBinaryString(5)
         >>> for i in xrange(len(g)):
         ...    g.append(1)
         >>> clone = g.clone()
         >>> clone[0]
         1

      :rtype: the G1DBinaryString instance clone

      """
        newcopy = G1DBinaryString(self.stringLength)
        self.copy(newcopy)
        return newcopy