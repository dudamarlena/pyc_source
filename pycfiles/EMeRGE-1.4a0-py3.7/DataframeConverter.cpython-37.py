# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DSSRiskAnalyzer\SubModulesContainer\DataframeConverter.py
# Compiled at: 2020-02-02 13:39:38
# Size of source mod 2**32: 827 bytes
"""
 List of sub-modules for processing dataframe:

 Avialable functionality
 1) Dataframe2DictionaryTwoColumn: e.g. DataFrameConverterWrapper(Dataframe2DictionaryTwoColumn,Dataframe, KeyCol="Keycolumname", ValCol="ValueColname")
 Explanation: Output will be dictionary with keys from values in 'Keycolumnname' and values from values in 'ValueColname'

 """

def DataFrameConverterWrapper(DataFrameConverterClass, dataframe, **kwargs):
    return (DataFrameConverterClass.ConvertDataFrame)(dataframe, **kwargs)


class DataframeConverter:

    def ConvertDataframe(dataframe, **kwargs):
        pass


class Dataframe2DictionaryTwoColumn(DataframeConverter):

    def ConvertDataframe(dataframe, **kwargs):
        return dict(zip(list(dataframe[kwargs['KeyCol']]), list(dataframe[kwargs['Valcol']])))