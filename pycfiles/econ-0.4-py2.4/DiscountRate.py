# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/DiscountRate.py
# Compiled at: 2007-04-18 06:57:54
import econ.log
logger = econ.log.get_logger()

class DiscountRate(object):
    """
    Interface class for model/empirical discount rates
    """
    __module__ = __name__

    def getDiscount(self, receiveTimePoint, evaluationTimePoint=0):
        """
        Get rate of return between evaluationTimePoint and receiveTimePoint.
        That is value x s.t. 1 unit at receiveTimePoint yields x at evaluation time point
         
        For standard present value evaluationTimePoint = 0 and receiveTimePoint is in future
        For standard cumulation, e.g. interest rates, evaluationTimePoint follows receiveTimePoint
        """
        raise 'Abstract Method'

    def getReturn(self, evaluationTimePoint, receiveTimePoint=0):
        return 1 / self.getDiscount(evaluationTimePoint, receiveTimePoint)


class DiscountRateConstant(DiscountRate):
    __module__ = __name__
    discountRate = 1
    assumeRateAboveOneIsInterestRate = True

    def __init__(self, discountRate=1):
        self.setUnitDiscountRate(discountRate)

    def getDiscount(self, receiveTimePoint, evaluationTimePoint=0):
        logger.debug('DiscountRateConstant.getReturnRate(). evalTimePoint = ' + str(evaluationTimePoint) + ' receiveTimePoint = ' + str(receiveTimePoint))
        logger.debug('(Unit) return rate: ' + str(self.discountRate))
        return pow(self.discountRate, receiveTimePoint - evaluationTimePoint)

    def setUnitDiscountRate(self, discountRate):
        self.discountRate = self.__processRateOnSetting(discountRate)

    def getUnitDiscountRate(self):
        return self.discountRate

    def __processRateOnSetting(self, rate):
        if self.assumeRateAboveOneIsInterestRate and rate > 1:
            return 1.0 / rate
        else:
            return rate


class DiscountRateHistorical(DiscountRate):
    __module__ = __name__

    def __init__(self, timeSeries):
        self._timeSeries = timeSeries

    def getDiscount(self, receiveTimePoint, evaluationTimePoint=0):
        indexReceive = self._timeSeries.getValue(receiveTimePoint)
        indexEval = self._timeSeries.getValue(evaluationTimePoint)
        return indexReceive / indexEval