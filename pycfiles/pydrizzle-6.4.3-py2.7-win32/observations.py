# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\observations.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from pattern import *
from stsci.tools import fileutil
from distortion import mutil
import numpy as np

class ACSObservation(Pattern):
    """This class defines an observation with information specific
       to ACS WFC exposures, including knowledge of how to mosaic both
       chips."""
    PARITY = {'WFC': [[1.0, 0.0], [0.0, -1.0]], 'HRC': [[-1.0, 0.0], [0.0, 1.0]], 'SBC': [[-1.0, 0.0], [0.0, 1.0]]}

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        self.instrument = 'ACS'
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        self.addMembers(filename)
        self.computeOffsets()
        self.buildProduct(filename, output)


class GenericObservation(Pattern):
    """
        This class defines an observation stored in a Simple FITS format;
        i.e., only a Primary header and image without extensions.
    """
    REFPIX = {'x': 512.0, 'y': 512.0}
    DETECTOR_NAME = 'INSTRUME'

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        if 'INSTRUME' in self.header:
            _instrument = self.header['INSTRUME']
        else:
            _instrument = self.DETECTOR_NAME
        self.instrument = _instrument
        if 'crpix1' in self.header:
            self.REFPIX['x'] = self.header['crpix1']
            self.REFPIX['y'] = self.header['crpix2']
        else:
            self.REFPIX['x'] = self.header['naxis1'] / 2.0
            self.REFPIX['y'] = self.header['naxis2'] / 2.0
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        self.nmembers = 1
        self.addMembers(filename)
        _ikey = self.members[0].geometry.ikey
        if _ikey != 'idctab' and _ikey != 'wcs':
            self.computeCubicCoeffs()
        else:
            self.computeOffsets()
        self.buildProduct(filename, output)


class STISObservation(Pattern):
    """This class defines an observation with information specific
       to STIS exposures.
    """
    IDCKEY = 'cubic'
    __theta = 0.0
    __parity = fileutil.buildRotMatrix(__theta) * np.array([[-1.0, 1.0], [-1.0, 1.0]])
    PARITY = {'CCD': __parity, 'NUV-MAMA': __parity, 'FUV-MAMA': __parity}

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        self.instrument = 'STIS'
        self.__theta = 0.0
        self.REFDATA = {'CCD': {'psize': 0.05, 'xoff': 0.0, 'yoff': 0.0, 'v2': -213.999, 'v3': -224.897, 'theta': self.__theta}, 'NUV-MAMA': {'psize': 0.024, 'xoff': 0.0, 'yoff': 0.0, 'v2': -213.999, 'v3': -224.897, 'theta': self.__theta}, 'FUV-MAMA': {'psize': 0.024, 'xoff': 0.0, 'yoff': 0.0, 'v2': -213.999, 'v3': -224.897, 'theta': self.__theta}}
        self.REFPIX = {'x': 512.0, 'y': 512.0}
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        self.addMembers(filename)
        if self.members[0].geometry.ikey != 'idctab':
            self.computeCubicCoeffs()
        else:
            self.computeOffsets()
        self.buildProduct(filename, output)

    def getExptime(self):
        header = fileutil.getHeader(self.name + '[sci,1]')
        _exptime = float(header['EXPTIME'])
        if _exptime == 0.0:
            _exptime = 1.0
        if 'EXPSTART' in header:
            _expstart = float(header['EXPSTART'])
            _expend = float(header['EXPEND'])
        else:
            _expstart = 0.0
            _expend = _exptime
        return (_exptime, _expstart, _expend)


