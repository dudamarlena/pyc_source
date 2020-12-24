# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pifi/SpectrumAnalyzer.py
# Compiled at: 2014-10-22 23:55:44
import numpy, time, logging
MPD_FIFO = '/tmp/mpd.fifo'
SAMPLE_SIZE = 256
SAMPLING_RATE = 44100
FIRST_SELECTED_BIN = 5
NUMBER_OF_SELECTED_BINS = 10
SCALE_WIDTH = 20.0

def moveCursorTo(new_x, new_y):
    """Move cursor to new_x, new_y"""
    print '\x1b[' + str(new_x) + ';' + str(new_y) + 'H',


def displayConsole(spectrumValues):
    print '\x1b[2J',
    print '\x1b[?25l',
    moveCursorTo(0, 0)
    for val in spectrumValues:
        print '=' * val

    time.sleep(0.05)


class SpectrumAnalyzer(object):

    def __init__(self, sampleSize, samplingRate, firstSelectedBin, numberOfSelectedBins):
        self.sampleSize = sampleSize
        self.samplingRate = samplingRate
        self.firstSelectedBin = firstSelectedBin
        self.numberOfSelectedBins = numberOfSelectedBins
        freq = numpy.fft.fftfreq(sampleSize) * samplingRate
        freqR = freq[:sampleSize / 2]
        self.bins = freqR[firstSelectedBin:firstSelectedBin + numberOfSelectedBins]
        self.resetSmoothing()

    def resetSmoothing(self):
        self.count = 0
        self.average = 0
        logging.debug('Reset smoothing')

    def smoothOut(self, x):
        self.count += 1
        self.average = (self.average * self.count + x) / (self.count + 1)
        return self.average

    def scaleList(self, list, scaleWidth):
        list[numpy.isnan(spectrum)] = 0
        list[numpy.isinf(spectrum)] = 0
        maximum = 1.1 * self.smoothOut(max(list))
        if maximum == 0:
            scaleFactor = 0.0
        else:
            scaleFactor = scaleWidth / float(maximum)
        scaledList = [ int(x * scaleFactor) for x in list ]
        return scaledList

    def computeRMS(self, fifoFile, scaleWidth):
        rawSamples = fifoFile.read(self.sampleSize)
        pcm = numpy.fromstring(rawSamples, dtype=numpy.int16)
        pcm = pcm / 32768.0
        rms = numpy.sqrt(numpy.mean(pcm ** 2))
        maximum = 2 * self.smoothOut(rms)
        if maximum == 0:
            scaleFactor = 0.0
        else:
            scaleFactor = scaleWidth / float(maximum)
        return int(rms * scaleFactor)

    def computeSpectrum(self, fifoFile, scaleWidth):
        rawSamples = fifoFile.read(self.sampleSize)
        pcm = numpy.fromstring(rawSamples, dtype=numpy.int16)
        pcm = pcm / 32768.0
        N = pcm.size
        fft = numpy.fft.fft(pcm)
        uniquePts = numpy.ceil((N + 1) / 2.0)
        fft = fft[0:uniquePts]
        amplitudeSpectrum = numpy.abs(fft) / float(N)
        p = amplitudeSpectrum ** 2
        if N % 2 > 0:
            p[1:(len(p))] = p[1:len(p)] * 2
        else:
            p[1:(len(p) - 1)] = p[1:len(p) - 1] * 2
        logPower = 10 * numpy.log10(p)
        spectrum = logPower[self.firstSelectedBin:self.firstSelectedBin + self.numberOfSelectedBins]
        scaledSpectrum = self.scaleList(spectrum, scaleWidth)
        return (
         self.bins, scaledSpectrum)

    def ComputeLevels(data, chunk, samplerate):
        fmt = '%dH' % (len(data) / 2)
        data2 = struct.unpack(fmt, data)
        data2 = numpy.array(data2, dtype='h')
        fourier = numpy.fft.fft(data2)
        ffty = numpy.abs(fourier[0:len(fourier) / 2]) / 1000
        ffty1 = ffty[:len(ffty) / 2]
        ffty2 = ffty[len(ffty) / 2::] + 2
        ffty2 = ffty2[::-1]
        ffty = ffty1 + ffty2
        ffty = numpy.log(ffty) - 2
        fourier = list(ffty)[4:-4]
        fourier = fourier[:len(fourier) / 2]
        size = len(fourier)
        levels = [ sum(fourier[i:i + size / 6]) for i in xrange(0, size, size / 6) ][:6]
        return levels


if __name__ == '__main__':
    analyzer = SpectrumAnalyzer(SAMPLE_SIZE, SAMPLING_RATE, FIRST_SELECTED_BIN, NUMBER_OF_SELECTED_BINS)
    with open(MPD_FIFO) as (fifo):
        while True:
            bins, scaledSpectrum = analyzer.computeSpectrum(fifo, SCALE_WIDTH)
            displayConsole(scaledSpectrum)