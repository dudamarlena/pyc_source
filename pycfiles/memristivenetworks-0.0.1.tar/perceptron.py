# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: memristivenetworks/perceptron.py
# Compiled at: 2018-01-15 05:48:26
from __future__ import unicode_literals
import numpy as np, matplotlib.pyplot as plt, pylab
from csv import reader

class Data:
    """This class reads the input and output data to train the network,
    which are placed in a .csv file or creates example data if a file is
    missing
    """

    def __init__(self, filename=None, npoints=20):
        """INITIALIZES THE OBJECT

         Keyword arguments:
         filename -- name of the file with data to classify (default None)
         npoints -- number of points to randomly generate weight/height data
         if there is no input file (default 20)
         """
        self.dataset = []
        self.training_data = []
        self.test_data = []
        if filename:
            self.keys = dict()
            with open(filename, b'r') as (file):
                csv_reader = reader(file)
                for row in csv_reader:
                    if not row:
                        continue
                    self.dataset.append(row)

            for i in range(len(self.dataset[0]) - 1):
                for row in self.dataset:
                    row[i] = float(row[i].strip())

            column = len(self.dataset[0]) - 1
            class_values = [ row[column] for row in self.dataset ]
            unique = set(class_values)
            for i, value in enumerate(unique):
                self.keys[value] = i

            for row in self.dataset:
                row[column] = self.keys[row[column]]

            print b'Dictionary:', self.keys
            for i in range(len(self.dataset)):
                self.dataset[i] = [np.array(self.dataset[i][:-1]),
                 np.array([float(self.dataset[i][(-1)])])]

        else:
            BMI = 25
            for i in range(npoints):
                height = np.random.uniform(1.6, 2.0)
                group = np.random.randint(2)
                if group:
                    arg = BMI * height * height / 100 + 0.05
                    weight = np.random.uniform(arg, 1.2)
                if not group:
                    arg = BMI * height * height / 100 - 0.05
                    weight = np.random.uniform(0.4, arg)
                self.dataset.append([
                 np.array([height, weight]), np.array([float(group)])])

    def folds(self, kfolds):
        """DIVIDES THE DATA INTO TRAINING AND TEST SETS

        Keyword arguments:
        kfolds -- number of parts to devide the data into
        """
        i = 0
        indexes = []
        while i < int((1.0 - 1.0 / kfolds) * len(self.dataset)):
            k = np.random.randint(len(self.dataset))
            if k not in indexes:
                indexes.append(k)
                self.training_data.append(self.dataset[k])
                i += 1

        len_training_data = len(self.training_data)
        compare_data = [ self.training_data[i][j].tolist() for i in range(len_training_data) for j in range(len(self.training_data[i]))
                       ]
        i = 0
        while i < int(1.0 / kfolds * len(self.dataset)):
            k = np.random.randint(len(self.dataset))
            if self.dataset[k][0].tolist() not in compare_data:
                self.test_data.append(self.dataset[k])
                i += 1


class SetReset:
    """This class gives the value of the memristor conductivity change as a
    function of conductivity, which are placed in a .csv file.
    """

    def __init__(self, fileName, norm=1000.0):
        """INITIALIZES THE OBJECT

        Keyword arguments:
        fileName -- name of the deltaG as a function of G file in .csv format
        norm -- normalization factor (default 1E3)
        """
        input = open(fileName, b'r')
        s = input.readlines()
        self.xDistribution = []
        self.yDistribution = []
        for line in s:
            pair = line.split(b',')
            self.xDistribution.append(norm * float(pair[0]))
            self.yDistribution.append(norm * float(pair[1]))

        input.close()

    def deltaG(self, xValue):
        """INTERPOLATES THE DATA

        Keyword arguments:
        xValue -- conductance value

        Return: interpolated conductivity change
        """
        return pylab.interp(xValue, self.xDistribution, self.yDistribution)


