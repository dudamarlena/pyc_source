# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/EPD64.framework/Versions/7.0/lib/python2.7/site-packages/pyspec/hasy.py
# Compiled at: 2011-02-13 14:08:59
"""
Python module for handling of HASYLAB data files.

Written by TAW Beale

Written for Spectra data files, as used on BW5, hasylab.   
Here call HASY, rather than SPECTRA to avoid confusion with SPEC.

This is distinctly different from spec.py (in pyspec) as each scan at HASYLAB is 
held in an individual file.    Therefore the name of the file is passed
to the routine.

Example:

        # Load datafile and index
        
        scan = HasyScanFile('fourc.01')         
        
        # Access to variables
        
        scan.data                                                       
        scan.values['TTH']                                       
        scan.TTH                                                        

        # access to suplimentary information
        
        scan.header                                                                             

"""
import time, sys, os
from numpy import *
from scipy import *
from pylab import *
__verbose__ = 1
NoFile = 'Scan file does not exist'

def removeIllegals(key):
    illegal = [
     '/', '-', ' ']
    for j in illegal:
        key = key.replace(j, '')

    if key[0].isalpha() == False:
        key = 'X' + key
    return key


class HasyScanFile:
    """
        Datafile class for handling a HASYLAB file
        """

    def __init__(self, prefix, scan):
        """
                Read scan data from Data class and set variables
                to all the data contained in the scan
                
                """
        self.prefix = prefix
        self.suffix = '.fio'
        self.scanno = scan
        self.dir = dir
        self.constructfilename()
        self.readheader()
        self.readdata()
        self.file.close()

    def constructfilename(self):
        """
                Construct the filename from the scan number and prefix
                """
        sc = '%05d' % self.scanno
        self.filename = ('').join([self.prefix, '_', sc, self.suffix])

    def readheader(self):
        """
                 Read the hasylab header from file 
                """
        self.file = open(self.filename, 'r')
        if __verbose__:
            print '...reading scan', self.filename
        self.motors = {}
        self.file.seek(0, 0)
        line = self.file.readline()
        while line[0:2] != '%c':
            line = self.file.readline()

        line = self.file.readline()
        self.header = ''
        while line[0:2] != '%p':
            if line[0:1] != '!':
                self.header = self.header + line
                if line[0:5] == ' Name':
                    time = line.split('sampling')
                    self.time = float(time[1].split('s')[0])
                if line[0:12] == ' lattice-par':
                    self.lattice = [ float(s) for s in line[14:-1].split('  ') ]
            line = self.file.readline()

        line = self.file.readline()
        while line[0:2] != '%d':
            if line[0:1] != '!':
                br = line.split('=')
                br[1] = br[1].replace('\n', '')
                br[0] = removeIllegals(br[0])
                self.motors[br[0]] = float(br[1])
            line = self.file.readline()

    def readdata(self):
        """
                Read the colomn data from the datafile
                """
        kk = 0
        self.columns = []
        self.data = []
        line = self.file.readline()
        while line[0:5] == ' Col ':
            self.columns.append(line)
            line = self.file.readline()

        dataline = zeros((1, len(self.columns)))
        while line != '':
            br = line.split(' ')
            jj = 0
            for ii in range(0, len(br) - 1):
                if br[ii][0:1] != ' ':
                    if br[ii] != '':
                        dataline[(0, jj)] = float(br[ii])
                        jj = jj + 1

            if self.data == []:
                self.data = dataline
            self.data = vstack((self.data, dataline))
            if kk == 0:
                self.data = self.data[0, :]
                kk = 1
            line = self.file.readline()

        self.x = self.data[:, 0]
        self.y = self.data[:, 1]
        for n in range(0, len(self.columns) - 1):
            exist = self.columns[n].find('DORIS')
            if exist != -1:
                self.doris = self.data[:, n]

        for n in range(0, len(self.columns) - 1):
            exist = self.columns[n].find('C6')
            if exist != -1:
                self.diode = self.data[:, n]

        for n in range(0, len(self.columns) - 1):
            exist = self.columns[n].find('T_CONTROL')
            if exist != -1:
                self.treg = self.data[:, n]

        for n in range(0, len(self.columns) - 1):
            exist = self.columns[n].find('T_SAMPLE')
            if exist != -1:
                self.tsam = self.data[:, n]