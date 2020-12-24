# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/menorah/nupic_output.py
# Compiled at: 2015-10-26 18:09:32
"""
Provides two classes with the same signature for writing data out of NuPIC
models.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import os, csv
from collections import deque
from abc import ABCMeta, abstractmethod
try:
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.pyplot as plt, matplotlib.gridspec as gridspec
    from matplotlib.dates import date2num
except ImportError:
    pass

WINDOW = 300

class NuPICOutput(object):
    __metaclass__ = ABCMeta

    def __init__(self, names, showAnomalyScore=False):
        self.names = names
        self.showAnomalyScore = showAnomalyScore

    @abstractmethod
    def write(self, timestamps, actualValues, predictedValues, predictionStep=1):
        pass

    @abstractmethod
    def close(self):
        pass


class NuPICFileOutput(NuPICOutput):

    def __init__(self, *args, **kwargs):
        super(NuPICFileOutput, self).__init__(*args, **kwargs)
        self.outputFiles = []
        self.outputWriters = []
        self.lineCounts = []
        headerRow = ['timestamp', 'value', 'prediction']
        for name in self.names:
            self.lineCounts.append(0)
            outputFileName = os.path.join(name, 'predictions.csv')
            print 'Preparing to output %s data to %s' % (name, outputFileName)
            outputFile = open(outputFileName, 'w')
            self.outputFiles.append(outputFile)
            outputWriter = csv.writer(outputFile)
            self.outputWriters.append(outputWriter)
            outputWriter.writerow(headerRow)

    def write(self, timestamps, actualValues, predictedValues, predictionStep=1):
        assert len(timestamps) == len(actualValues) == len(predictedValues)
        for index in range(len(self.names)):
            timestamp = timestamps[index]
            actual = actualValues[index]
            prediction = predictedValues[index]
            writer = self.outputWriters[index]
            if timestamp is not None:
                outputRow = [
                 timestamp, actual, prediction]
                writer.writerow(outputRow)
                self.lineCounts[index] += 1

        return

    def close(self):
        for index, name in enumerate(self.names):
            self.outputFiles[index].close()
            print 'Done. Wrote %i data lines to %s.' % (self.lineCounts[index], name)


class NuPICPlotOutput(NuPICOutput):

    def __init__(self, *args, **kwargs):
        super(NuPICPlotOutput, self).__init__(*args, **kwargs)
        plt.ion()
        self.dates = []
        self.convertedDates = []
        self.actualValues = []
        self.predictedValues = []
        self.actualLines = []
        self.predictedLines = []
        self.linesInitialized = False
        self.graphs = []
        plotCount = len(self.names)
        plotHeight = max(plotCount * 3, 6)
        fig = plt.figure(figsize=(14, plotHeight))
        gs = gridspec.GridSpec(plotCount, 1)
        for index in range(len(self.names)):
            self.graphs.append(fig.add_subplot(gs[(index, 0)]))
            plt.title(self.names[index])
            plt.ylabel(*args[0])
            plt.xlabel('Date')

        plt.tight_layout()

    def initializeLines(self, timestamps):
        for index in range(len(self.names)):
            print 'initializing %s' % self.names[index]
            self.dates.append(deque([timestamps[index]] * WINDOW, maxlen=WINDOW))
            self.convertedDates.append(deque([ date2num(date) for date in self.dates[index] ], maxlen=WINDOW))
            self.actualValues.append(deque([0.0] * WINDOW, maxlen=WINDOW))
            self.predictedValues.append(deque([0.0] * WINDOW, maxlen=WINDOW))
            actualPlot, = self.graphs[index].plot(self.dates[index], self.actualValues[index])
            self.actualLines.append(actualPlot)
            predictedPlot, = self.graphs[index].plot(self.dates[index], self.predictedValues[index])
            self.predictedLines.append(predictedPlot)

        self.linesInitialized = True

    def write(self, timestamps, actualValues, predictedValues, predictionStep=1):
        if not len(timestamps) == len(actualValues) == len(predictedValues):
            raise AssertionError
            self.linesInitialized or self.initializeLines(timestamps)
        for index in range(len(self.names)):
            self.dates[index].append(timestamps[index])
            self.convertedDates[index].append(date2num(timestamps[index]))
            self.actualValues[index].append(actualValues[index])
            self.predictedValues[index].append(predictedValues[index])
            self.actualLines[index].set_xdata(self.convertedDates[index])
            self.actualLines[index].set_ydata(self.actualValues[index])
            self.predictedLines[index].set_xdata(self.convertedDates[index])
            self.predictedLines[index].set_ydata(self.predictedValues[index])
            self.graphs[index].relim()
            self.graphs[index].autoscale_view(True, True, True)

        plt.draw()
        plt.legend(('actual', 'predicted'), loc=3)

    def close(self):
        plt.ioff()
        plt.show()


NuPICOutput.register(NuPICFileOutput)
NuPICOutput.register(NuPICPlotOutput)