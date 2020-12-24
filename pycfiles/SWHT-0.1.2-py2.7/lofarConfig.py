# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SWHT/lofarConfig.py
# Compiled at: 2018-01-09 05:04:50
"""
Functions and classes to read and parse LOFAR station configuration files
"""
import numpy as np, glob, os, struct
STATICMETADATA = __file__.split('lofarConfig.py')[0] + 'data/LOFAR/StaticMetaData/'
rcuInfo = [{'mode': 'OFF', 'rcuID': 0, 'array_type': 'LBA', 'bw': 100000000.0, 'offset': 0.0, 'nchan': 512}, {'mode': 'LBL_HPF10MHZ', 'rcuID': 1, 'array_type': 'LBA', 'bw': 100000000.0, 'offset': 0.0, 'nchan': 512}, {'mode': 'LBL_HPF30MHZ', 'rcuID': 2, 'array_type': 'LBA', 'bw': 100000000.0, 'offset': 0.0, 'nchan': 512}, {'mode': 'LBH_HPF10MHZ', 'rcuID': 3, 'array_type': 'LBA', 'bw': 100000000.0, 'offset': 0.0, 'nchan': 512}, {'mdde': 'LBH_HPF30MHZ', 'rcuID': 4, 'array_type': 'LBA', 'bw': 100000000.0, 'offset': 0.0, 'nchan': 512}, {'mode': 'HBA_110_190MHZ', 'rcuID': 5, 'array_type': 'HBA', 'bw': 100000000.0, 'offset': 100000000.0, 'nchan': 512}, {'mode': 'HBA_170_230MHZ', 'rcuID': 6, 'array_type': 'HBA', 'bw': 80000000.0, 'offset': 160000000.0, 'nchan': 512}, {'mode': 'HBA_210_290MHZ', 'rcuID': 7, 'array_type': 'HBA', 'bw': 100000000.0, 'offset': 200000000.0, 'nchan': 512}]

def getLofarStation(name=None, affn=None, aafn=None, deltas=None, noarrays=True):
    """Create an instance of the lofarStation class based on a station name and the configuration repo, or from the antenna array and field files
    name: station name (required if no filenames used)
    affn, aafn: AntennaArray filename, AntennaField filename (required if station name is not used)
    deltas: HBA tile deltas filename, optional, only used in HBA imaging
    noarrays: do not require a *-AntennaArrays.conf file
    """
    nameValid = False
    confValid = False
    dfn = None
    if name is not None:
        repoaafn = glob.glob(STATICMETADATA + name + '-AntennaArrays.conf')
        repoaffn = glob.glob(STATICMETADATA + name + '-AntennaField.conf')
        repodfn = glob.glob(STATICMETADATA + name + '-iHBADeltas.conf')
        if len(repoaffn) == 1 and noarrays:
            repoaffn = repoaffn[0]
            repoaafn = None
            nameValid = True
        elif len(repoaafn) == 1 and len(repoaffn) == 1:
            repoaafn = repoaafn[0]
            repoaffn = repoaffn[0]
            nameValid = True
        if len(repodfn) == 1:
            dfn = repodfn[0]
    if affn is not None and aafn is not None:
        confValid = True
    if nameValid is False and confValid is False:
        print 'ERROR: input station name or configuration files are no good, exiting'
        exit()
    if deltas is not None:
        dfn = deltas
    if confValid:
        stationName = affn.split('/')[(-1)].split('-')[0]
        print 'Station Name:', stationName
        print 'AntennaArray:', aafn
        print 'AntennaField:', affn
        print 'iHBADeltas:', dfn
        return lofarStation(stationName, affn, aafn, deltas=dfn)
    else:
        if nameValid:
            print 'Station Name:', name
            print 'AntennaArray:', repoaafn
            print 'AntennaField:', repoaffn
            print 'iHBADeltas:', dfn
            return lofarStation(name, repoaffn, repoaafn, deltas=dfn)
        return


class lofarStation:

    def __init__(self, name, affn, aafn=None, deltas=None):
        """deltas: optional HBA deltas file
        """
        self.name = name
        self.antField = antennaField(name, affn)
        if aafn is not None:
            self.antArrays = antennaArrays(name, aafn)
        if deltas is not None:
            self.deltas = getHBADeltas(deltas)
        else:
            self.deltas = None
        if name.lower().startswith('cs'):
            self.stype = 'core'
        elif name.lower().startswith('rs'):
            self.stype = 'remote'
        elif name.lower().startswith('kaira'):
            self.stype = 'kaira'
        else:
            self.stype = 'international'
        return