class NICMOSObservation(Pattern):
    """This class defines an observation with information specific
       to NICMOS exposures.
    """
    IDCKEY = 'cubic'
    DETECTOR_NAME = 'camera'
    NUM_IMSET = 5
    __theta = 0.0
    __parity = fileutil.buildRotMatrix(__theta) * np.array([[-1.0, 1.0], [-1.0, 1.0]])
    PARITY = {'1': __parity, '2': __parity, '3': __parity}

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        self.instrument = 'NICMOS'
        self.__theta = 0.0
        self.REFDATA = {'1': {'psize': 0.0432, 'xoff': 0.0, 'yoff': 0.0, 'v2': -296.9228, 'v3': 290.1827, 'theta': self.__theta}, '2': {'psize': 0.076, 'xoff': 0.0, 'yoff': 0.0, 'v2': -319.9464, 'v3': 311.8579, 'theta': self.__theta}, '3': {'psize': 0.203758, 'xoff': 0.0, 'yoff': 0.0, 'v2': -249.817, 'v3': 235.2371, 'theta': self.__theta}}
        self.REFPIX = {'x': 128.0, 'y': 128.0}
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        self.addMembers()
        if self.members[0].geometry.ikey != 'idctab':
            self.computeCubicCoeffs()
        else:
            self.computeOffsets()
        self.buildProduct(filename, output)

    def addMembers(self):
        """ Build rootname for each SCI extension, and
            create the mask image from the DQ extension.
            It would then append a new Exposure object to 'members'
            list for each extension.
        """
        self.detector = detector = str(self.header[self.DETECTOR_NAME])
        if self.pars['section'] == None:
            self.pars['section'] = [
             None] * self.nmembers
        for i in range(self.nmembers):
            _sciname = self.imtype.makeSciName(i + 1, section=self.pars['section'][i])
            _dqname = self.imtype.makeDQName(i + 1)
            _extname = self.imtype.dq_extname
            _masklist = []
            _masknames = []
            _maskname = buildmask.buildMaskName(_dqname, i + 1)
            _masknames.append(_maskname)
            outmask = buildmask.buildMaskImage(_dqname, self.bitvalue[0], _maskname, extname=_extname, extver=i + 1)
            _masklist.append(outmask)
            _maskname = _maskname.replace('final_mask', 'single_mask')
            _masknames.append(_maskname)
            outmask = buildmask.buildMaskImage(_dqname, self.bitvalue[1], _maskname, extname=_extname, extver=i + 1)
            _masklist.append(outmask)
            _masklist.append(_masknames)
            self.members.append(Exposure(_sciname, idckey=self.idckey, dqname=_dqname, mask=_masklist, pa_key=self.pa_key, parity=self.PARITY[detector], idcdir=self.pars['idcdir'], group_indx=i + 1, handle=self.image_handle, extver=i + 1, exptime=self.exptime[0], ref_pscale=self.REFDATA[self.detector]['psize'], mt_wcs=self.pars['mt_wcs']))

        return


class WFC3Observation(Pattern):
    """This class defines an observation with information specific
       to ACS WFC exposures, including knowledge of how to mosaic both
       chips."""
    PARITY = {'UVIS': [[-1.0, 0.0], [0.0, 1.0]], 'IR': [[-1.0, 0.0], [0.0, 1.0]]}

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        self.instrument = 'WFC3'
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        self.addMembers(filename)
        self.computeOffsets()
        self.buildProduct(filename, output)


