# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\pyRunTimeSeriesPowerFlow.py
# Compiled at: 2020-03-15 13:07:48
# Size of source mod 2**32: 5952 bytes
import opendssdirect as dss
from datetime import timedelta
from ResultDashboard.Dashboard.DSSRiskAnalyzer.MetricContainer.pyMetric import *
from ResultDashboard.Dashboard.DSSRiskAnalyzer.SubModulesContainer.DateTimeProcessingContainer import *
from ResultDashboard.Dashboard.DSSRiskAnalyzer.pyDistributionMetricSnapShot import *
from ResultDashboard.Dashboard.DSSRiskAnalyzer.ResultContainer.pyResult import *
from ResultDashboard.Dashboard.DSSRiskAnalyzer.ExportContainer.pyExport import *

class OpenDSS:

    def __init__(self, DSSpath, SimulationSettings, ExtraDataFilesDataStoredByIndicator, ExportPath):
        self.SimulationSettings = SimulationSettings
        self.DSSpath = DSSpath
        self.ExtraDataFilesStoredByIndicator = ExtraDataFilesDataStoredByIndicator
        self.DSS = dss
        self.ExportPath = ExportPath
        self.RunOpenDSSPowerFlow()

    def RunOpenDSSPowerFlow(self):
        self.DSS.run_command('Clear')
        self.DSS.Basic.ClearAll()
        print(self.DSS.run_command('Redirect {}'.format(self.DSSpath)))
        self.StartDate, self.EndDate, self.SimulationTimePeriod, self.SimulationStartIndex = DateTimeProcessorWrapper(OpenDSSStartEndTimeProcessor, StartDate=(self.SimulationSettings['start_time']), EndDate=(self.SimulationSettings['stop_time']), Unit=(self.SimulationSettings['simulation_time_unit']), Format=(self.SimulationSettings['time_format']))
        self.SimulationStartIndex = int(self.SimulationStartIndex / self.SimulationSettings['simulation_time_step'])
        self.SimulationTimeCounter, self.SimulationTimeStamp = 0, self.StartDate
        self.SecondConverter = {'Minute':0.016666666666666666, 
         'Hour':0.0002777777777777778,  'Second':1}
        self.MinuteConverter = {'Minute':1,  'Hour':0.016666666666666666,  'Second':60}
        self.DeltaTimeStep = self.DSS.Solution.StepSize() * self.SecondConverter[self.SimulationSettings['simulation_time_unit']]
        self.TimeStampForRecordingData = []
        self.TemperatureData = list(self.ExtraDataFilesStoredByIndicator['TemperatureData']['Temperature'])
        self.TemperatureDataSliced = self.TemperatureData[self.SimulationStartIndex:self.SimulationStartIndex + int(self.SimulationTimePeriod / self.SimulationSettings['simulation_time_step'])]
        self.TransformerLifeParameters = self.ExtraDataFilesStoredByIndicator['TransformerLifeParameters'].set_index('Parameters')['Value'].to_dict()
        NodeMetricDict, LineMetricDict, TransformerMetricDict, SystemMetricDict = ({}, {}, {}, {})
        while self.SimulationTimeCounter < self.SimulationTimePeriod:
            self.DSS.Solution.Number(1)
            self.SimulationTimeStepMinute = self.SimulationSettings['simulation_time_step'] * self.MinuteConverter[self.SimulationSettings['simulation_time_unit']]
            self.DSS.run_command('set stepsize={}m'.format(self.SimulationTimeStepMinute + 1))
            self.DSS.run_command('set controlmode=time')
            if self.SimulationTimeCounter == 0:
                self.DSS.run_command('set number={}'.format(self.SimulationStartIndex))
            self.DSS.Solution.Solve()
            self.MetricsStoreFlag = 1 if self.SimulationTimeCounter % self.SimulationSettings['Risk_metric_aggregate_minutes'] == 0 else 0
            if self.DSS.Solution.Iterations() < self.SimulationSettings['Maximum_Iteration']:
                if self.DSS.Solution.Converged():
                    NodeMetricDict[str(self.SimulationTimeStamp)] = DistributionSystemMetricWrapper(NodalMetric, DSSobject=(self.DSS), SimulationSettings=(self.SimulationSettings), NodeCustDown=(self.ExtraDataFilesStoredByIndicator['NodeDownwardCustomers']))
                    LineMetricDict[str(self.SimulationTimeStamp)] = DistributionSystemMetricWrapper(LineMetric, DSSobject=(self.DSS), SimulationSettings=(self.SimulationSettings), LineCustDown=(self.ExtraDataFilesStoredByIndicator['LineDownwardCustomers']))
                    TransformerMetricDict[str(self.SimulationTimeStamp)] = DistributionSystemMetricWrapper(TransformerMetric, DSSobject=(self.DSS), SimulationSettings=(self.SimulationSettings), TransformerCustDown=(self.ExtraDataFilesStoredByIndicator['TransformerDownwardCustomers']))
                    SystemMetricDict[str(self.SimulationTimeStamp)] = DistributionSystemMetricWrapper(SystemMetric, Node=(NodeMetricDict[str(self.SimulationTimeStamp)]), Line=(LineMetricDict[str(self.SimulationTimeStamp)]), Transformer=(TransformerMetricDict[str(self.SimulationTimeStamp)]), DSSobject=(self.DSS), SimulationSettings=(self.SimulationSettings))
            if self.MetricsStoreFlag:
                if self.SimulationTimeCounter != 0:
                    self.TimeStampForRecordingData.append(str(self.SimulationTimeStamp))
            if self.MetricsStoreFlag:
                print(self.SimulationTimeStamp)
            self.SimulationTimeStamp = self.SimulationTimeStamp + timedelta(minutes=(self.SimulationSettings['simulation_time_step']))
            self.SimulationTimeCounter += self.DeltaTimeStep

        self.OutputObject = ResultProcessor(self.TimeStampForRecordingData, NodeMetricDict, LineMetricDict, TransformerMetricDict, SystemMetricDict, self.TemperatureDataSliced, self.TransformerLifeParameters)
        ProcessExport(self.OutputObject, self.ExportPath)