def getHBADeltas(fn):
    """Interface to a 16x3 delta offset XYZ  position for the elements of an HBA tile relative to the position in antennaField
    """
    fh = open(fn)
    lines = []
    lines = fh.read().split('\n')
    fh.close()
    cleanStr = ''
    for l in lines:
        if l == '' or l.startswith('#'):
            continue
        cleanStr += (' ').join(l.split()) + ' '

    cleanStr = (' ').join(cleanStr.split())
    return np.array(map(float, cleanStr.split(' ')[5:-1])).reshape((16, 3))


class antennaField:

    def __init__(self, name, fn):
        self.name = name
        self.rotMatrix = {}
        self.normVec = {}
        self.antpos = {}
        self.localAntPos = {}
        self.location = {}
        fh = open(fn)
        lines = []
        lines = fh.read().split('\n')
        fh.close()
        cleanStr = ''
        for l in lines:
            if l == '' or l.startswith('#'):
                continue
            cleanStr += (' ').join(l.split()) + ' '

        cleanStr = (' ').join(cleanStr.split())
        lastMode = None
        for l in cleanStr.split(']'):
            if l == '':
                continue
            infoStr, dataStr = l.split('[')
            infoStr = infoStr.strip()
            if infoStr.lower().startswith('normal'):
                name, mode, length = infoStr.split(' ')
                self.normVec[mode] = np.array(map(float, dataStr.strip().split(' ')))
            elif infoStr.lower().startswith('rotation'):
                name, mode, l0, fill, l1 = infoStr.split(' ')
                if len(l0) == 1:
                    self.rotMatrix[mode] = np.array(map(float, dataStr.strip().split(' '))).reshape((int(l0), int(l1)))
                else:
                    l0 = l0.split(',')[(-1)][:-1]
                    l1 = l1.split(',')[(-1)][:-1]
                    self.rotMatrix[mode] = np.array(map(float, dataStr.strip().split(' '))).reshape((int(l0) + 1, int(l1) + 1))
            elif infoStr.lower().startswith('lba') or infoStr.lower().startswith('hba'):
                mode, length = infoStr.split(' ')
                self.location[mode] = np.array(map(float, dataStr.strip().split(' ')))
                lastMode = mode
            else:
                l0, f0, l1, f1, l2 = infoStr.split(' ')
                print l0, f0, l1, f1, l2
                if len(l0) < 3:
                    self.antpos[lastMode] = np.array(map(float, dataStr.strip().split(' '))).reshape((int(l0), int(l1), int(l2)))
                else:
                    l0 = l0.split(',')[(-1)][:-1]
                    l1 = l1.split(',')[(-1)][:-1]
                    l2 = l2.split(',')[(-1)][:-1]
                    self.antpos[lastMode] = np.array(map(float, dataStr.strip().split(' '))).reshape((int(l0) + 1, int(l1) + 1, int(l2) + 1))

        for mode in self.antpos:
            for rkey in self.rotMatrix:
                if mode.startswith(rkey):
                    rotMode = mode
                    continue

            self.localAntPos[mode] = np.zeros_like(self.antpos[mode])
            self.localAntPos[mode][:, 0, :] = np.linalg.lstsq(self.rotMatrix[rotMode], self.antpos[mode][:, 0, :].T)[0].T
            self.localAntPos[mode][:, 1, :] = np.linalg.lstsq(self.rotMatrix[rotMode], self.antpos[mode][:, 1, :].T)[0].T

        return


class antennaArrays:

    def __init__(self, name, fn):
        """Parse the AntenneArrays file, most of the informationis redundant to the AntennaField file, but contains the (lat, long, height)
        DEPRECIATED: these files were used to get the station (lat, lon, h) only, but that is now computed with the array X,Y,Z positions in antennaField() using ecef.py
        """
        self.name = name
        self.antpos = {}
        self.location = {}
        fh = open(fn)
        lines = []
        lines = fh.read().split('\n')
        fh.close()
        cleanStr = ''
        for l in lines:
            if l == '' or l.startswith('#'):
                continue
            cleanStr += (' ').join(l.split()) + ' '

        cleanStr = (' ').join(cleanStr.split())
        lastMode = None
        for l in cleanStr.split(']'):
            if l == '':
                continue
            infoStr, dataStr = l.split('[')
            infoStr = infoStr.strip()
            if infoStr.lower().startswith('lba') or infoStr.lower().startswith('hba'):
                mode, length = infoStr.split(' ')
                self.location[mode] = np.array(map(float, dataStr.strip().split(' ')))
                lastMode = mode
            else:
                l0, f0, l1, f1, l2 = infoStr.split(' ')
                self.antpos[lastMode] = np.array(map(float, dataStr.strip().split(' '))).reshape((int(l0), int(l1), int(l2)))

        return


