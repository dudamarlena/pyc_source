# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_observed_catalogue.py
# Compiled at: 2019-07-16 04:25:49
from astropy.io import ascii
from astropy.io import fits
from beagle_utils import is_FITS_file

class ObservedCatalogue(object):

    def load(self, file_name):
        """ 
        Load a catalogue of observed sources. It automatically
        detects, and loads, FITS or ASCII files depending on the suffix.

        Parameters
        ----------
        file_name : str
            Contains the file name of the catalogue.
        """
        if is_FITS_file(file_name):
            self.data = fits.open(file_name)[1].data
            self.columns = fits.open(file_name)[1].columns
        else:
            self.data = ascii.read(file_name, Reader=ascii.basic.CommentedHeader)