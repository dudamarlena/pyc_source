# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gevolver/pbge/individual.py
# Compiled at: 2007-07-24 13:41:18
"""
GE Individuals
"""
import copy
from twisted.internet.task import coiterate
from twisted.internet import defer

class ConditionError(Exception):
    __module__ = __name__


class Termiterator(object):
    """
    """
    __module__ = __name__

    def __init__(self, sentence, inputState):
        self.remnant = copy.copy(sentence)
        self.state = copy.copy(inputState)

    def __iter__(self):
        """
        """
        return self

    def next(self):
        """
        Running the C{value} method on the terminal can't take too long or it
        will mess up the coiteration.
        """
        if self.remnant:
            terminal = self.remnant.pop(0)
            terminal.value(self.state)
        else:
            raise StopIteration

    def getState(self):
        """
        """
        return self.state


class Individual(object):
    """
    I manage a set of production rules B{P} and a terminal set B{T}, applying
    them to supplied genomes and evaluating the resulting individual program.
    """
    __module__ = __name__

    def evaluate(self, sentence, inputStates, errorFunction=None, fitnessFunction=None):
        """
        Evaluates the program defined by the supplied I{sentence} of terminals
        and a sequence of I{inputStates} supplied as args, and either an
        I{errorFunction} or a I{fitnessFunction} supplied as a keyword.
        
        Returns a deferred that fires with a numerical value reflecting the
        total fitness for all the input states supplied.
        """

        def meanError(null):
            inverseErrors = [ 1.0 / abs(x) for x in results if x != 0 ]
            return len(inverseErrors) / sum(inverseErrors)

        def meanFitness(null):
            return sum(abs(results)) / len(results)

        @defer.deferredGenerator
        def function():
            for inputState in inputStates:
                wfd = defer.waitForDeferred(self.run(sentence, state))
                yield wfd
                resultState = wfd.getResult()
                results.append(f(inputState, resultState))

        results = []
        if errorFunction is not None and fitnessFunction is not None:
            raise ConditionError('Conflicting evaluation function specification')
        elif callable(errorFunction):
            f = errorFunction
            callback = meanError
        elif callable(fitnessFunction):
            f = fitnessFunction
            callback = meanFitness
        else:
            raise ConditionError('No error or fitness function supplied')
        return function().addCallback(callback)

    def run(self, sentence, inputState):
        """
        Runs the program defined by the supplied I{sentence} of terminals,
        giving it a copy of the supplied I{inputState} to access and
        modify.

        Returns a deferred that fires when the end of the terminal sentence is
        reached. At that point, the program will have finished running and
        making modifications to its copy of the state, a reference to which the
        deferred supplies as the argument to its callback function.
        """
        ti = Termiterator(sentence, inputState)
        return coiterate(ti).addCallback(ti.getState)