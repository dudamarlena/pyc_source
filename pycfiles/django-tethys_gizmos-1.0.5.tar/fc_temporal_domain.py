# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/lib/fetchclimate/fc_temporal_domain.py
# Compiled at: 2014-10-02 15:19:10


def FCparseMatlabSequence(s):
    if s.find(':') >= 0:
        seq = s.split(':')
        if len(seq) == 2:
            from_ = float(seq[0])
            to = float(seq[1])
            if from_ > to:
                raise Exception('End of sequence should be less than start')
            result = []
            while from_ <= to:
                result.append(from_)
                from_ += 1

            return result
        if len(seq) == 3:
            from_ = float(seq[0])
            to = float(seq[2])
            step = float(seq[1])
            if from_ > to:
                raise Exception('End of sequence should be less than start')
            if step <= 0:
                raise Exception('Step should be positive')
            result = []
            while from_ <= to:
                result.append(from_)
                from_ += step

            return result
        if len(seq) > 3:
            raise Exception('Too many points in matlab notation')
    else:
        if s.find(',') >= 0:
            seq = s.split(',')
            result = []
            for seq_i in seq:
                result.append(float(seq_i))

            return result
        return [float(s)]


def FCgetMatlabSequence(a):
    if len(a) == 1:
        return a[0] + ''
    else:
        if len(a) == 2:
            return a[0] + ',' + a[1]
        step = a[1] - a[0]
        isConstantStep = True
        for i in range(1, len(a) - 2):
            if abs(a[(i + 1)] - a[i] - step) > 1e-10:
                isConstantStep = False
                break

        if isConstantStep:
            return a[0] + ':' + step + ':' + a[(len(a) - 1)]
        result = ''
        for i in range(1, len(a)):
            if len(result) > 0:
                result = result + ','
            result = result + a[i]

        return result


class FCTemporalDomain:

    def __init__(self, years, yearCellMode, days, dayCellMode, hours, hourCellMode):
        if not isinstance(years, list) or not isinstance(days, list) or not isinstance(hours, list):
            raise Exception('Years, days and hours must be arrays')
        if yearCellMode and len(years) < 2:
            raise Exception('At least two years must be specified in cell mode')
        if dayCellMode and len(days) < 2:
            raise Exception('At least two days must be specified in cell mode')
        if hourCellMode and len(hours) < 2:
            raise Exception('At least two hours must be specified in cell mode')
        self.yearCellMode = yearCellMode
        self.years = self.setTime(years, yearCellMode)
        self.dayCellMode = dayCellMode
        self.days = self.setTime(days, dayCellMode)
        self.hourCellMode = hourCellMode
        self.hours = self.setTime(hours, hourCellMode)

    def fillFetchRequest(self, request):
        if 'Domain' not in request:
            request['Domain'] = {}
        request['Domain']['TimeRegion'] = {'Years': self.years, 
           'Days': self.days, 
           'Hours': self.hours, 
           'IsIntervalsGridYears': self.yearCellMode, 
           'IsIntervalsGridDays': self.dayCellMode, 
           'IsIntervalsGridHours': self.hourCellMode}

    def setTime(self, time, timeCellMode):
        if not timeCellMode:
            if len(time) == 1:
                return time
            else:
                if time[0] == time[(len(time) - 1)]:
                    return [time[0]]
                return range(time[0], time[(len(time) - 1)] + 1)

        else:
            return time


class FCTemporalDomainBuilder:

    def __init__(self):
        self.years = 0
        self.days = 0
        self.hours = 0
        self.isYearPoints = False
        self.isDayPoints = False
        self.isHourPoints = False

    def parseYears(self, s):
        if self.years:
            raise Exception('Year axis is already defined')
        yp = FCparseMatlabSequence(s)
        if len(yp) == 1 and not self.isYearPoints:
            raise Exception('At least two points must be defined for year cells')
        self.years = [ int(i) for i in yp ]

    def parseDays(self, s):
        if self.days:
            raise Exception('Days axis is already defined')
        dp = FCparseMatlabSequence(s)
        if len(dp) == 1 and not self.isDayPoints:
            raise Exception('At least two points must be defined for day cells')
        self.days = [ int(i) for i in dp ]

    def parseHours(self, s):
        if self.hours:
            raise Exception('Hour axis is already defined')
        hp = FCparseMatlabSequence(s)
        if len(hp) == 1 and not self.isHourPoints:
            raise Exception('At least two points must be defined for hour cells')
        self.hours = [ int(i) for i in hp ]

    def parseYearCells(self, s):
        self.isYearPoints = False
        self.parseYears(s)

    def parseDayCells(self, s):
        self.isDayPoints = False
        self.parseDays(s)

    def parseHourCells(self, s):
        self.isHourPoints = False
        self.parseHours(s)

    def parseYearPoints(self, s):
        self.isYearPoints = True
        self.parseYears(s)

    def parseDayPoints(self, s):
        self.isDayPoints = True
        self.parseDays(s)

    def parseHourPoints(self, s):
        self.isHourPoints = True
        self.parseHours(s)

    def getTemporalDomain(self):
        if not self.years or not self.days or not self.hours:
            return None
        return FCTemporalDomain(self.years, not self.isYearPoints, self.days, not self.isDayPoints, self.hours, not self.isHourPoints)