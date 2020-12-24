# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/runrscript.py
# Compiled at: 2010-10-12 17:55:40
from optparse import OptionParser
from os import popen
from mpgutils import utils
from mpgutils.RUtils import RscriptToPython
import optparse, sys, re, os

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = optparse.OptionParser(usage)
    parser.add_option('--pif', help='Pool Info File')
    parser.add_option('--outputdir', help='Output Directory')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    lstRequiredOptions = [
     'pif']
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    pifpath = open(dctOptions.pif, 'r').readlines()
    for line in pifpath[1:]:
        line = line.rstrip()
        line = line.split()
        bamfile = line[0]
        individuals = line[2]
        table_file_name = str(bamfile) + '.combined.error.coverage'
        output_file_name = str(bamfile) + '.combined.error.coverage.calls'
        num_people = int(individuals)
        print num_people
        print '\n\n'
        CallonR(table_file_name, output_file_name, num_people)


def CallonR(table_file_name, output_file_name, num_people):
    lstLibraries = ['mpganalysis.syzygy']
    methodName = 'syzygylikelihoodcalc'
    dctArguments = {'table_file_name': table_file_name, 'output_file_name': output_file_name, 
       'num_people': num_people, 
       'verbose': True}
    RscriptToPython.callRscript(lstLibraries, methodName, dctArguments, True)


if __name__ == '__main__':
    main()