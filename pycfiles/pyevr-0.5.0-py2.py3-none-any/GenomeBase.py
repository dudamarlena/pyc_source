# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\GenomeBase.py
# Compiled at: 2009-01-21 19:09:01
__doc__ = '\n\n:mod:`GenomeBase` -- the genomes base module\n================================================================\n\nThis module have the class which every representation extends,\nif you are planning to create a new representation, you must\ntake a inside look into this module.\n\n'
from FunctionSlot import FunctionSlot

class GenomeBase:
    """ GenomeBase Class - The base of all chromosome representation """
    evaluator = None
    initializator = None
    mutator = None
    crossover = None

    def __init__(self):
        """Genome Constructor"""
        self.evaluator = FunctionSlot('Evaluator')
        self.initializator = FunctionSlot('Initializator')
        self.mutator = FunctionSlot('Mutator')
        self.crossover = FunctionSlot('Crossover')
        self.allSlots = [
         self.evaluator, self.initializator,
         self.mutator, self.crossover]
        self.internalParams = {}
        self.score = 0.0
        self.fitness = 0.0

    def getRawScore(self):
        """ Get the Raw Score of the genome

      :rtype: genome raw score

      """
        return self.score

    def getFitnessScore(self):
        """ Get the Fitness Score of the genome

      :rtype: genome fitness score

      """
        return self.fitness

    def __repr__(self):
        """String representation of Genome"""
        ret = '- GenomeBase\n'
        ret += '\tScore:\t\t\t %.6f\n' % (self.score,)
        ret += '\tFitness:\t\t %.6f\n\n' % (self.fitness,)
        for slot in self.allSlots:
            ret += '\t' + slot.__repr__()

        ret += '\n'
        return ret

    def setParams(self, **args):
        """ Set the initializator params

      Example:
         >>> genome.setParams(rangemin=0, rangemax=100, gauss_mu=0, gauss_sigma=1)

      :param args: this params will saved in every chromosome for genetic op. use

      """
        self.internalParams.update(args)

    def getParam(self, key, nvl=None):
        """ Gets an initialization parameter

      Example:
         >>> genome.getParam("rangemax")
         100

      :param key: the key of param
      :param nvl: if the key doesn't exist, the nvl will be returned

      """
        return self.internalParams.get(key, nvl)

    def resetStats(self):
        """ Clear score and fitness of genome """
        self.score = 0.0
        self.fitness = 0.0

    def evaluate(self, **args):
        """ Called to evaluate genome

      :param args: this parameters will be passes to the evaluator

      """
        self.resetStats()
        for it in self.evaluator.applyFunctions(self, **args):
            self.score += it

    def initialize(self, **args):
        """ Called to initialize genome

      :param args: this parameters will be passed to the initializator

      """
        for it in self.initializator.applyFunctions(self, **args):
            pass

    def mutate(self, **args):
        """ Called to mutate the genome

      :param args: this parameters will be passed to the mutator

      """
        nmuts = 0
        for it in self.mutator.applyFunctions(self, **args):
            nmuts += it

        return nmuts

    def copy(self, g):
        """ Copy the current GenomeBase to 'g'

      :param g: the destination genome      

      """
        g.score = self.score
        g.fitness = self.fitness
        g.evaluator = self.evaluator
        g.initializator = self.initializator
        g.mutator = self.mutator
        g.crossover = self.crossover
        g.allSlots = self.allSlots[:]
        g.internalParams = self.internalParams.copy()

    def clone(self):
        """ Clone this GenomeBase

      :rtype: the clone genome   

      """
        newcopy = GenomeBase()
        self.copy(newcopy)
        return newcopy