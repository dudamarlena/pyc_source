# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/EPD64.framework/Versions/7.0/lib/python2.7/site-packages/pyspec/gda.py
# Compiled at: 2011-02-13 14:08:59
import time, sys, os
from numpy import *
from scipy import *
from pylab import *

class gdaScan:

    def __init__(self, scannumber):
        """
                Read scan data and set variables
                to all the data contained in the scan
                
                """
        scan = '%05d' % scannumber
        self.filename = ('').join([scan, '.dat'])
        self.scandata = gdaData()
        self.data = []
        self.values = {}
        self.line = ''
        self.scanfile = open(self.filename)
        self.readheader()
        self.readdata()
        self.scanfile.close()

    def readheader(self):
        self.line = self.scanfile.readline()
        while self.line[0:17] != '<MetaDataAtStart>':
            self.line = self.scanfile.readline()
            if self.line[0:5] == ' &END':
                print 'No metadata in this scan file'
                return

        self.line = self.scanfile.readline()
        while self.line[0:18] != '</MetaDataAtStart>':
            if self.line == '' or self.line == '\n':
                self.line = self.scanfile.readline()
            pos = self.line.split('=')
            if self.is_number(pos[1]) == True:
                self.scandata.setValue(pos[0], float(pos[1]))
            else:
                self.scandata.setValue(pos[0], pos[1])
            self.line = self.scanfile.readline()

    def readdata(self):
        while self.line[0:5] != ' &END':
            self.line = self.scanfile.readline()

        self.line = self.scanfile.readline()
        self.cols = self.line.split('\t')
        self.cols[-1] = self.cols[(-1)].rstrip('\n')
        self.line = self.scanfile.readline()
        while self.line != '':
            dataline = self.line.split('\t')
            dataline[-1] = dataline[(-1)].rstrip('\n')
            dataArray = zeros(len(dataline))
            for ii in range(0, len(dataline)):
                dataArray[ii] = float(dataline[ii])

            if self.data == []:
                self.data = dataArray
            else:
                self.data = vstack([self.data, dataArray])
            self.line = self.scanfile.readline()

        for ii in range(0, len(self.cols)):
            self.scandata.setValue(self.cols[ii], self.data[:, ii])

        for i in self.scandata.values.keys():
            setattr(self, i, self.scandata.values[i])

    def show(self):
        """
                Show statistics on scan
                """
        print 'Datafile:'
        print self.filename
        self.scandata.show()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


class gdaData:

    def __init__(self):
        self.values = {}

    def __call__(self, key):
        print key

    def setValue(self, key, data, setdata=True):
        self.values[key] = data

    def get(self, key):
        if self.values.has_key(key):
            return self.values[key]
        else:
            return
            return

    def show(self):
        """
                Show statistics on data (motors, scalars)
                
                example   : SpecData.show()
                """
        print 'Header Variables'
        for i in self.values.keys():
            if self.values[i].shape == (1, ):
                print '%10s ' % i,

        print 'Scan Variables:'
        for i in self.values.keys():
            if self.values[i].shape != (1, ):
                print '%10s ' % i,

        return