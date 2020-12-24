# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/EPD64.framework/Versions/7.0/lib/python2.7/site-packages/pyspec/ccd/specext.py
# Compiled at: 2011-02-21 19:54:27
import os, numpy
from pyspec.spec import SpecExtension

class CCDSpecExtension(SpecExtension):

    def __init__(self):
        self.ccddark = '-DARK'
        self.ccdpath = None
        self.ccdtail = '.spe'
        return

    def initSpec(self, object):
        object.ccdpath = self.ccdpath
        object.ccddark = self.ccddark
        object.ccdtail = self.ccdtail

    def initSpecScan(self, object):
        object.ccdAcquireTime = 0.0
        object.ccdAcquirePeriod = 0.0
        object.ccdNumExposures = 1
        object.ccdNumImages = 1
        object.ccdNumAcquisitions = 1

    def getName(self):
        return 'SPEC / EPICS CCD Extension'

    def parseSpecScanHeader(self, object, line):
        if line[0:6] == '#UCCD2':
            print '---- Reading CCD Header information'
            try:
                pos = line[6:].strip().split()
                pos = map(float, pos)
            except:
                print '**** Unable to parse CCD data (UCCD2)'
                return

            object.ccdAcquireTime = pos[0]
            object.ccdAcquirePeriod = pos[1]
            object.ccdNumExposures = int(pos[2])
            object.ccdNumImages = int(pos[3])
            if hasattr(object, 'ccdSubImages'):
                print '---- CCD Sub Images set to %d' % object.ccdSubImages
                object.ccdNumAcquisitions = object.ccdSubImages
            else:
                object.ccdNumAcquisitions = int(pos[4])

    def concatenateSpecScan(self, object, a):
        object.ccdAcquireTime = numpy.concatenate((object.ccdAcquireTime, a.ccdAcquireTime))
        object.ccdAcquirePeriod = numpy.concatenate((object.ccdAcquirePeriod, a.ccdAcquirePeriod))
        object.ccdNumExposures = numpy.concatenate((object.ccdNumExposures, a.ccdNumExposures))
        object.ccdNumImages = numpy.concatenate((object.ccdNumImages, a.ccdNumImages))
        object.ccdNumAcquisitions = numpy.concatenate((object.ccdNumAcquisitions, a.ccdNumAcquisitions))
        object.ccdFilenames = object.ccdFilenames + a.ccdFilenames
        object.ccdDarkFilenames = object.ccdDarkFilenames + a.ccdDarkFilenames

    def postProcessSpecScanHeader(self, object):
        object.ccdAcquireTime = numpy.ones(object.data.shape[0]) * object.ccdAcquireTime
        object.ccdAcquirePeriod = numpy.ones(object.data.shape[0]) * object.ccdAcquirePeriod
        object.ccdNumExposures = numpy.ones(object.data.shape[0], dtype=numpy.int) * object.ccdNumExposures
        object.ccdNumImages = numpy.ones(object.data.shape[0], dtype=numpy.int) * object.ccdNumImages
        object.ccdNumAcquisitions = numpy.ones(object.data.shape[0], dtype=numpy.int) * object.ccdNumAcquisitions
        if object.datafile.ccdpath is not None:
            _path = object.datafile.ccdpath + os.sep
        else:
            _path = ''
        _datafile = object.datafile.filename.split(os.sep)
        if object.data.ndim == 1:
            ndps = 1
        else:
            ndps = object.data.shape[0]
        allfilenames = []
        for dark in ['', object.datafile.ccddark]:
            filenames = []
            for i, scan, cna in zip(object.scandatum, object.scanno, object.ccdNumAcquisitions):
                _fnames = []
                for j in range(cna):
                    _f = '%s_%04d-%04d%s_%04d%s' % (_datafile[(-1)],
                     scan,
                     i,
                     dark,
                     j,
                     object.datafile.ccdtail)
                    _fnames.append('%s%s' % (_path, _f))

                filenames.append(_fnames)

            allfilenames.append(filenames)

        object.ccdFilenames = allfilenames[0]
        object.ccdDarkFilenames = allfilenames[1]
        return