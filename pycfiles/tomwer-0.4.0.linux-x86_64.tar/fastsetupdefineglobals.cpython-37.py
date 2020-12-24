# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/fastsetupdefineglobals.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 5187 bytes
"""This module provides global definitions to prepare fasttomo input as HDF5 file.
of reconstruction parameters structure and should be a mirror of the octave one:
/sware/pub/octave-tomwer/suse82/m/tomotools/DEV/defineGLOBALS.m
"""
__authors__ = [
 'C. Nemoz', 'H.Payno']
__license__ = 'MIT'
__date__ = '25/05/2016'
import os, logging
from tomwer.core.process.reconstruction.ftseries.params import ReconsParams
import copy
logger = logging.getLogger(__name__)
try:
    from silx.io.octaveh5 import Octaveh5
except ImportError as e:
    try:
        logger.error('Module ' + __name__ + ' requires silx.io.octaveh5')
        raise e
    finally:
        e = None
        del e

class H5MissingParameters(Exception):
    __doc__ = 'Exception launch when some h5 parameters are missing from a structure'

    def __init__(self, missingStruc, missingVar):
        super(H5MissingParameters, self).__init__()
        self.missingStructures = missingStruc
        self.missingVariables = missingVar

    def __str__(self):
        mess = 'File is missing some structures and/or variables.'
        mess += 'Values of those has been setted to default values. '
        mess += 'Please make sure they are correct. Missing structures are '
        mess += ' missing variables \n: %s' % self.missingVariables
        mess += ' missing structures \n: %s' % self.missingStructures
        return mess


class FastSetupAll(object):
    OFFV = 'pyhst2'
    h5_prefix = 'ftinput_'
    DEFAULT_VALUES = ReconsParams()

    def __init__(self):
        self.tmph5 = 'octave_input.h5'
        self.structures = ReconsParams()

    @staticmethod
    def getDefaultValues(structID):
        """Return a deep copy of the struct ID param name / value dict"""
        if structID == 'FT':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.ft.to_dict())
        if structID == 'FTAXIS':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.axis.to_dict())
        if structID == 'PAGANIN':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.paganin.to_dict())
        if structID == 'PYHSTEXE':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.pyhst.to_dict())
        if structID == 'BEAMGEO':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.beam_geo.to_dict())
        if structID == 'DKRF':
            return copy.deepcopy(FastSetupAll.DEFAULT_VALUES.dkrf.to_dict())
        raise ValueError('%s has no default values' % structID)

    def readAll(self, filn, targetted_octave_version):
        if not os.path.isfile(filn):
            raise IOError('given path is not a file %s' % filn)
        reader = Octaveh5(targetted_octave_version).open(filn)
        self.resetDefaultStructures()
        for st in list(reader.file):
            if st in self.structures.managed_params:
                self.structures[st].load_from_dict(reader.get(st))
            else:
                if st in self.structures.unmanaged_params:
                    self.structures._remove_unmanaged_param(param=st)
                self.structures._add_unmanaged_param(param=st, value=(reader.get(st)))
            assert st in self.structures.all_params

    def resetDefaultStructures(self):
        self.structures.load_from_dict(ReconsParams().to_dict())
        self.structures._reset_unmanaged_params()

    def writeAll(self, filn, targetted_octave_version):
        if os.path.isfile(filn) is True:
            os.remove(filn)
        writer = Octaveh5(targetted_octave_version)
        writer.open(filn, 'a')
        structures = self.structures.to_dict()
        for s in structures:
            assert type(structures[s]) is dict
            writer.write(s, structures[s])

        writer.close()

    @staticmethod
    def getAllDefaultStructures():
        return ReconsParams()