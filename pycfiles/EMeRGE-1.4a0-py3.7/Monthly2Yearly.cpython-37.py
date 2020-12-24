# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\CombineMonthlyResults\Monthly2Yearly.py
# Compiled at: 2020-03-24 13:22:51
# Size of source mod 2**32: 5337 bytes
import pandas as pd, calendar, os

class Template:
    __doc__ = ' A class which generates template for combining monthly results including .toml file\n    \n    :param FolderPath: A folder path where you want to create project\n    :type FolderPath: str\n    '

    def __init__(self, FolderPath):
        FolderName = 'Monthy2YearlyFolderTemplate'
        os.mkdir(os.path.join(FolderPath, FolderName))
        os.mkdir(os.path.join(FolderPath, FolderName, 'MonthlyResults'))
        print('{} created successfully'.format(os.path.join(FolderPath, FolderName, 'MonthlyResults')))
        os.mkdir(os.path.join(FolderPath, FolderName, 'YearlyResults'))
        print('{} created successfully'.format(os.path.join(FolderPath, FolderName, 'MonthlyResults')))


class Monthly2Yearly:
    __doc__ = ' A class for combining monthly results.\n    \n    :param inputpath: A path where all monthly results are stored\n    :type inputpath: str\n    :param outputpath: A path where you want to store results\n    :type outputpath: str\n    :param DoNotReadFiles: list of files to avoid combining\n    :type DoNotReadFiles: list, optional\n    :return: csv files\n    '

    def __init__(self, inputpath, outputpath, DoNotReadFiles=[]):
        FolderNameList = ['Category_' + calendar.month_name[(i + 1)][0:3] for i in range(12)]
        PVScenarios_list = ['{}.0%-customer-100.0%-PV'.format((i + 1) * 10) for i in range(10)]
        PVScenarios_list = PVScenarios_list + ['Base']
        MetricAddition = ['{}Asset.csv'.format(metric) for metric in ('CRI', 'LVRI',
                                                                      'TVRI', 'NVRI',
                                                                      'TLOF', 'TOG')]
        MetricAverage = ['{}Asset.csv'.format(metric) for metric in ('LE', 'TE')]
        for PVScenario in PVScenarios_list:
            AllDataDict = {}
            print('Converting monthly result to annual for {} scenario ..............................................'.format(PVScenario))
            if not os.path.exists(os.path.join(outputpath, PVScenario)):
                os.mkdir(os.path.join(outputpath, PVScenario))
            for Folder in FolderNameList:
                assert os.path.exists(os.path.join(inputpath, Folder, PVScenario)), '{} does not exists.'.format(os.path.join(inputpath, Folder, PVScenario))
                for files in os.listdir(os.path.join(inputpath, Folder, PVScenario)):
                    if 'TimeSeries.csv' in files:
                        if files not in DoNotReadFiles:
                            if files not in AllDataDict:
                                AllDataDict[files] = []
                            AllDataDict[files].append(pd.read_csv(os.path.join(inputpath, Folder, PVScenario, files)))
                    if files not in DoNotReadFiles:
                        if files not in AllDataDict:
                            AllDataDict[files] = pd.read_csv(os.path.join(inputpath, Folder, PVScenario, files))
                        else:
                            this_dataframe = pd.read_csv(os.path.join(inputpath, Folder, PVScenario, files))
                            AllDataDict[files]['Values'] = [sum(x) for x in zip(AllDataDict[files]['Values'].tolist(), this_dataframe['Values'].tolist())]

            for keys, values in AllDataDict.items():
                if 'TimeSeries.csv' in keys:
                    df = pd.concat(values)
                    df.to_csv((os.path.join(outputpath, PVScenario, keys)), index=False)
                    print('{} created successfully'.format(os.path.join(outputpath, PVScenario, keys)))
                elif keys in MetricAverage:
                    values['Values'] = [el / 12 for el in values['Values']]
                    values.to_csv((os.path.join(outputpath, PVScenario, keys)), index=False)
                    print('{} created successfully'.format(os.path.join(outputpath, PVScenario, keys)))
                elif keys == 'SystemLevelMetrics.csv':
                    datadict = dict(zip(values['Metrics'], values['Values']))
                    keys_to_average = ['SE_line', 'SE_transformer', 'SE']
                    for key, val in datadict.items():
                        if key in keys_to_average:
                            datadict[key] = val / 12

                    datadictmodified = {'Metrics':[k for k in datadict.keys()], 
                     'Values':[v for k, v in datadict.items()]}
                    df = pd.DataFrame.from_dict(datadictmodified)
                    df.to_csv((os.path.join(outputpath, PVScenario, keys)), index=False)
                    print('{} created successfully'.format(os.path.join(outputpath, PVScenario, keys)))
                else:
                    values.to_csv((os.path.join(outputpath, PVScenario, keys)), index=False)
                    print('{} created successfully'.format(os.path.join(outputpath, PVScenario, keys)))


if __name__ == '__main__':
    inputpath = 'C:\\Users\\KDUWADI\\Desktop\\NREL_Projects\\CIFF-TANGEDCO\\TANGEDCO\\SoftwareTools\\CombineMonthlyResults\\MonthlyResults\\GWC'
    outputpath = 'C:\\Users\\KDUWADI\\Desktop\\NREL_Projects\\CIFF-TANGEDCO\\TANGEDCO\\SoftwareTools\\CombineMonthlyResults\\YearlyResults\\GWC'
    DonotReadFilesList = ['voltagemagAssetTimeSeries.csv', 'lineloadingAssetTimeSeries.csv', 'transformerloadingAssetTimeSeries.csv']
    Monthly2Yearly(inputpath, outputpath, DonotReadFilesList)