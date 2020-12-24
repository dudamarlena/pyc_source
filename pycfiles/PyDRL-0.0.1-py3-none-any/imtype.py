# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\imtype.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import types, pyfits
from stsci.tools import fileutil

class Imtype:
    """ Class which determines the format of the file, how to access the
        SCI data array, and if available, any DQ array as well.  The syntax
        for accessing the data will then be kept as attributes for use by
        other tasks/classes.

        Parameters:
            filename    -   name of file to be examined
            handle      -   PyFITS-style file handle for image
            dqsuffix    -   suffix for DQ array for non-MEF files

        If 'dqsuffix' is not provided and the file is GEIS formatted,
        then this class will search for a '.c1h' extension by default,
        and return None if not found.

    """

    def __init__(self, filename, handle=None, dqsuffix=None):
        self.handle = handle
        self.filename = filename
        self.dqfile = filename
        self.seperator = ','
        self.dq_suffix = dqsuffix
        self.dq_extname = 'dq'
        self.sci_extname = 'sci'
        self.sci_extn = '[' + self.sci_extname + ',1]'
        self.dq_extn = '[' + self.dq_extname + ',1]'
        if filename:
            if filename.find('.fits') > -1:
                if handle and len(handle) == 1:
                    self.sci_extn = None
                    self.dq_extn = None
                    self.dq_extname = None
                    self.sci_extname = None
            else:
                self.seperator = '['
                if not dqsuffix:
                    _dqsuffix = '.c1h'
                    _indx = filename.rfind('.')
                    if fileutil.findFile(filename[:_indx] + _dqsuffix):
                        self.dq_suffix = '.c1h'
                    else:
                        self.dq_suffix = None
                self.sci_extn = '[1]'
                self.dq_extn = '[1]'
                self.dq_extname = '1'
                self.sci_extname = '1'
        return

    def makeSciName(self, extver, section=None):
        """ Returns the properly formatted filename to access the SCI extension."""
        if section == None:
            _extname = self.filename + self._setSciExtn(extn=extver)
        else:
            _extname = self.filename + '[sci,' + str(section) + ']'
        return _extname

    def makeDQName(self, extver):
        """ Create the name of the file which contains the DQ array.
            For multi-extension FITS files, this will be the same file
            as the SCI array.
        """
        if not self.dq_suffix:
            _dqname = self.dqfile
        else:
            _dqname = fileutil.buildNewRootname(self.dqfile, extn=self.dq_suffix)
        if self.dq_extn:
            _dqname += self._setDQExtn(extn=extver)
        elif self.dq_suffix:
            _dqname = _dqname + '[0]'
        else:
            _dqname = None
        return _dqname

    def _setDQExtn(self, extn=None):
        """ Builds extension specification for accessing DQ extension/group.
        """
        if extn != None:
            if self.dq_extn:
                _lensep = len(self.seperator)
                _indx = self.dq_extn.find(self.seperator) + _lensep
                return self.dq_extn[:_indx] + repr(extn) + self.dq_extn[_indx + 1:]
            else:
                return ''

        else:
            return self.dq_extn
        return

    def _setSciExtn(self, extn=None):
        """ Builds extension specification for accessing SCI extension/group.
        """
        if extn != None:
            if self.sci_extn:
                _lensep = len(self.seperator)
                _indx = self.sci_extn.find(self.seperator) + _lensep
                return self.sci_extn[:_indx] + repr(extn) + self.sci_extn[_indx + 1:]
            else:
                return ''

        else:
            return self.sci_extn
        return