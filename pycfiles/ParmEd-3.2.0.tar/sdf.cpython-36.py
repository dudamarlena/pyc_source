# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/formats/sdf.py
# Compiled at: 2017-03-01 21:14:20
# Size of source mod 2**32: 1041 bytes
"""
This module contains parsers for sdf file format 
extension described at https://www.cas.org/content/chemical-suppliers/example-sdf
"""
from __future__ import print_function, division, absolute_import
import linecache
from parmed.formats.registry import FileFormatType
from parmed.utils.six import add_metaclass
from parmed import rdkit

@add_metaclass(FileFormatType)
class SDFFile(object):
    __doc__ = ' Class to read SDF file '

    @staticmethod
    def id_format(filename):
        """ Identify the file as a SDF file format or not

        Parameters
        ----------
        filename : str
            Name of the file to test whether or not it is a sdf file

        Returns
        -------
        is_fmt : bool
            True if it is a sdf file, False otherwise
        """
        words = linecache.getline(filename, lineno=4).split()
        return len(words) >= 3 and words[(-1)] in ('V2000', 'V3000')

    @staticmethod
    def parse(filename, structure=False):
        return rdkit.from_sdf(filename, structure=structure)