# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parang/bpnn.py
# Compiled at: 2009-08-22 22:50:09
"""Back-Propagation Neural Networks
    Copyright (C) 2007-2008  Neil Schemenauer and Eric Wald
    
    This software may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this software for
    commercial purposes without permission from the authors is prohibited.
"""
import math, random
from parlance.config import VerboseObject
random.seed()

def rand(a, b):
    return (b - a) * random.random() + a


def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)

    return m


def sigmoid(x):
    return math.tanh(x)


def dsigmoid(y):
    return 1.0 - y * y


class NN(VerboseObject):

    def __init__(self, ni, nh, no, wi=None, wo=None):
        self.__super.__init__()
        self.ni = ni + 1
        self.nh = nh
        self.no = no
        self.ai = [
         1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no
        if wi and wo:
            self.wi = wi
            self.wo = wo
        else:
            self.wi = makeMatrix(self.ni, self.nh)
            self.wo = makeMatrix(self.nh, self.no)
            for j in range(self.nh):
                if not j % 10:
                    self.log_debug(11, '%d nodes done', j)
                for i in range(self.ni):
                    self.wi[i][j] = rand(-2.0, 2.0)

                for k in range(self.no):
                    self.wo[j][k] = rand(-2.0, 2.0)

        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni - 1:
            raise ValueError('wrong number of inputs')
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum += self.ai[i] * self.wi[i][j]

            self.ah[j] = sigmoid(sum)

        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += self.ah[j] * self.wo[j][k]

            self.ao[k] = sigmoid(sum)

        return self.ao[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')
        output_deltas = [
         0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        hidden_deltas = [
         0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k] * self.wo[j][k]

            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change + M * self.co[j][k]
                self.co[j][k] = change

        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] += N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        error = 0.0
        for k in range(len(targets)):
            error += 0.5 * (targets[k] - self.ao[k]) ** 2

        return error

    def test(self, patterns):
        for p in patterns:
            print p[0], '->', self.update(p[0])

    def weights(self):
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]

        print
        print 'Output weights:'
        for j in range(self.nh):
            print self.wo[j]

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error += self.backPropagate(targets, N, M)

            if i % 100 == 0:
                self.log_debug(11, 'error %-14f', error)

    def learn(self, inputs, targets, iterations=1000, N=0.5, M=0.1):
        """ Trains the network with a single pattern.
            Slightly more efficient than train().
        """
        self.update(inputs)
        for i in xrange(iterations):
            error = self.backPropagate(targets, N, M)
            if i % 100 == 0:
                self.log_debug(11, 'Training... epsilon %-14f', error)


def demo():
    pat = [
     [
      [
       0, 0], [0]],
     [
      [
       0, 1], [1]],
     [
      [
       1, 0], [1]],
     [
      [
       1, 1], [0]]]
    n = NN(2, 2, 1)
    n.train(pat)
    n.test(pat)
    n.weights()


if __name__ == '__main__':
    demo()