def rotationMatrix(alpha, beta, gamma):
    """Generic rotation matrix to apply to an XYZ co-ordinate"""
    return np.matrix([[np.cos(beta) * np.cos(gamma), np.cos(gamma) * np.sin(alpha) * np.sin(beta) - np.cos(alpha) * np.sin(gamma), np.cos(alpha) * np.cos(gamma) * np.sin(beta) + np.sin(alpha) * np.sin(gamma)],
     [
      np.cos(beta) * np.sin(gamma), np.cos(alpha) * np.cos(gamma) + np.sin(alpha) * np.sin(beta) * np.sin(gamma), -1.0 * np.cos(gamma) * np.sin(alpha) + np.cos(alpha) * np.sin(beta) * np.sin(gamma)],
     [
      -1.0 * np.sin(beta), np.cos(beta) * np.sin(alpha), np.cos(alpha) * np.cos(beta)]])


def rotMatrixfromXYZ(station, mode='LBA'):
    """Return a rotation matrix which will rotate a station to (0,0,1)"""
    loc = station.antField.location[mode]
    longRotMat = rotationMatrix(0.0, 0.0, -1.0 * np.arctan(loc[1] / loc[0]))
    loc0 = np.dot(longRotMat, loc)
    latRotMat = rotationMatrix(0.0, np.arctan(loc0[(0, 2)] / loc0[(0, 0)]), 0.0)
    return np.dot(latRotMat, longRotMat)


def applyRotMatrix(station, rm, mode='LBA'):
    """Apply a rotation matrix to a station location, returns new location after apply rotation matrix"""
    loc = station.antField.location[mode]
    return np.dot(rm, loc)


def relativeStationOffset(s0, s1, mode='LBA'):
    """Return the relative offset of station s1 from station s0"""
    rotMat = rotMatrixfromXYZ(s0, 'LBA')
    s0loc = applyRotMatrix(s0, rotMat, mode)
    s1loc = applyRotMatrix(s1, rotMat, mode)
    return np.array(s1loc - s0loc)[0][::-1]


def readCalTable(fn, nants=96, nsbs=512, npols=2):
    """Parse a LOFAR Calibration Table
    return: [NSBS, NANTS * NPOLS] complex array, the X and Y pols are interlaced, not serial, i.e. xGains = antGains[:, 0::2] and yGains = antGains[:, 1::2]
    """
    fh = open(fn)
    line = fh.readline()
    if 'HeaderStart' in line:
        while 'HeaderStop' not in line:
            line = fh.readline()

    else:
        file.seek(0)
    fmt = str(nants * npols * nsbs * 2) + 'd'
    sz = struct.calcsize(fmt)
    antGains = np.array(struct.unpack(fmt, fh.read(sz)))
    fh.close()
    antGains = antGains[0::2] + complex(0.0, 1.0) * antGains[1::2]
    antGains.resize(nsbs, nants * npols)
    return antGains


if __name__ == '__main__':
    print 'Running test cases'
    print 'Using data from this directory:', STATICMETADATA
    deltas = getHBADeltas(STATICMETADATA + 'SE607-iHBADeltas.conf')
    print deltas
    CS013 = lofarStation('CS013', STATICMETADATA + 'CS013-AntennaField.conf', STATICMETADATA + 'CS013-AntennaArrays.conf')
    print CS013.name
    RS208 = lofarStation('RS208', STATICMETADATA + 'RS208-AntennaField.conf', STATICMETADATA + 'RS208-AntennaArrays.conf')
    print RS208.name
    UK608 = lofarStation('UK608', STATICMETADATA + 'UK608-AntennaField.conf', STATICMETADATA + 'UK608-AntennaArrays.conf')
    print UK608.name
    SE607 = lofarStation('SE607', STATICMETADATA + 'SE607-AntennaField.conf')
    print SE607.name
    CS002 = lofarStation('CS002', STATICMETADATA + 'CS002-AntennaField.conf', STATICMETADATA + 'CS002-AntennaArrays.conf')
    CS003 = lofarStation('CS003', STATICMETADATA + 'CS003-AntennaField.conf', STATICMETADATA + 'CS003-AntennaArrays.conf')
    rotMat = rotMatrixfromXYZ(CS002, 'LBA')
    print relativeStationOffset(CS002, CS003)
    print relativeStationOffset(CS002, CS013)
    print relativeStationOffset(CS002, RS208)
    print relativeStationOffset(CS002, UK608)
    getLofarStation(name='SE607')
    getLofarStation(affn=STATICMETADATA + 'SE607-AntennaField.conf', aafn=STATICMETADATA + 'SE607-AntennaArrays.conf')
    getLofarStation(affn=STATICMETADATA + 'SE607-AntennaField.conf', aafn=STATICMETADATA + 'SE607-AntennaArrays.conf', deltas=STATICMETADATA + 'SE607-iHBADeltas.conf')
    KAIRA = getLofarStation(name='KAIRA')
    print KAIRA.antField.antpos['LBA'].shape
    IE613 = getLofarStation(name='IE613')
    print IE613.antField.antpos['LBA'].shape
    print 'Made it through without any errors.'