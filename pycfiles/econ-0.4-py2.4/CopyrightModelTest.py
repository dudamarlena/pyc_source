# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/CopyrightModelTest.py
# Compiled at: 2007-04-18 06:57:54
import unittest, random, math
from CopyrightModel import *
from DiscountRate import *

class CopyrightIncomeTest(unittest.TestCase):
    __module__ = __name__

    def testCopyrightIncomeModelLinear(self):
        a1 = 1
        incModel = CopyrightIncomeModelLinear()
        incModel.constant = a1
        self.assertEquals(incModel.getIncome(random.randint(0, 2000)), a1)

    def testCopyrightIncomeModelQuadratic(self):
        b = random.randint(0, 100)
        quad1 = CopyrightIncomeModelQuadratic([0, b, -1])
        self.assertAlmostEqual(0, quad1.getIncome(b))

    def testExponentialModel(self):
        exponentialModel = CopyrightIncomeModelExponential()
        self.assertAlmostEqual(0.00673794699909, exponentialModel.getIncome(5))

    def testHybridModel(self):
        linearModel = CopyrightIncomeModelLinear()
        exponentialModel = CopyrightIncomeModelExponential()
        incomeModel = CopyrightIncomeModelHybrid()
        self.assertEqual(0, incomeModel.getIncome(10))
        incomeModel.getModelList().append((1, linearModel))
        incomeModel.getModelList().append((5, exponentialModel))
        smallNumber = 0.2
        largeNumber = 100
        self.assertNotEqual(1, incomeModel.getIncome(smallNumber))
        self.assertAlmostEqual(1, incomeModel.getIncome(largeNumber))

    def testSummary(self):
        drc1 = DiscountRateConstant()
        dr1 = 1 / 1.02
        drc1.setUnitDiscountRate(dr1)
        a1 = 1
        incModel = CopyrightIncomeModelLinear()
        incModel.constant = a1

        def linearSolution(constant, discount, period):
            return (1 - pow(discount, period)) / (1 - discount)

        def linearSolutionTotal(constant, discount):
            return 1 / (1 - discount)

        def numPeriods(proportion, discount):
            """
            Get number of periods necessary to obtain proportion of total
            **possible** income.
            proportion in [0,1)
            """
            return math.log(1 - proportion) / math.log(discount)

        def proportionOfTotalIncome(discount, numPeriods):
            return 1 - pow(discount, numPeriods)

        cis1 = CopyrightIncomeSummary(incModel, drc1)
        cis1.calculate()
        self.assertAlmostEqual(cis1.totalPossibleIncome, linearSolutionTotal(a1, dr1), 1)
        ran2 = random.randint(0, 1500)
        self.assertAlmostEqual(cis1.getProportionOfTotalPossibleIncome(ran2), proportionOfTotalIncome(dr1, ran2), 1)