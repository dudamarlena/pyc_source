# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\MetricContainer\pyMetric.py
# Compiled at: 2020-02-11 21:49:52
# Size of source mod 2**32: 6325 bytes
"""
All Metric computing class must inherit 'DistributionSystemMetric' class and implement the ComputeMetric function appropriately

List of metric class implemented currently:

VoltageViolationRiskMetric - Input: voltagearray, numofdownwardcustomers, Totalcustomers, simulationtimestep, VupperPU=1.1, VlowerPU=0.9, Output: gamma, VRI
LineOrTransformerViolationRiskMetric - Input: currentarray, limit ,numofdownwardcustomers, Totalcustomers, simulationtimestep, MaxLoadingPU=1.0, Output: alpha, loading, VRI
LineOrTransformerEfficiency - Input: Powerarray, lossarray Output: Peff, Qeff, Ploss, Qloss, Psendpower, Qsendpower
TransformerLossofLife - Input: Loadingarray, temperaturearray, lifeparameterdict, Output: lossoflife
"""

def ComputeMetricWrapper(MetricClass, *argv, **kwargs):
    return (MetricClass.ComputeMetric)(*argv, **kwargs)


class DistributionSystemMetric:

    def ComputeMetric(*argv, **kwargs):
        pass


class VoltageViolationRiskMetric(DistributionSystemMetric):

    def ComputeMetric(*argv, **kwargs):
        MagnitudeList, NumOfDownwardCustomers, NumOfTotalCustomers, SimulationTimeStep = argv
        UpperVoltageLimit, LowerVoltageLimit = kwargs['VupperPU'], kwargs['VlowerPU']
        maxVoltage, minVoltage = [max(MagnitudeList), min(MagnitudeList)] if type(MagnitudeList) == list else [MagnitudeList, MagnitudeList]
        if maxVoltage < UpperVoltageLimit:
            if minVoltage > LowerVoltageLimit:
                gamma = 0
        if maxVoltage > UpperVoltageLimit:
            if minVoltage < LowerVoltageLimit:
                gamma = max([maxVoltage - UpperVoltageLimit, LowerVoltageLimit - minVoltage])
        if maxVoltage > UpperVoltageLimit:
            if minVoltage > LowerVoltageLimit:
                gamma = maxVoltage - UpperVoltageLimit
        if maxVoltage < UpperVoltageLimit:
            if minVoltage < LowerVoltageLimit:
                gamma = LowerVoltageLimit - minVoltage
        return (
         gamma, NumOfDownwardCustomers / NumOfTotalCustomers * gamma * SimulationTimeStep)


class LineOrTransformerViolationRiskMetric(DistributionSystemMetric):

    def ComputeMetric(*argv, **kwargs):
        import math, numpy as np
        if len(argv) == 4:
            LoadingPU, NumOfDownwardCustomers, NumOfTotalCustomers, SimulationTimeStep = argv
        if len(argv) == 5:
            CurrentRawList, CurrentLimit, NumOfDownwardCustomers, NumOfTotalCustomers, SimulationTimeStep = argv
            MagnitudeList = [math.sqrt(i ** 2 + j ** 2) for i, j in zip(CurrentRawList[::2], CurrentRawList[1::2])]
            LoadingPU = max(MagnitudeList) / float(CurrentLimit) if kwargs['Tag'] == 'Line' else max(MagnitudeList[:int(0.5 * len(MagnitudeList))]) / float(CurrentLimit)
        alpha = LoadingPU - kwargs['MaxLoadingPU'] if LoadingPU > kwargs['MaxLoadingPU'] else 0
        return (alpha, LoadingPU, NumOfDownwardCustomers / NumOfTotalCustomers * alpha * SimulationTimeStep)


class LineOrTransformerEfficiency(DistributionSystemMetric):

    def ComputeMetric(*argv, **kwargs):
        import math, numpy as np
        ElementPower, ElementLoss = argv
        Bus1ElementPower, Bus2ElementPower = ElementPower[:int(0.5 * len(ElementPower))], ElementPower[int(0.5 * len(ElementPower)):]
        ActivePowerLoss, ReactivePowerLoss = ElementLoss[0], ElementLoss[1]
        SendingActivePower = abs(sum(Bus1ElementPower[::2])) if abs(sum(Bus1ElementPower[::2])) > abs(sum(Bus2ElementPower[::2])) else abs(sum(Bus2ElementPower[::2]))
        SendingReactivePower = abs(sum(Bus1ElementPower[1::2])) if abs(sum(Bus1ElementPower[1::2])) > abs(sum(Bus2ElementPower[1::2])) else abs(sum(Bus2ElementPower[1::2]))
        ActivePowerEfficiency, ReactivePowerEfficiency = ActivePowerLoss / (10 * SendingActivePower), ReactivePowerLoss / (10 * SendingReactivePower)
        Overgeneration = sum(Bus2ElementPower[::2]) - sum(Bus1ElementPower[::2]) if sum(Bus2ElementPower[::2]) - sum(Bus1ElementPower[::2]) > 0 else 0
        return (
         ActivePowerEfficiency, ReactivePowerEfficiency, ActivePowerLoss, ReactivePowerLoss, SendingActivePower, SendingReactivePower, Overgeneration)


class TransformerLossofLife(DistributionSystemMetric):

    def ComputeMetric(*argv, **kwargs):
        import math
        TransformerLoadingList, TemperatureData, TransformerLifeParametersDict = argv
        TransformerLoadingList, TemperatureData = TransformerLoadingList + [TransformerLoadingList[0]], TemperatureData + [TemperatureData[0]]
        theta_ii = TransformerLifeParametersDict['theta_i']
        for ite in range(int(TransformerLifeParametersDict['num_of_iteration'])):
            TransformerHotSpotTemperatureList = []
            for k in range(len(TransformerLoadingList)):
                theta_u = TransformerLifeParametersDict['theta_fl'] * pow((TransformerLoadingList[k] * TransformerLoadingList[k] * TransformerLifeParametersDict['R'] + 1) / (TransformerLifeParametersDict['R'] + 1), TransformerLifeParametersDict['n'])
                theta_not = (theta_u - theta_ii) * (1 - math.exp(-0.25 / TransformerLifeParametersDict['tau'])) + theta_ii
                theta_ii = theta_not
                theta_g = TransformerLifeParametersDict['theta_gfl'] * pow(TransformerLoadingList[k], 2 * TransformerLifeParametersDict['m'])
                theta_hst = theta_not + TemperatureData[k] + theta_g
                TransformerHotSpotTemperatureList.append(theta_hst)

            theta_ii = theta_hst - TemperatureData[k] - theta_g

        loss_of_life = sum([25.0 / pow(10, TransformerLifeParametersDict['A'] + TransformerLifeParametersDict['B'] / (el + 273)) for el in TransformerHotSpotTemperatureList])
        return loss_of_life