class Perceptron:
    """
    This class defines the perceptron, writes and reads the associations.
    For more information about the utilization consult the README file.
    """

    def __init__(self, NA=2, NB=1, bias=1, setFileName=b'set.csv', resetFileName=b'reset.csv'):
        """INITIALIZES THE NETWORK

        Keyword arguments:
        NA -- number of input neurons (default 2)
        NB -- number of output neurons (default 1)
        bias -- bias value (default 1)
        setFileName -- name of the file for conductivity increase
                       (default 'set.csv')
        resetFileName -- name of the file for conductivity decrease
                         (default 'reset.csv')
        """
        self.A_memristors = np.random.rand(NA + 1, NB)
        self.B_memristors = np.random.rand(NA + 1, NB)
        self.Ahist = []
        self.Bhist = []
        self.NA = NA
        self.NB = NB
        self.bias = bias
        self.errors = []
        self.errorshist = []
        self.set = SetReset(setFileName)
        self.reset = SetReset(resetFileName)
        self.VA = [[0]] * (NA + 1)
        self.VB = [[0]] * (NA + 1)
        self.Ahist.append(np.copy(self.A_memristors))
        self.Bhist.append(np.copy(self.B_memristors))

    def train(self, iteration, l_rate, voltSet=-1.7, voltReset=2.6):
        """TRAINS THE NETWORK ON 1 PATTERN (by changing the weights if needed)

        Keyword arguments:
        iteration -- input data to train the network
                     (combination of input and expected output)
        l_rate -- learning rate
        Vset -- voltage used for Set
        Vreset -- voltage used for Reset
        """
        inputs = np.copy(iteration)
        inputs[0] = np.lib.pad(inputs[0], (0, 1), b'constant', constant_values=self.bias)

        def unit_step(x):
            if x <= 0:
                return 0
            return 1

        result = []
        error = np.zeros(self.NB)
        for i in range(self.NB):
            result.append(np.dot(inputs[0], self.A_memristors.T[i] - self.B_memristors.T[i]))
            error[i] = inputs[1][i] - unit_step(result[(-1)])
            er = error[i]
            self.errors.append(er)
            for j in range(self.NA + 1):
                idealA = self.A_memristors[j][i] + l_rate * er * inputs[0][j] / 2.0
                idealB = self.B_memristors[j][i] - l_rate * er * inputs[0][j] / 2.0
                if er > 0:
                    cc = 1
                    while self.A_memristors[j][i] < idealA and cc < 1000.0:
                        dgA = abs(self.set.deltaG(self.A_memristors[j][i]))
                        self.A_memristors[j][i] += dgA
                        self.VA[j].append(voltSet)
                        cc += 1

                    cc = 1
                    while self.B_memristors[j][i] > idealB and cc < 1000.0:
                        dgB = abs(self.reset.deltaG(self.B_memristors[j][i]))
                        self.B_memristors[j][i] -= dgB
                        self.VB[j].append(voltReset)
                        cc += 1

                if er < 0:
                    cc = 1
                    while self.A_memristors[j][i] > idealA and cc < 1000.0:
                        dgA = abs(self.reset.deltaG(self.A_memristors[j][i]))
                        self.A_memristors[j][i] -= dgA
                        self.VA[j].append(voltReset)
                        cc += 1

                    cc = 1
                    while self.B_memristors[j][i] < idealB and cc < 1000.0:
                        dgB = abs(self.set.deltaG(self.B_memristors[j][i]))
                        self.B_memristors[j][i] += dgB
                        self.VB[j].append(voltSet)
                        cc += 1

                if self.A_memristors[j][i] > 1:
                    self.A_memristors[j][i] = 1
                if self.A_memristors[j][i] < 0:
                    self.A_memristors[j][i] = 0
                if self.B_memristors[j][i] > 1:
                    self.B_memristors[j][i] = 1
                if self.B_memristors[j][i] < 0:
                    self.B_memristors[j][i] = 0

        self.Ahist.append(np.copy(self.A_memristors))
        self.Bhist.append(np.copy(self.B_memristors))

    def trainMany(self, training_data, numberIterations, l_rate):
        """TRAINS THE NETWORK ON MULTIPLE PATTERNS

        Keyword arguments:
        training_data -- list of input patterns with known output
        numberIterations -- epochs
        l_rate -- learning rate
        """
        for i in range(numberIterations):
            self.errors = []
            for j in range(len(training_data)):
                self.train(training_data[j], l_rate, voltSet=-1.7, voltReset=2.6)

            self.errorshist.append(np.copy(self.errors))
            print b'>epoch = %d, lrate = %.3f, error = %d' % (
             i + 1, l_rate, sum(map(abs, self.errorshist[i])))

    def read(self, pattern):
        """READS THE OUTPUT OF A PATTERN

        Keyword arguments:
        pattern -- input pattern to compute + expected value:
                   e.g. [np.array([1,1]),np.array([1])]

        Return: read values
        """
        pattern = np.lib.pad(pattern, (0, 1), b'constant', constant_values=self.bias)

        def unit_step(x):
            if x <= 0:
                return 0
            return 1

        result = []
        for i in range(self.NB):
            arg = self.A_memristors.T[i] - self.B_memristors.T[i]
            result.append(unit_step(np.dot(pattern, arg)))

        return np.array(result)

    def readMany(self, patterns):
        """READS THE OUTPUT OF MANY PATTERNS

        Keyword arguments:
        patterns -- input patterns to compute + expected values
        """
        self.errors = []
        for pattern in patterns:
            self.errors.append(sum(map(abs, self.read(pattern[0]) - pattern[1])))

        arg = (len(patterns) - sum(map(abs, self.errors))) / len(patterns)
        print b'Correct tested patterns:', arg * 100, b'%'

    def eq_hyperplane(self, x):
        """DEFINES THE HYPERLANE IN 2D

        Keyword arguments:
        x -- range in the input 1 space

        Return: hyperplane y values
        """
        m = -(self.A_memristors[0] - self.B_memristors[0]) / (self.A_memristors[1] - self.B_memristors[1])
        b = -(self.A_memristors[2] - self.B_memristors[2]) / (self.A_memristors[1] - self.B_memristors[1])
        return m * x + b


