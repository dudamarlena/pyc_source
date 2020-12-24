# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/lib/fetchclimate/fc_time_series.py
# Compiled at: 2014-10-02 15:19:10
import datetime, time

class FCTimeSeries:

    def __init__(self, temporalDomain, averageData):
        self.temporalDomain = temporalDomain
        self.averageData = averageData
        self.combinedData = []
        self.initTimeSeriesData()
        self.combinedDataMiliSec = []
        self.plots = None
        return

    def timeSeriesDateToMilisecond(self):
        if self.temporalDomain.hourCellMode:
            dt = datetime.timedelta(hours=-7)
        else:
            dt = datetime.timedelta(hours=1)
        self.combinedDataMiliSec = self.combinedData
        for point in self.combinedDataMiliSec:
            shiftedTime = point[0] + dt
            point[0] = time.mktime(shiftedTime.timetuple()) * 1000

        return self.combinedDataMiliSec

    def isLeapYear(self, year):
        return year > 1582 and (0 == year % 400 or 0 == year % 4 and not 0 == year % 100)

    def getNumericMonthDay(self, yearNum, dayNum):
        daysInFeb = 29 if self.isLeapYear(yearNum) else 28
        if dayNum <= 31:
            return [1, dayNum]
        if dayNum <= 31 + daysInFeb:
            return [2, dayNum - 31]
        if dayNum <= 62 + daysInFeb:
            return [3, dayNum - (31 + daysInFeb)]
        if dayNum <= 92 + daysInFeb:
            return [4, dayNum - (62 + daysInFeb)]
        if dayNum <= 123 + daysInFeb:
            return [5, dayNum - (92 + daysInFeb)]
        if dayNum <= 93 + 60 + daysInFeb:
            return [
             6, dayNum - (123 + daysInFeb)]
        if dayNum <= 124 + 60 + daysInFeb:
            return [7, dayNum - (93 + 60 + daysInFeb)]
        if dayNum <= 155 + 60 + daysInFeb:
            return [8, dayNum - (124 + 60 + daysInFeb)]
        if dayNum <= 155 + 90 + daysInFeb:
            return [9, dayNum - (155 + 60 + daysInFeb)]
        if dayNum <= 186 + 90 + daysInFeb:
            return [10, dayNum - (155 + 90 + daysInFeb)]
        if dayNum <= 186 + 120 + daysInFeb:
            return [11, dayNum - (186 + 90 + daysInFeb)]
        if dayNum <= 217 + 120 + daysInFeb:
            return [12, dayNum - (186 + 120 + daysInFeb)]

    def timeSeriesDataSize(self):
        lenHours = (self.temporalDomain.hourCellMode or len)(self.temporalDomain.hours) if 1 else 1
        lenDays = (self.temporalDomain.dayCellMode or len)(self.temporalDomain.days) if 1 else 1
        lenYears = (self.temporalDomain.yearCellMode or len)(self.temporalDomain.years) if 1 else 1
        return lenHours * lenDays * lenYears

    def initTimeSeriesData(self):
        self.combinedData = []
        hours = [
         0]
        if not self.temporalDomain.hourCellMode:
            hours = self.temporalDomain.hours
        days = [
         1]
        if not self.temporalDomain.dayCellMode:
            days = self.temporalDomain.days
        if not self.temporalDomain.yearCellMode:
            years = self.temporalDomain.years
            tmpData = self.averageData if self.averageData else [ 0 for i in range(len(years) * len(days) * len(hours)) ]
        else:
            years = [
             self.temporalDomain.years[0], self.temporalDomain.years[(len(self.temporalDomain.years) - 1)]]
            if isinstance(self.averageData, list):
                dataValue = self.averageData[0] if self.averageData else 0
            else:
                dataValue = self.averageData if self.averageData else 0
            tmpData = [ dataValue for i in range(len(years) * len(days) * len(hours)) ]
        dayLen = len(days)
        hourLen = len(hours)
        for i in range(len(years)):
            for j in range(dayLen):
                for k in range(hourLen):
                    monthDay = self.getNumericMonthDay(years[i], days[j])
                    self.combinedData.append([datetime.datetime(years[i], monthDay[0], monthDay[1], hours[k]), tmpData[(i * dayLen + j * hourLen + k)]])

    def getTimeSeriesPlot(self, variableName, gridName, variableDescription, response=None, hashString=None):
        timeseries_plot_object = {'chart': {'type': 'area', 
                     'zoomType': 'x'}, 
           'title': {'text': gridName}, 
           'xAxis': {'maxZoom': 86400000, 
                     'type': 'datetime'}, 
           'yAxis': {'title': {'text': variableDescription}, 
                     'min': 0}, 
           'series': [
                    {'name': variableDescription, 
                       'data': self.combinedData}], 
           'custom': {'grid': gridName, 
                      'variable': variableName, 
                      'hash': hashString, 
                      'responseUri': response.uri if response else None}}
        return {'highcharts_object': timeseries_plot_object, 'width': '500px', 'height': '500px'}