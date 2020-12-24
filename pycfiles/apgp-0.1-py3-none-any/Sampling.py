# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/Sampling.py
# Compiled at: 2013-10-11 16:14:20
from apgl.util.Parameter import Parameter
import numpy

class Sampling(object):
    """
    An class to sample a set of examples in different ways. 
    """

    def __init__(self):
        pass

    @staticmethod
    def crossValidation(folds, numExamples):
        """
        Returns a list of tuples (trainIndices, testIndices) using k-fold cross
        validation. The dataset is split into approximately folds contiguous 
        subsamples.  

        :param folds: The number of cross validation folds.
        :type folds: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`
        """
        Parameter.checkInt(folds, 1, numExamples)
        Parameter.checkInt(numExamples, 2, float('inf'))
        foldSize = float(numExamples) / folds
        indexList = []
        for i in range(0, folds):
            testIndices = numpy.arange(int(foldSize * i), int(foldSize * (i + 1)))
            trainIndices = numpy.setdiff1d(numpy.arange(0, numExamples), numpy.array(testIndices))
            indexList.append((trainIndices, testIndices))

        return indexList

    @staticmethod
    def randCrossValidation(folds, numExamples, dtype=numpy.int32):
        """
        Returns a list of tuples (trainIndices, testIndices) using k-fold cross
        validation. In this case we randomise the indices and then split into 
        folds. 

        :param folds: The number of cross validation folds.
        :type folds: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`
        """
        Parameter.checkInt(folds, 1, numExamples)
        Parameter.checkInt(numExamples, 2, float('inf'))
        foldSize = float(numExamples) / folds
        indexList = []
        inds = numpy.array(numpy.random.permutation(numExamples), dtype)
        for i in range(0, folds):
            testIndices = inds[int(foldSize * i):int(foldSize * (i + 1))]
            trainIndices = numpy.setdiff1d(numpy.arange(0, numExamples), testIndices)
            indexList.append((trainIndices, testIndices))

        return indexList

    @staticmethod
    def bootstrap(repetitions, numExamples):
        """
        Perform 0.632 bootstrap in whcih we take a sample with replacement from
        the dataset of size numExamples. The examples not present in the training
        set are used to form the test set. Returns a list of tuples of the form
        (trainIndices, testIndices).

        :param repetitions: The number of repetitions of bootstrap to perform.
        :type repetitions: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`

        """
        Parameter.checkInt(numExamples, 2, float('inf'))
        Parameter.checkInt(repetitions, 1, float('inf'))
        inds = []
        for i in range(repetitions):
            trainInds = numpy.random.randint(numExamples, size=numExamples)
            testInds = numpy.setdiff1d(numpy.arange(numExamples), numpy.unique(trainInds))
            inds.append((trainInds, testInds))

        return inds

    @staticmethod
    def bootstrap2(repetitions, numExamples):
        """
        Perform 0.632 bootstrap in whcih we take a sample with replacement from
        the dataset of size numExamples. The examples not present in the training
        set are used to form the test set. We oversample the test set to include
        0.368 of the examples from the training set. Returns a list of tuples of the form
        (trainIndices, testIndices).

        :param repetitions: The number of repetitions of bootstrap to perform.
        :type repetitions: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`

        """
        Parameter.checkInt(numExamples, 2, float('inf'))
        Parameter.checkInt(repetitions, 1, float('inf'))
        inds = []
        for i in range(repetitions):
            trainInds = numpy.random.randint(numExamples, size=numExamples)
            testInds = numpy.setdiff1d(numpy.arange(numExamples), numpy.unique(trainInds))
            inds.append((trainInds, testInds))

        return inds

    @staticmethod
    def shuffleSplit(repetitions, numExamples, trainProportion=None):
        """
        Random permutation cross-validation iterator. The training set is sampled
        without replacement and of size (repetitions-1)/repetitions of the examples,
        and the test set represents the remaining examples. Each repetition is
        sampled independently.

        :param repetitions: The number of repetitions to perform.
        :type repetitions: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`

        :param trainProp: The size of the training set relative to numExamples, between 0 and 1 or None to use (repetitions-1)/repetitions
        :type trainProp: :class:`int`
        """
        Parameter.checkInt(numExamples, 2, float('inf'))
        Parameter.checkInt(repetitions, 1, float('inf'))
        if trainProportion != None:
            Parameter.checkFloat(trainProportion, 0.0, 1.0)
        if trainProportion == None:
            trainSize = int((repetitions - 1) * numExamples / repetitions)
        else:
            trainSize = int(trainProportion * numExamples)
        idx = []
        for i in range(repetitions):
            inds = numpy.random.permutation(numExamples)
            trainInds = inds[0:trainSize]
            testInds = inds[trainSize:]
            idx.append((trainInds, testInds))

        return idx

    @staticmethod
    def repCrossValidation(folds, numExamples, repetitions, seed=21):
        """
        Returns a list of tuples (trainIndices, testIndices) using k-fold cross
        validation repeated m times. 

        :param folds: The number of cross validation folds.
        :type folds: :class:`int`

        :param numExamples: The number of examples.
        :type numExamples: :class:`int`
        
        :param repetitions: The number of repetitions.
        :type repetitions: :class:`int`
        """
        Parameter.checkInt(folds, 1, numExamples)
        Parameter.checkInt(numExamples, 2, float('inf'))
        Parameter.checkInt(repetitions, 1, float('inf'))
        foldSize = float(numExamples) / folds
        indexList = []
        numpy.random.seed(seed)
        for j in range(repetitions):
            permInds = numpy.random.permutation(numExamples)
            for i in range(folds):
                testIndices = numpy.arange(int(foldSize * i), int(foldSize * (i + 1)))
                trainIndices = numpy.setdiff1d(numpy.arange(0, numExamples), numpy.array(testIndices))
                indexList.append((permInds[trainIndices], permInds[testIndices]))

        return indexList