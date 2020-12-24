# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/lib/fetchclimate/fc_response.py
# Compiled at: 2014-10-02 15:19:10
import datetime, requests, urllib

def arrayDepth(l):
    if isinstance(l, list):
        return 1 + max(arrayDepth(item) for item in l)
    else:
        return 0


class FCResponse:

    def __init__(self, request, resultUri):
        self.rq = request
        self.uri = resultUri
        self.values = []

    def rearrangeMeanDataMultYrDayPoint(self):
        arrayAvg = []
        for yearArray in self.values:
            for dayArray in yearArray:
                for dayData in dayArray:
                    arrayAvg.append(dayData)

        return arrayAvg

    def rearrangeMeanDataMultYrDayHourPoint(self):
        arrayAvg = []
        for yearArray in self.values:
            for dayArray in yearArray:
                for hourArray in dayArray:
                    for hourData in hourArray:
                        arrayAvg.append(hourData)

        return arrayAvg

    def findDataMeanAvgGrid(self):
        numValuesInSum = 0
        arraySum = [ 0 for i in range(len(self.values[0])) ]
        for array in self.values:
            for i in range(len(array)):
                if array[i]:
                    arraySum[i] += array[i]
                else:
                    arraySum[i] += arraySum[i] / (numValuesInSum + 1)

            numValuesInSum += 1

        return [ x / float(numValuesInSum) for x in arraySum ]

    def findDataMeanMultYrGrid(self):
        numValuesInSum = 0
        arraySum = [ 0 for i in range(len(self.values[0][0])) ]
        for array in self.values:
            for yearArray in array:
                for i in range(len(yearArray)):
                    if yearArray[i]:
                        arraySum[i] += yearArray[i]
                    else:
                        arraySum[i] += arraySum[i] / (numValuesInSum + 1)

                numValuesInSum += 1

        return [ x / float(numValuesInSum) for x in arraySum ]

    def findDataMeanMultYrDayGrid(self):
        dayLen = len(self.values[0][0][0])
        arraySum = [ 0 for i in range(dayLen * len(self.values[0][0])) ]
        numValuesInSum = 0
        for array in self.values:
            for yearArray in array:
                for yearIndex, dayArray in enumerate(yearArray):
                    for i in range(dayLen):
                        if dayArray[i]:
                            arraySum[(yearIndex * dayLen + i)] += dayArray[i]
                        else:
                            arraySum[(yearIndex * dayLen + i)] += arraySum[(yearIndex * dayLen + i)] / float(numValuesInSum + 1)

                numValuesInSum += 1

        return [ x / float(numValuesInSum) for x in arraySum ]

    def findDataMeanMultYrDayHourGrid(self):
        numValuesInSum = 0
        dayLen = len(self.values[0][0][0])
        hourLen = len(self.values[0][0][0][0])
        arraySum = [ 0 for i in range(len(self.values[0][0]) * dayLen * hourLen) ]
        for array in self.values:
            for yearArray in array:
                for yearIndex, dayArray in enumerate(yearArray):
                    for dayIndex, hourArray in enumerate(dayArray):
                        for i in range(hourLen):
                            if hourArray[i]:
                                arraySum[((yearIndex * dayLen + dayIndex) * hourLen + i)] += hourArray[i]
                            else:
                                arraySum[((yearIndex * dayLen + dayIndex) * hourLen + i)] += arraySum[((yearIndex * dayLen + dayIndex) * hourLen + i)] / float(numValuesInSum + 1)

                numValuesInSum += 1

        return [ x / float(numValuesInSum) for x in arraySum ]

    def findDataMean(self, isPoint=False):
        if any(x is None for x in self.values):
            return None
        else:
            depth = arrayDepth(self.values)
            if len(self.values) == 1:
                if depth == 1:
                    return self.values
                if depth == 2:
                    return self.values[0]
                if depth == 3:
                    return self.rearrangeMeanDataMultYrDayPoint()
                if depth == 4:
                    return self.rearrangeMeanDataMultYrDayHourPoint()
            if depth == 3:
                return self.findDataMeanMultYrGrid()
            if depth == 4:
                return self.findDataMeanMultYrDayGrid()
            if depth == 5:
                return self.findDataMeanMultYrDayHourGrid()
            return self.findDataMeanAvgGrid()

    def getData(self, names=None):
        if not names:
            names = ['values', 'sd']
        print str(datetime.datetime.now()) + ': Requesting ' + str(names) + ' of ' + self.uri
        variables = ''
        for i in range(0, len(names)):
            if len(variables) > 0:
                variables = variables + ','
            variables += names[i]

        headers = {'data-type': 'json'}
        r = requests.get(self.rq.serviceUrl + '/jsproxy/data?uri=' + urllib.quote(self.uri.encode('utf-8')) + '&variables=' + urllib.quote(variables.encode('utf-8')), headers=headers, timeout=self.rq.timeout)
        data = []
        if r.status_code == requests.codes.ok:
            data = r.json()
            self.values = data['values']
        return self.values