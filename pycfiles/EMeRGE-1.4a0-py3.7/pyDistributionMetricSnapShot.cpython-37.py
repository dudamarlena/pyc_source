# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\pyDistributionMetricSnapShot.py
# Compiled at: 2020-03-15 13:08:04
# Size of source mod 2**32: 9995 bytes
import numpy as np
from ResultDashboard.Dashboard.DSSRiskAnalyzer.MetricContainer.pyMetric import *

def DistributionSystemMetricWrapper(ElementClass, **kwargs):
    return (ElementClass(**kwargs).ComputeDistributionSystemMetrics)(**kwargs)


class MetricsAbstract:
    __doc__ = ' Abstract class for Metrics'

    def __init__(self, **kwargs):
        self.DSS = kwargs['DSSobject']
        self.Circuit = self.DSS.Circuit
        self.Bus = self.DSS.Bus
        self.Loads = self.DSS.Loads
        self.Element = self.DSS.CktElement
        self.DSSClass = self.DSS.ActiveClass
        self.SimulationSettings = kwargs['SimulationSettings']
        self.TotalCustomers = self.Loads.Count()
        self.OutputDict = {'VRI':{},  'CRI_weight':{LoadName:0 for LoadName in self.Loads.AllNames()}, 
         'SARDI':[],  'ImpactedCustomersList':[]}

    def ComputeDistributionSystemMetrics(self, **kwargs):
        pass


class SystemMetric(MetricsAbstract):

    def ComputeDistributionSystemMetrics(self, **kwargs):
        import numpy as np
        NodeDict, LineDict, TransformerDict = kwargs['Node'], kwargs['Line'], kwargs['Transformer']
        self.OutputDict['ImpactedCustomersList'] = NodeDict['ImpactedCustomersList'] + LineDict['ImpactedCustomersList'] + TransformerDict['ImpactedCustomersList']
        self.OutputDict['SARDI'] = len(np.unique(self.OutputDict['ImpactedCustomersList'])) * self.SimulationSettings['simulation_time_step'] / self.TotalCustomers
        for LoadName, Values in self.OutputDict['CRI_weight'].items():
            self.OutputDict['CRI_weight'][LoadName] = (NodeDict['CRI_weight'][LoadName] + LineDict['CRI_weight'][LoadName] + TransformerDict['CRI_weight'][LoadName]) / self.SimulationSettings['simulation_time_step']

        LineLossPowerArray = [effarray[2:6] for Line, effarray in LineDict['EfficiencyMetric'].items()]
        self.OutputDict['LineLossPower'] = [sum(array) for array in list(zip(*LineLossPowerArray))]
        TransformerLossPowerArray = [effarray[2:6] for Transformer, effarray in TransformerDict['EfficiencyMetric'].items()]
        self.OutputDict['TransformerLossPower'] = [sum(array) for array in list(zip(*TransformerLossPowerArray))]
        self.OutputDict['TotalLossPower'] = [sum(array) for array in zip(*[self.OutputDict['LineLossPower'], self.OutputDict['TransformerLossPower']])]
        self.OutputDict['Overgeneration'] = round(self.Circuit.TotalPower()[0]) if self.Circuit.TotalPower()[0] > 0 else 0
        return self.OutputDict


class NodalMetric(MetricsAbstract):

    def ComputeDistributionSystemMetrics(self, **kwargs):
        import numpy as np
        for BusName in self.Circuit.AllBusNames():
            self.Circuit.SetActiveBus(BusName)
            VoltageMagnitudeList, NodeName = self.Bus.puVmagAngle()[::2], BusName.split('.')[0].lower()
            gamma, self.OutputDict['VRI'][NodeName] = ComputeMetricWrapper(VoltageViolationRiskMetric, VoltageMagnitudeList,
              (len(kwargs['NodeCustDown'][NodeName])), (self.TotalCustomers), (self.SimulationSettings['simulation_time_step']), VupperPU=(self.SimulationSettings['voltage_upper_limit']),
              VlowerPU=(self.SimulationSettings['voltage_lower_limit']))
            if gamma != 0:
                self.OutputDict['ImpactedCustomersList'].extend(kwargs['NodeCustDown'][NodeName])
            if 'VoltageMag' not in self.OutputDict:
                self.OutputDict['VoltageMag'] = {}
            self.OutputDict['VoltageMag'][BusName] = max(VoltageMagnitudeList)
            for LoadName in kwargs['NodeCustDown'][NodeName]:
                if self.OutputDict['CRI_weight'][LoadName] < gamma:
                    self.OutputDict['CRI_weight'][LoadName] = gamma

        self.OutputDict['SARDI'] = len(np.unique(self.OutputDict['ImpactedCustomersList'])) * self.SimulationSettings['simulation_time_step'] / self.TotalCustomers
        return self.OutputDict


