# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/cmdl_handler.py
# Compiled at: 2016-07-23 05:10:01
"""
    Handles command line arguments.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import argparse
from genonets_writer import Writer
from seq_bit_impl import BitManipFactory
from genonets_constants import ErrorCodes
from genonets_exceptions import GenonetsError

class CmdParser:

    def __init__(self, arguments=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('alphabetType', help='Each genotype in the input file must be a string ' + 'of letters from the alphabet selected here.', choices=BitManipFactory.getMoleculeTypes())
        parser.add_argument('includeIndels', help="Should be set to 'True' if mutations that shift " + 'the entire genotype sequence by one letter should ' + 'also be considered. Only single point mutations are ' + "considered when this parameter is set to 'False'.", choices=[
         'True', 'true', 'False', 'false'])
        parser.add_argument('inFilePath', help='Complete path to the input file, relative to the ' + 'current directory.')
        parser.add_argument('tau', help='Minimum score threshold: all genotypes in the input ' + "file with 'score' values below 'Tau' will be ignored." + 'Tau must be a number.', type=float)
        parser.add_argument('outPath', help='Path to the directory where output files should be ' + 'generated. The directory will be created if it does ' + 'not already exist.')
        parser.add_argument('-rc', '--use_reverse_complements', dest='use_reverse_complements', action='store_const', const=True, help='When specified, reverse complements are considered during creation ' + 'and analysis of genotype networks for alphabet type DNA. This option is ' + 'not valid for other alphabet types.')
        parser.add_argument('-np', '--num_processes', dest='num_procs', action='store', type=int, default='4', help='No. of processes to be used in parallel processing')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True, help='Processing steps are printed to the screen during ' + 'program execution.')
        if arguments:
            self.args = parser.parse_args(arguments)
        else:
            self.args = parser.parse_args()

    def getArgs(self):
        return self.args


class CmdArgs:

    def __init__(self, arguments):
        self.moleculeType = arguments.alphabetType
        self.use_reverse_complements = True if arguments.use_reverse_complements else False
        if self.use_reverse_complements and self.moleculeType != 'DNA':
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.RC_ALPHABET_MISMATCH)
            raise GenonetsError(ErrorCodes.RC_ALPHABET_MISMATCH)
        if arguments.includeIndels.lower() == 'true':
            self.useIndels = True
        else:
            self.useIndels = False
        self.inFilePath = arguments.inFilePath
        self.tau = arguments.tau
        self.outPath = arguments.outPath
        if not self.outPath.endswith('/'):
            self.outPath += '/'
        self.num_procs = arguments.num_procs
        self.verbose = True if arguments.verbose else False
        paramsDict = {'alphabetType': self.moleculeType, 
           'includeIndels': str(self.useIndels), 
           'inFilePath': self.inFilePath, 
           'tau': str(self.tau), 
           'outPath': self.outPath, 
           'useReverseComplements': str(self.use_reverse_complements), 
           'num_procs': str(self.num_procs), 
           'verbose': str(self.verbose)}
        self.printInParams(paramsDict)
        Writer.writeInParamsToFile(paramsDict, self.outPath)

    def printInParams(self, paramsDict):
        print '\nParsed input parameter values:'
        print '------------------------------'
        for param in paramsDict.keys():
            print param + ': ' + paramsDict[param]

        print '------------------------------\n'