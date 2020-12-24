# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\G1DList.py
# Compiled at: 2009-01-21 20:09:34
__doc__ = '\n\n:mod:`G1DList` -- the 1D list chromosome\n=============================================================\n\nThis is the 1D List representation, this list can carry real\nnumbers or integers or any kind of object, by default, we have\ngenetic operators for integer and real lists, which can be found\non the respective modules. This chromosome class extends the :class:`GenomeBase.GenomeBase` class.\n\n'
from GenomeBase import GenomeBase
import Consts

class G1DList(GenomeBase):
    """ G1DList Class - The 1D List chromosome representation
   
   **Examples**

      The instantiation
         >>> g = G1DList(10)

      Compare
         >>> genome2 = genome1.clone()
         >>> genome2 == genome1
         True

      Multiply
         >>> genome = population[0]
         >>> genome
         (...)
         [1, 2, 3, 4]
         >>> genome_result = genome * 2
         >>> genome_result
         (...)
         [2, 2, 6, 8]

      Add
         >>> genome
         (...)
         [1, 2, 3, 4]
         >>> genome_result = genome + 2
         (...)
         [3, 4, 5, 6]
         
      Iteration
         >>> for i in genome:
         >>>   print i
         1
         2
         3
         4

      Size, slice, get/set, append
         >>> len(genome)
         4
         >>> genome
         (...)
         [1, 2, 3, 4]
         >>> genome[0:1]
         [1, 2]
         >>> genome[1] = 666
         >>> genome
         (...)
         [1, 666, 3, 4]
         >>> genome.append(99)
         >>> genome
         (...)
         [1, 666, 3, 4, 99]

   :param size: the 1D list size

   """
    evaluator = None
    initializator = None
    mutator = None
    crossover = None

    def __init__(self, size):
        """ The initializator of G1DList representation,
      size parameter must be specified """
        GenomeBase.__init__(self)
        self.genomeList = []
        self.listSize = size
        self.initializator.set(Consts.CDefG1DListInit)
        self.mutator.set(Consts.CDefG1DListMutator)
        self.crossover.set(Consts.CDefG1DListCrossover)

    def __eq__(self, other):
        """ Compares one chromosome with another """
        cond1 = self.genomeList == other.genomeList
        cond2 = self.listSize == other.listSize
        return True if cond1 and cond2 else False

    def __mul__(self, other):
        """ Multiply every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] *= other

        return newObj

    def __add__(self, other):
        """ Plus every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] += other

        return newObj

    def __sub__(self, other):
        """ Plus every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] -= other

        return newObj

    def __getslice__(self, a, b):
        """ Return the sliced part of chromosome """
        return self.genomeList[a:b]

    def __getitem__(self, key):
        """ Return the specified gene of List """
        return self.genomeList[key]

    def __setitem__(self, key, value):
        """ Set the specified value for an gene of List """
        self.genomeList[key] = value

    def __iter__(self):
        """ Iterator support to the list """
        return iter(self.genomeList)

    def __len__(self):
        """ Return the size of the List """
        return len(self.genomeList)

    def __repr__(self):
        """ Return a string representation of Genome """
        ret = GenomeBase.__repr__(self)
        ret += '- G1DList\n'
        ret += '\tList size:\t %s\n' % (self.listSize,)
        ret += '\tList:\t\t %s\n\n' % (self.genomeList,)
        return ret

    def append(self, value):
        """ Appends an item to the list
      
      Example:
         >>> genome.append(44)

      :param value: value to be added
      
      """
        self.genomeList.append(value)

    def clearList(self):
        """ Remove all genes from Genome """
        del self.genomeList[:]

    def copy(self, g):
        """ Copy genome to 'g'
      
      Example:
         >>> genome_origin.copy(genome_destination)
      
      :param g: the destination G1DList instance

      """
        GenomeBase.copy(self, g)
        g.listSize = self.listSize
        g.genomeList = self.genomeList[:]

    def clone(self):
        """ Return a new instace copy of the genome
      
      :rtype: the G1DList clone instance

      """
        newcopy = G1DList(self.listSize)
        self.copy(newcopy)
        return newcopy