class LineMetric(MetricsAbstract):

    def ComputeDistributionSystemMetrics(self, **kwargs):
        self.Circuit.SetActiveClass('Line')
        flag = self.DSSClass.First()
        while flag > 0:
            LineName, LineCurrentRawList, LineLimit = self.Element.Name().split('.')[1], self.Element.Currents(), self.Element.NormalAmps()
            alpha, loadingPU, self.OutputDict['VRI'][LineName] = ComputeMetricWrapper(LineOrTransformerViolationRiskMetric, LineCurrentRawList,
              LineLimit, (len(kwargs['LineCustDown'][LineName])), (self.TotalCustomers), (self.SimulationSettings['simulation_time_step']), MaxLoadingPU=(self.SimulationSettings['line_loading_upper_limit']),
              Tag='Line')
            if alpha != 0:
                self.OutputDict['ImpactedCustomersList'].extend(kwargs['LineCustDown'][LineName])
            for LoadName in kwargs['LineCustDown'][LineName]:
                if self.OutputDict['CRI_weight'][LoadName] < alpha:
                    self.OutputDict['CRI_weight'][LoadName] = alpha

            if 'EfficiencyMetric' not in self.OutputDict:
                self.OutputDict['EfficiencyMetric'] = {}
            self.OutputDict['EfficiencyMetric'][LineName] = ComputeMetricWrapper(LineOrTransformerEfficiency, self.Element.Powers(), self.Element.Losses())
            if 'PULoading' not in self.OutputDict:
                self.OutputDict['PULoading'] = {}
            self.OutputDict['PULoading'][LineName] = loadingPU
            flag = self.DSSClass.Next()

        self.OutputDict['SARDI'] = len(np.unique(self.OutputDict['ImpactedCustomersList'])) * self.SimulationSettings['simulation_time_step'] / self.TotalCustomers
        return self.OutputDict


class TransformerMetric(MetricsAbstract):

    def ComputeDistributionSystemMetrics(self, **kwargs):
        self.Circuit.SetActiveClass('Transformer')
        flag = self.DSSClass.First()
        while flag > 0:
            TransformerName, TransformerCurrentRawList, TransformerLimit = self.Element.Name().split('.')[1], self.Element.Currents(), self.Element.NormalAmps()
            beta, TransformerPUloading, self.OutputDict['VRI'][TransformerName] = ComputeMetricWrapper(LineOrTransformerViolationRiskMetric, TransformerCurrentRawList,
              TransformerLimit, (len(kwargs['TransformerCustDown'][TransformerName])), (self.TotalCustomers), (self.SimulationSettings['simulation_time_step']), MaxLoadingPU=(self.SimulationSettings['transformer_loading_upper_limit']),
              Tag='Transformer')
            if 'PULoading' not in self.OutputDict:
                self.OutputDict['PULoading'] = {}
            self.OutputDict['PULoading'][TransformerName] = TransformerPUloading
            if beta != 0:
                self.OutputDict['ImpactedCustomersList'].extend(kwargs['TransformerCustDown'][TransformerName])
            for LoadName in kwargs['TransformerCustDown'][TransformerName]:
                if self.OutputDict['CRI_weight'][LoadName] < beta:
                    self.OutputDict['CRI_weight'][LoadName] = beta

            if 'EfficiencyMetric' not in self.OutputDict:
                self.OutputDict['EfficiencyMetric'] = {}
            self.OutputDict['EfficiencyMetric'][TransformerName] = ComputeMetricWrapper(LineOrTransformerEfficiency, self.Element.Powers(), self.Element.Losses())
            if 'Overgeneration' not in self.OutputDict:
                self.OutputDict['Overgeneration'] = {}
            self.OutputDict['Overgeneration'][TransformerName] = round(self.OutputDict['EfficiencyMetric'][TransformerName][(-1)], 3)
            flag = self.DSSClass.Next()

        self.OutputDict['SARDI'] = len(np.unique(self.OutputDict['ImpactedCustomersList'])) * self.SimulationSettings['simulation_time_step'] / self.TotalCustomers
        return self.OutputDict