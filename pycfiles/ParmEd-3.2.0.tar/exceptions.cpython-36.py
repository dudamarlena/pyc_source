# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/exceptions.py
# Compiled at: 2017-09-07 13:54:44
# Size of source mod 2**32: 3511 bytes
"""
This module contains all of the exceptions that are used in the chemistry
package
"""
import warnings

class ParmedError(Exception):
    __doc__ = ' Base class for all non-trivial exceptions raised by ParmEd '


class ParsingError(ParmedError):
    __doc__ = ' If there was a problem parsing any kind of file '


class PDBError(ParsingError):
    __doc__ = ' If there was a problem parsing a PDB file '


class Mol2Error(ParsingError):
    __doc__ = ' If there was a problem parsing a Mol2 file '


class MaskError(ParmedError):
    __doc__ = ' Error when a Mask is poorly formed '


class OpenMMError(ParmedError):
    __doc__ = " If there's a problem making an OpenMM system "


class AmberError(ParsingError):
    __doc__ = ' This is a generic AmberParmError '


class TinkerError(ParsingError):
    __doc__ = ' Raised when one of the TINKER parsing routines hits a bad file '


class CharmmError(ParsingError):
    __doc__ = ' If there is a problem parsing CHARMM PSF files '


class ResidueError(ParmedError):
    __doc__ = ' For when there are problems defining a residue '


class IncompatiblePatchError(ParmedError):
    __doc__ = ' For when applying a PatchTemplate to a ResidueTemplate fails '


class ParameterError(ParmedError):
    __doc__ = ' If a parameter is missing from a database '


class GromacsError(ParmedError):
    __doc__ = ' If there is a problem parsing GROMACS topology files '


class FormatNotFound(ParmedError):
    __doc__ = ' If the file format does not have a registered parser with it '


class RosettaError(ParmedError):
    __doc__ = ' If there is a problem loading a Rosetta pose object '


class PreProcessorError(ParmedError):
    __doc__ = ' If there is a problem running the C-like preprocessor '


class MoleculeError(ParmedError):
    __doc__ = ' If there is a problem defining a molecule via the bond graph '


class PdbxError(ParmedError):
    __doc__ = ' Class for catching general errors with PDBx/mmCIF parsing '


class PdbxSyntaxError(PdbxError):
    __doc__ = ' Class for catching errors in mmCIF/PDBx syntax '

    def __init__(self, lineNumber='-1', text=''):
        Exception.__init__(self)
        self.lineNumber = lineNumber
        self.text = text

    def __str__(self):
        return '%%ERROR - [at line: %d] %s' % (self.lineNumber, self.text)


class InputError(ParmedError):
    __doc__ = ' When there is an error with input '


class ParmedWarning(Warning):
    __doc__ = ' Base class for all warnings raised by ParmEd '


warnings.filterwarnings('always', category=ParmedWarning)

class PDBWarning(ParmedWarning):
    __doc__ = ' A non-fatal error to indicate a problematic PDB file '


class AmberWarning(ParmedWarning):
    __doc__ = ' If there is something that is non-fatal '


class SplitResidueWarning(ParmedWarning):
    __doc__ = ' For if a residue with the same number but different names is split '


class CharmmWarning(ParmedWarning):
    __doc__ = ' For non-fatal PSF parsing issues '


class GromacsWarning(ParmedWarning):
    __doc__ = ' If we are uncertain about something regarding the GROMACS topology file '


class ParameterWarning(ParmedWarning):
    __doc__ = " If a type of parameter is missing, but you don't want it to be fatal "


class TinkerWarning(ParmedWarning):
    pass


class PreProcessorWarning(ParmedWarning):
    __doc__ = ' If there is something we should warn about in preprocessing '


class OpenMMWarning(ParmedWarning):
    __doc__ = ' If there is something we should warn when processing OpenMM objects '


class CharmmPsfEOF(ParmedError):
    __doc__ = ' If we hit an end-of-file in parsing CHARMM files '