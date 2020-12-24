# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\G2DList.py
# Compiled at: 2009-01-21 20:09:54
__doc__ = '\n:mod:`G2DList` -- the 2D list chromosome\n================================================================\n\nThis is the 2D List representation, this list can carry real numbers or\nintegers or any kind of object, by default, we have genetic operators\nfor integer and real lists, which can be found on the respective modules.\nThis chromosome class extends the :class:`GenomeBase.GenomeBase`.\n\n'
from GenomeBase import GenomeBase
import Consts

class G2DList(GenomeBase):
    """ G2DList Class - The 2D List chromosome representation

   **Examples**

      The instantiation
         >>> genome = G2DList.G2DList(10, 10)

      The instantiation
         >>> g = G1DList(10)

      Compare
         >>> genome2 = genome1.clone()
         >>> genome2 == genome1
         True

      Iteration
         >>> for row in genome:
         >>>   print row
         [1, 3, 4, 1]
         [7, 5, 3, 4]
         [9, 0, 1, 2]

      Size, slice, get/set, append
         >>> len(genome)
         3
         >>> genome
         (...)
         [1, 3, 4, 1]
         [7, 5, 3, 4]
         [9, 0, 1, 2]
         >>> genome[1][2]
         3
         >>> genome[1] = [666, 666, 666, 666]
         >>> genome
         (...)
         [1, 3, 4, 1]
         [666, 666, 666, 666]
         [9, 0, 1, 2]

   :param height: the number of rows
   :param width: the number of columns

   """
    evaluator = None
    initializator = None
    mutator = None
    crossover = None

    def __init__(self, height, width):
        """ The initializator of G2DList representation,
      height and width must be specified """
        GenomeBase.__init__(self)
        self.height = height
        self.width = width
        self.genomeList = [
         None] * height
        for i in xrange(height):
            self.genomeList[i] = [
             None] * width

        self.initializator.set(Consts.CDefG2DListInit)
        self.mutator.set(Consts.CDefG2DListMutator)
        self.crossover.set(Consts.CDefG2DListCrossover)
        return

    def __eq__(self, other):
        """ Compares one chromosome with another """
        cond1 = self.genomeList == other.genomeList
        cond2 = self.height == other.height
        cond3 = self.width == other.width
        return True if cond1 and cond2 and cond3 else False

    def getItem(self, x, y):
        """ Return the specified gene of List

      Example:
         >>> genome.getItem(3, 1)
         666
      
      :param x: the x index, the column
      :param y: the y index, the row
      :rtype: the item at x,y position
      
      """
        return self.genomeList[x][y]

    def setItem(self, x, y, value):
        """ Set the specified gene of List

      Example:
         >>> genome.setItem(3, 1, 666)
      
      :param x: the x index, the column
      :param y: the y index, the row
      :param value: the value
      
      """
        self.genomeList[x][y] = value

    def __getitem__(self, key):
        """ Return the specified gene of List """
        return self.genomeList[key]

    def __iter__(self):
        """ Iterator support to the list """
        return iter(self.genomeList)

    def getHeight(self):
        """ Return the height (lines) of the List """
        return self.height

    def getWidth(self):
        """ Return the width (lines) of the List """
        return self.width

    def getSize(self):
        """ Returns a tuple (height, widht)
   
      Example:
         >>> genome.getSize()
         (3, 2)

      """
        return (
         self.getHeight(), self.getWidth())

    def __repr__(self):
        """ Return a string representation of Genome """
        ret = GenomeBase.__repr__(self)
        ret += '- G2DList\n'
        ret += '\tList size:\t %s\n' % (self.getSize(),)
        ret += '\tList:\n'
        for line in self.genomeList:
            ret += '\t\t\t'
            for item in line:
                ret += '[%s] ' % item

            ret += '\n'

        ret += '\n'
        return ret

    def clearList(self):
        """ Remove all genes from Genome """
        del self.genomeList[:]
        self.genomeList = [
         None] * self.height
        for i in xrange(self.height):
            self.genomeList[i] = [
             None] * self.width

        return

    def copy(self, g):
        """ Copy genome to 'g'
      
      Example:
         >>> genome_origin.copy(genome_destination)
      
      :param g: the destination G2DList instance

      """
        GenomeBase.copy(self, g)
        g.height = self.height
        g.width = self.width
        for i in xrange(self.height):
            g.genomeList[i] = self.genomeList[i][:]

    def clone(self):
        """ Return a new instace copy of the genome
      
      :rtype: the G2DList clone instance

      """
        newcopy = G2DList(self.height, self.width)
        self.copy(newcopy)
        return newcopy