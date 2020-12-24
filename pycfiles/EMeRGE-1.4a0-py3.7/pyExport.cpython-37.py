# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\ExportContainer\pyExport.py
# Compiled at: 2020-02-26 17:07:28
# Size of source mod 2**32: 2140 bytes
import pandas as pd, os

class ProcessExport:

    def __init__(self, ExportObject, ExportPath):
        self.system_level_metrics = ExportObject.system_level_metrics
        self.system_level_metrics_time_series = ExportObject.system_level_metrics_time_series
        self.Asset_level_metric = ExportObject.Asset_level_metric
        self.Asset_level_metric_time_series = ExportObject.Asset_level_metric_time_series
        self.AssetLevelParameters = ExportObject.AssetLevelParameters
        if not os.path.exists(ExportPath):
            os.mkdir(ExportPath)
        DataToBeExported = {'Metrics':[],  'Values':[]}
        DataToBeExported['Metrics'], DataToBeExported['Values'] = [keys for keys in self.system_level_metrics.keys()], [values for keys, values in self.system_level_metrics.items()]
        self.CSVexport(DataToBeExported, os.path.join(ExportPath, 'SystemLevelMetrics.csv'))
        self.CSVexport(self.system_level_metrics_time_series, os.path.join(ExportPath, 'SystemLevelMetricsTimeSeries.csv'))
        for keys, values in self.Asset_level_metric.items():
            DataToBeExported = {'Metrics':[],  'Values':[]}
            DataToBeExported['Metrics'], DataToBeExported['Values'] = [key for key in values.keys()], [value for key, value in values.items()]
            self.CSVexport(DataToBeExported, os.path.join(ExportPath, keys + 'Asset.csv'))

        for keys, values in self.Asset_level_metric_time_series.items():
            self.CSVexport(values, os.path.join(ExportPath, keys + 'AssetTimeSeries.csv'))

        for keys, values in self.AssetLevelParameters.items():
            self.CSVexport(values, os.path.join(ExportPath, keys + 'AssetTimeSeries.csv'))

    def CSVexport(self, DataDict, ExportPath):
        Dataframe = pd.DataFrame.from_dict(DataDict)
        Dataframe.to_csv(ExportPath, index=False)