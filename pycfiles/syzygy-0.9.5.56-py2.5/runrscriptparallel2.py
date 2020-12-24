# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/runrscriptparallel2.py
# Compiled at: 2010-10-12 17:55:37
from optparse import OptionParser
from os import popen
from mpgutils import utils
from mpgutils.RUtils import RscriptToPython
import optparse, sys, re, os, pp, time

def main(argv=None):
    if not argv:
        argv = sys.argv
    usage = 'usage: %prog [options] '
    parser = optparse.OptionParser(usage)
    parser.add_option('--pif', help='Pool Info File')
    parser.add_option('--outputdir', help='Output Directory')
    parser.add_option('--ncpu')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    lstRequiredOptions = [
     'pif']
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    ppservers = ()
    ncpus = int(dctOptions.ncpu)
    job_server = pp.Server(ncpus, ppservers=ppservers)
    print 'Starting pp with', job_server.get_ncpus(), 'workers\n'
    readpif = open(dctOptions.pif, 'r').readlines()
    jobs = []
    for line in readpif[1:]:
        line = line.rstrip()
        line = line.split()
        bamfile = line[0]
        individuals = line[2]
        table_file_name = str(bamfile) + '.combined.error.coverage'
        output_file_name = str(bamfile) + '.combined.error.coverage.calls'
        num_people = int(individuals)
        possible_args = ['table_file_name', 'output_file_name', 'num_people']
        current_args = []
        current_args.append('--table_file_name')
        current_args.append(table_file_name)
        current_args.append('--output_file_name')
        current_args.append(output_file_name)
        current_args.append('--num_people')
        current_args.append(num_people)
        jobs.append(job_server.submit(CallonR, (table_file_name, output_file_name, num_people), (), ('mpgutils',
                                                                                                     'mpgutils.RUtils',
                                                                                                     'mpgutils.RUtils.RscriptToPython')))

    start_time = time.time()
    for job in jobs:
        result = job()
        if result:
            break

    print 'Time elapsed: ', time.time() - start_time, 's'
    job_server.print_stats()


def CallonR(table_file_name, output_file_name, num_people):
    lstLibraries = [
     'mpganalysis.syzygy']
    methodName = 'syzygylikelihoodcalc'
    dctArguments = {'table_file_name': table_file_name, 'output_file_name': output_file_name, 
       'num_people': num_people, 
       'verbose': True}
    mpgutils.RUtils.RscriptToPython.callRscript(lstLibraries, methodName, dctArguments, True)


if __name__ == '__main__':
    main()