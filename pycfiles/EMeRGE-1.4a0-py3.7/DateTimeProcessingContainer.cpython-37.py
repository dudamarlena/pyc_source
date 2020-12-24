# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\DateTimeProcessingContainer.py
# Compiled at: 2020-02-05 18:52:56
# Size of source mod 2**32: 1888 bytes
"""
 List of sub-modules for processing datetime:

 Avialable functionality
 1) OpenDSSStartEndTimeProcessor: e.g. DateTimeProcessorWrapper(OpenDSSStartEndTimeProcessor,StartDate='2015-1-1 00:00:00'
 EndDate='2015-1-2 00:00:00', TimeUnit="Minute", TimeFormat='%Y-%m-%d %H:%M:%S') -  TimeUnit = {'Minute'(Default), 'Hour', 'Second'}
 Explanation: StartDate, EndDate, SimulationTimePeriod, SimulationStartTimeIndex

 """

def DateTimeProcessorWrapper(DateTimeProcessorClass, **kwargs):
    return (DateTimeProcessorClass.DateTimeProcessor)(**kwargs)


class DateTimeProcessor:

    def DataTimeProcessor(**kwargs):
        pass


class OpenDSSStartEndTimeProcessor(DateTimeProcessor):

    def DateTimeProcessor(**kwargs):
        import datetime as dt
        StartDate, EndDate = kwargs['StartDate'], kwargs['EndDate']
        TimeUnit = kwargs['Unit'] if 'Unit' in kwargs else 'Minute'
        DateFormat = kwargs['Format'] if 'Format' in kwargs else '%Y/%m/%d %H:%M:%S'
        StartDateStruct = dt.datetime.strptime(StartDate, DateFormat).timetuple()
        StartDate, EndDate = dt.datetime.strptime(StartDate, DateFormat), dt.datetime.strptime(EndDate, DateFormat)
        TimeUnitConversion = {'Second':1, 
         'Minute':60,  'Hour':3600}
        SimulationTimePeriod = int(((EndDate - StartDate).days * 86400 + (EndDate - StartDate).seconds) / TimeUnitConversion[TimeUnit])
        SimulationStartIndex = {'Second':(StartDateStruct.tm_yday - 1) * 1440 * 60 + StartDateStruct.tm_hour * 60 * 60 + StartDateStruct.tm_min * 60 + StartDateStruct.tm_sec, 
         'Minute':(StartDateStruct.tm_yday - 1) * 1440 + StartDateStruct.tm_hour * 60 + StartDateStruct.tm_min, 
         'Hour':(StartDateStruct.tm_yday - 1) * 24 + StartDateStruct.tm_hour}
        return (
         StartDate, EndDate, SimulationTimePeriod, SimulationStartIndex[TimeUnit])