if __name__ == b'__main__':
    l_rate = 0.1
    n_epoch = 25
    kfolds = 5
    data = Data()
    data.folds(kfolds)
    print b'Training points:', len(data.training_data)
    print b'Testing points:', len(data.test_data)
    network = Perceptron()
    network.trainMany(data.training_data, n_epoch, l_rate)
    network.readMany(data.test_data)
    plt.figure(b'Experimental data')
    plt.plot(network.set.xDistribution, network.set.yDistribution, b'.-g', label=b'Set')
    plt.plot(network.reset.xDistribution, network.reset.yDistribution, b'x-r', label=b'Reset')
    plt.xlabel(b'G (S)')
    plt.ylabel(b'$\\Delta$G (S)')
    plt.xlim([0, 1])
    plt.ticklabel_format(axis=b'y', style=b'sci', scilimits=(0, 0))
    plt.legend()
    if len(data.dataset[0][0]) == 2:
        plt.figure(b'BMI')
        plt.xlabel(b'height (m)')
        plt.ylabel(b'weight (kg)')
        height_normal_training = [ i[0][0] for i in data.training_data if not i[1]
                                 ]
        height_over_training = [ i[0][0] for i in data.training_data if i[1] ]
        weight_normal_training = [ i[0][1] * 100 for i in data.training_data if not i[1] ]
        weight_over_training = [ i[0][1] * 100 for i in data.training_data if i[1] ]
        height_normal_test = [ i[0][0] for i in data.test_data if not i[1] ]
        height_over_test = [ i[0][0] for i in data.test_data if i[1] ]
        weight_normal_test = [ i[0][1] * 100 for i in data.test_data if not i[1] ]
        weight_over_test = [ i[0][1] * 100 for i in data.test_data if i[1] ]
        plt.plot(height_normal_training, weight_normal_training, b'ob', label=b'normal weight (training)')
        plt.plot(height_over_training, weight_over_training, b'sr', label=b'overweight (training)')
        plt.plot(height_normal_test, weight_normal_test, b'ob', fillstyle=b'none', label=b'normal weight (test)')
        plt.plot(height_over_test, weight_over_test, b'sr', fillstyle=b'none', label=b'overweight (test)')
        plt.xlim(min([ i[0][0] for i in data.training_data ]) - 0.05, max([ i[0][0] for i in data.training_data ]) + 0.05)
        plt.ylim(min([ i[0][1] * 100 for i in data.training_data ]) - 10, max([ i[0][1] * 100 for i in data.training_data ]) + 10)
        plt.legend(loc=b'upper left')
        plt.plot(np.arange(1.55, 2.2, 0.2), network.eq_hyperplane(np.arange(1.55, 2.2, 0.2)) * 100, b'-k')
    plt.figure(b'Error')
    plt.xlabel(b'epoch')
    plt.ylabel(b'error sum')
    plt.xlim([1, n_epoch + 1])
    plt.plot(np.arange(1, n_epoch + 1), [ sum(map(abs, i)) for i in network.errorshist ], b'.-b')
    if len(data.dataset[0][0]) == 2:
        plt.figure(b'weights')
        plt.xlabel(b'iteration')
        for i in range(len(network.Ahist)):
            for j in range(network.NA + 1):
                plt.subplot(((network.NA + 1) * 2 + 1) * 100 + 10 + 2 * j + 1)
                plt.plot(i, network.Ahist[i][j], b'.r')
                plt.ylabel(b'wA' + str(j + 1))
                plt.ylim([0, 1])
                plt.xticks([])
                plt.yticks(np.arange(0, 1.25, 0.25))
                if j == network.NA:
                    plt.ylabel(b'wAb')
                plt.subplot(((network.NA + 1) * 2 + 1) * 100 + 10 + 2 * j + 2)
                plt.plot(i, network.Bhist[i][j], b'.b')
                plt.ylabel(b'wB' + str(j + 1))
                plt.ylim([0, 1])
                plt.xticks([])
                plt.yticks(np.arange(0, 1.25, 0.25))
                if j == network.NA:
                    plt.ylabel(b'wBb')

        plt.subplot((len(network.Ahist[0]) * 2 + 1) * 100 + 10 + (len(network.Ahist[0]) * 2 + 1))
        plt.ylabel(b'error')
        plt.xlabel(b'iteration')
        plt.ylim([-1, 1])
        plt.yticks([-1, 0, 1])
        plt.xlim([0, n_epoch * len(data.training_data)])
        cc = 1
        for i in range(n_epoch):
            for j in range(len(data.training_data)):
                plt.bar(cc - 1, network.errorshist[i][j])
                cc += 1

    if len(data.dataset[0][0]) == 2:
        plt.figure(b'pulses')
        for i in range(network.NA + 1):
            plt.subplot((network.NA + 1) * 2 * 100 + 10 + 2 * i + 1)
            plt.plot(np.arange(len(network.VA[i])), network.VA[i], b'r')
            plt.ylabel(b'VA' + str(i + 1))
            plt.xticks([])
            plt.yticks([min(network.VA[i]), 0, max(network.VA[i])])
            if i == network.NA:
                plt.ylabel(b'VAb')
            plt.subplot(len(network.Ahist[0]) * 2 * 100 + 10 + 2 * i + 2)
            plt.plot(np.arange(len(network.VB[i])), network.VB[i], b'b')
            plt.ylabel(b'VB' + str(i + 1))
            if not i == network.NA:
                plt.xticks([])
            plt.yticks([min(network.VA[i]), 0, max(network.VA[i])])
            if i == network.NA:
                plt.ylabel(b'VBb')
            if i == network.NA:
                plt.xlabel(b'pulse number')

    plt.show()