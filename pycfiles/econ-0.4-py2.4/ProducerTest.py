# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/ProducerTest.py
# Compiled at: 2007-04-18 06:57:54
import unittest, random, DemandFunction, Producer

class ProducerTest(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.dfConstant = 5.0
        self.dfSlope = -1.0
        self.df = DemandFunction.getLinearDemandFunction(self.dfConstant, self.dfSlope)
        self.marginalCost = 0.0

        def costFunction(quantity):
            return quantity * self.marginalCost

        self.cf = costFunction
        self.producer = Producer.Producer(self.df, self.cf)

    def testGetProfitFunction(self):

        def profitFunction(price):
            return max(0, self.dfConstant * price + price ** 2 * self.dfSlope)

        maxPrice = self.producer.MAXPRICE
        numsteps = 30.0
        price = 0.0
        while price < maxPrice:
            price += maxPrice / numsteps
            self.assertAlmostEquals(self.producer.profitFunction(price), profitFunction(price))

    def testGetMonopolyPrice(self):
        self.marginalCost = 0.0
        expectedPrice = -self.dfConstant / (2 * self.dfSlope)
        self.assertEqual(expectedPrice, self.producer.getMonopolyPrice())

    def testGetMonopolyPrice2(self):
        self.marginalCost = 1.0
        expectedPrice = (self.dfConstant - self.dfSlope) / (-2 * self.dfSlope)
        self.assertEqual(expectedPrice, self.producer.getMonopolyPrice())

    def testGetCompetitivePrice(self):
        """
        Constant marginal cost so very easy
        """
        self.marginalCost = 0.0
        expectedPrice = self.marginalCost
        self.assertEquals(expectedPrice, self.producer.getCompetitivePrice())

    def testGetCompetitivePrice2(self):
        """
        Constant marginal cost so very easy
        """
        self.marginalCost = self.dfConstant * random.random()
        expectedPrice = self.marginalCost
        self.assertAlmostEquals(expectedPrice, self.producer.getCompetitivePrice())

    def testGetMonopolyDeadweightCosts(self):
        self.marginalCost = self.dfConstant * random.random()
        monopolyPrice = self.producer.getMonopolyPrice()
        monopolyQuantity = self.producer.demandFunction(monopolyPrice)
        competiveQuantity = self.producer.demandFunction(self.marginalCost)
        deadweightCosts = 0.5 * (monopolyPrice - self.marginalCost) * (competiveQuantity - monopolyQuantity)
        self.assertAlmostEquals(deadweightCosts, self.producer.getMonopolyDeadweightCosts())