class WFPCObservation(Pattern):
    """This class defines an observation with information specific
       to WFPC2 exposures, including knowledge of how to mosaic the
       chips."""
    IDCKEY = 'idctab'
    __pmat = np.array([[-1.0, 0.0], [0.0, 1.0]])
    __refchip = 3
    PARITY = {'1': __pmat, '2': __pmat, '3': __pmat, '4': __pmat, 'WFPC': __pmat}
    NUM_IMSET = 1

    def __init__(self, filename, output, pars=None):
        Pattern.__init__(self, filename, output=output, pars=pars)
        self.instrument = 'WFPC2'
        self.REFDATA = {'1': {'psize': 0.04554, 'xoff': 354.356, 'yoff': 343.646, 'v2': 2.374, 'v3': -30.268, 'theta': 224.848}, '2': {'psize': 0.0996, 'xoff': 345.7481, 'yoff': 375.28818, 'v2': -51.368, 'v3': -5.698, 'theta': 314.352}, '3': {'psize': 0.0996, 'xoff': 366.56876, 'yoff': 354.79435, 'v2': 0.064, 'v3': 48.692, 'theta': 44.67}, '4': {'psize': 0.0996, 'xoff': 355.85016, 'yoff': 351.29183, 'v2': 55.044, 'v3': -6.098, 'theta': 135.221}}
        self.REFPIX = {'x': 400.0, 'y': 400.0}
        gcount = None
        self.setNames(filename, output)
        self.exptime = self.getExptime()
        _mode = fileutil.getKeyword(filename, 'MODE')
        if _mode == 'AREA':
            self.binned = 2
            if self.idckey == 'cubic':
                for l in self.REFPIX.keys():
                    self.REFPIX[l] = self.REFPIX[l] / self.binned

                for l in self.REFDATA.keys():
                    self.REFDATA[l]['psize'] = self.REFDATA[l]['psize'] * self.binned
                    self.REFDATA[l]['xoff'] = self.REFDATA[l]['xoff'] / self.binned
                    self.REFDATA[l]['yoff'] = self.REFDATA[l]['yoff'] / self.binned

        self.addMembers(filename)
        self.setBunit('COUNTS')
        chips = [ int(member.chip) for member in self.members ]
        try:
            chip_ind = chips.index(self.__refchip)
        except ValueError:
            chip_ind = 0

        self.refchip = chips[chip_ind]
        if self.members[0].geometry.ikey != 'idctab':
            self.computeCubicCoeffs()
        else:
            self.computeOffsets(refchip=self.refchip)
        self.setOrient()
        self.buildProduct(filename, output)
        return

    def addMembers(self, filename):
        self.detector = 'WFPC'
        _chip1_rot = None
        if self.pars['section'] == None:
            self.pars['section'] = [
             None] * self.nmembers
            group_indx = range(1, self.nmembers + 1)
        else:
            group_indx = self.pars['section']
        for i in range(self.nmembers):
            _extname = self.imtype.makeSciName(i + 1, section=self.pars['section'][i])
            _detnum = fileutil.getKeyword(_extname, self.DETECTOR_NAME)
            _dqfile, _dqextn = self._findDQFile()
            self.imtype.dqfile = _dqfile
            self.imtype.dq_extn = _dqextn
            _dqname = self.imtype.makeDQName(extver=group_indx[i])
            _masklist = []
            _masknames = []
            if _dqname != None:
                _maskname = buildmask.buildMaskName(fileutil.buildNewRootname(_dqname), _detnum)
            else:
                _maskname = None
            _masknames.append(_maskname)
            outmask = buildmask.buildShadowMaskImage(_dqname, _detnum, group_indx[i], _maskname, bitvalue=self.bitvalue[0], binned=self.binned)
            _masklist.append(outmask)
            _maskname = _maskname.replace('final_mask', 'single_mask')
            _masknames.append(_maskname)
            outmask = buildmask.buildShadowMaskImage(_dqname, _detnum, group_indx[i], _maskname, bitvalue=self.bitvalue[1], binned=self.binned)
            _masklist.append(outmask)
            _masklist.append(_masknames)
            self.members.append(Exposure(_extname, idckey=self.idckey, dqname=_dqname, mask=_masklist, parity=self.PARITY[str(i + 1)], idcdir=self.pars['idcdir'], group_indx=i + 1, rot=_chip1_rot, handle=self.image_handle, extver=_detnum, exptime=self.exptime[0], ref_pscale=self.REFDATA['1']['psize'], binned=self.binned))
            if self.idckey != 'idctab':
                _chip1_rot = self.members[0].geometry.def_rot

        return

    def _findDQFile(self):
        """ Find the DQ file which corresponds to the input WFPC2 image. """
        dqfile = ''
        dqextn = ''
        if self.name.find('.fits') < 0:
            dqfile = self.name[:-2] + '1h'
            dqextn = '[sdq,1]'
        elif 'c0h.fits' in self.name:
            dqfile = self.name.replace('0h.fits', '1h.fits')
            dqextn = '[sdq,1]'
        elif 'c0f.fits' in self.name:
            dqfile = self.name.replace('0f.fits', '1f.fits')
            dqextn = '[sci,1]'
        elif 'c0m.fits' in self.name:
            dqfile = self.name.replace('0m.fits', '1m.fits')
            dqextn = '[sci,1]'
        return (dqfile, dqextn)

    def setOrient(self):
        """ Determine desired orientation of product."""
        meta_orient = None
        for exp in self.members:
            if int(exp.chip) == 1:
                meta_orient = exp.geometry.wcslin.orient

        if meta_orient == None:
            meta_orient = self.members[0].geometry.wcslin.orient
        for exp in self.members:
            exp.geometry.wcs.orient = meta_orient

        return