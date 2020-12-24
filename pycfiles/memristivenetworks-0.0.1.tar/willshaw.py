# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: memristivenetworks/willshaw.py
# Compiled at: 2018-01-14 18:20:09
from __future__ import unicode_literals
import numpy as np, random, matplotlib.pyplot as plt

class Willshaw:
    """This class defines the Willshaw network, writes and reads the
    associations, and executes an example. For more information about the
    utilization consult the README file.
    """

    def __init__(self, NB=128, NA=128, MB=7, MA=7):
        """INITIALIZATION OF THE OBJECT

        Keyword arguments:
        NB -- number of neurons of population B - input (default 128)
        NA -- number of neurons of population A - output (default 128)
        MB -- number of units of each patten for population B (default 7)
        MA -- number of units of each patten for population A (default 7)
        """
        self.network = np.zeros((NB, NA))
        self.associations = {b'B_neurons': [], b'A_neurons': []}
        self.MB = MB
        self.MA = MA
        self.NB = NB
        self.NA = NA

    def write(self, b_neuronList, a_neuronList):
        """ TRAINING PROCESS: WRITES AN ASSOCIATION IN THE NETWORK (MATRIX)

        Keyword arguments:
        b_neuronList -- index list of the neurons of population B taking part
                        in the association
        a_neuronList -- index list of the neurons of population A taking part
                        in the association
        """
        cond_1 = len(b_neuronList) == self.MB
        cond_2 = len(a_neuronList) == self.MA
        cond_3 = sorted(b_neuronList) not in self.associations[b'B_neurons']
        if cond_1 and cond_2 and cond_3:
            self.associations[b'B_neurons'].append(sorted(b_neuronList))
            self.associations[b'A_neurons'].append(sorted(a_neuronList))
            for i in range(self.MB):
                for j in range(self.MA):
                    ind = self.associations[b'A_neurons'][(-1)][j]
                    self.network[self.associations[b'B_neurons'][(-1)][i]][ind] = 1

        else:
            print b'invalid association'

    def writeMany(self, numberAssociations):
        """WRITES SEVERAL RANDOM ASSOCIATIONS IN THE MEMRISTIVE MATRIX

        Keyword arguments:
        numberAssociations -- number of random associations to be written

        Return: 2 lists of neurons in the associations
        """
        list_B_neurons = []
        list_A_neurons = []
        i = 0
        while i < numberAssociations:
            b_neuronList = sorted(random.sample(range(self.NB), self.MB))
            a_neuronList = sorted(random.sample(range(self.NA), self.MA))
            if b_neuronList not in list_B_neurons:
                list_B_neurons.append(b_neuronList)
                list_A_neurons.append(a_neuronList)
                i += 1
            else:
                print b'invalid association'

        for i in range(numberAssociations):
            self.write(list_B_neurons[i], list_A_neurons[i])

        return (
         list_B_neurons, list_A_neurons)

    def read(self, b_neuronList, threshold):
        """READS THE OUTPUT IN POPULATION B FOR AN INPUT GIVEN FOR POPULATON A

        Keyword arguments:
        b_neuronList -- index list for population B for which an action is
        given threshold -- minimum value for which we have a state 1 in neurons
        of population B

        Return: index list for population A
        """
        b_neuronList = sorted(b_neuronList)
        a_neuronList = []
        for i in range(self.NA):
            sum1 = 0.0
            for j in b_neuronList:
                sum1 += self.network[j][i]
                if sum1 >= threshold:
                    a_neuronList.append(i)

        a_neuronList = sorted(a_neuronList)
        return a_neuronList

    def count(self, threshold=None):
        """COUNTS HOW MANY PATTERNS ARE STILL OK

        Keyword arguments:
        threshold -- minimum value for which we have a state 1 in neurons of
                     population A

        Return: the number and average number of associations that are
                retrieved correctly
        """
        sum1 = 0
        errors = []
        if threshold is None:
            threshold = self.MB
        for i in range(len(self.associations[b'B_neurons'])):
            list_error = sorted(self.read(self.associations[b'B_neurons'][i], threshold))
            error = [ x for x in list_error if x not in sorted(self.associations[b'A_neurons'][i])
                    ]
            if len(error) <= 1:
                sum1 += 1
            else:
                print b'error =', len(error)
            errors += [len(error)]

        return (
         sum1, np.average(errors))


if __name__ == b'__main__':
    numberSimulations = 1
    PAmax = 250
    a = []
    b = []
    average_capacity = []
    for j in range(numberSimulations):
        print b'>>>Simulation:', j, b'/', numberSimulations
        x = []
        y = []
        capacity = []
        for i in range(PAmax):
            print b'#Patterns =', i
            network = Willshaw()
            beta, alfa = network.writeMany(numberAssociations=i)
            x.append(i)
            out = network.count()
            y.append(out[0])
            capacity.append(out[1])

        x = np.array(x)
        y = np.array(y)
        capacity = np.array(capacity)
        a.append(x)
        b.append(y)
        average_capacity.append(capacity)

    x = sum(a) / float(numberSimulations)
    y = sum(b) / float(numberSimulations)
    capacity = sum(average_capacity) / float(numberSimulations)
    deviation = map(lambda x: np.std(x), zip(*b))
    plt.figure(b'correct patterns')
    plt.fill_between(x, y - np.array(deviation), y + np.array(deviation), facecolor=b'grey')
    plt.plot(x, y)
    plt.xlabel(b'number of written patterns')
    plt.ylabel(b'number of correctly retrieved patterns')
    plt.figure(b'average error')
    plt.bar(x, capacity)
    plt.plot(x, np.ones(PAmax))
    plt.xlabel(b'number of written patterns')
    plt.ylabel(b'average number of incorrect units in the retrieved patterns')
    plt.show()