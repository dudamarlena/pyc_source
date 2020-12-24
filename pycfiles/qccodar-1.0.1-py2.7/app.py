# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qccodar/app.py
# Compiled at: 2017-08-24 15:42:32
"""Quality control CODAR (qccodar) RadialMetric data. 

Usage:
  qccodar (auto | catchup | manual) [options]
  qccodar --help | --version

Options:
  -d DIR --datadir DIR      Data directory to process [default: /Codar/SeaSonde/Data]
  -p PAT --pattern PAT      Pattern type [default: IdealPattern]
  -h --help                 Show this help message and exit
  --version                 Show version
  
"""
import os, re, glob
from pkg_resources import get_distribution
import time
from .qcutils import do_qc, recursive_glob
from .codarutils import run_LLUVMerger, get_radialmetric_foldername
__version__ = get_distribution('qccodar').version
debug = 1

def manual(datadir, pattern):
    """ Manual mode runs qc and merge on all files in datadir """
    rmfoldername = get_radialmetric_foldername(datadir)
    fns = recursive_glob(os.path.join(datadir, rmfoldername, pattern), 'RDL*.ruv')
    if not fns:
        print 'Warn: qccodar manual --datadir %s --pattern %s' % (datadir, pattern)
        print 'No files RDL*.ruv found in %s' % fulldatadir
        return
    print 'qccodar (manual) -- qc step ...'
    for fullfn in fns:
        print '... input: %s' % fullfn
        fn = os.path.basename(fullfn)
        ofn = do_qc(datadir, fn, pattern)
        print '... output: %s' % ofn

    fns = recursive_glob(os.path.join(datadir, 'RadialShorts_qcd', pattern), 'RDL*00.ruv')
    print 'qccodar (manual) -- merge step: ...'
    for fullfn in fns:
        print '... input: %s' % fullfn
        fn = os.path.basename(fullfn)
        ofn = run_LLUVMerger(datadir, fn, pattern)
        print '... output: %s' % ofn


def auto(datadir, pattern, fullfn):
    """ Auto mode runs qc and merge for each fullfn """
    numfiles = 3
    rmfoldername = get_radialmetric_foldername(datadir)
    indir = os.path.join(datadir, rmfoldername, pattern)
    fns = recursive_glob(indir, 'RDL*.ruv')
    try:
        idx = fns.index(fullfn)
    except ValueError as e:
        idx = None

    if idx == None:
        print 'qccodar (auto): Expecting RadialMetric file. '
        print "    File %s does not match 'RDL*.ruv'" % fullfn
        return
    else:
        if numfiles == 1 and len(fns) >= 1:
            fullfn = fns[idx]
        else:
            if numfiles == 3 and len(fns) >= 2 and idx >= 1:
                fullfn = fns[(idx - 1)]
            else:
                if numfiles == 5 and len(fns) >= 3 and idx >= 2:
                    fullfn = fns[(idx - 2)]
                else:
                    print '... Nothing processed. Need more files to run qc'
                    return
                try:
                    print '... qc input: %s' % fullfn
                    fn = os.path.basename(fullfn)
                    rsdfn = do_qc(datadir, fn, pattern)
                    print '... qc output: %s' % rsdfn
                except EOFError as e:
                    print 'Encountered empty file in qc process ... wait for next file event to process'
                    return

            indir = os.path.join(datadir, 'RadialShorts_qcd', pattern)
            fns = recursive_glob(indir, 'RDL*00.ruv')
            try:
                idx = fns.index(rsdfn)
            except ValueError as e:
                idx = None

        if idx != None:
            fullfn = fns[idx]
            print '... merge input: %s' % fullfn
            fn = os.path.basename(fullfn)
            ofn = run_LLUVMerger(datadir, fn, pattern)
            print '... merge output: %s' % ofn
        return


def catchup(datadir, pattern):
    """ Process any new RadialMetric files not processed yet in datadir """
    numfiles = 3
    if pattern == 'IdealPattern':
        lluvtype = 'v'
    else:
        if pattern == 'MeasPattern':
            lluvtype = 'w'
        rmfoldername = get_radialmetric_foldername(datadir)
        fns = recursive_glob(os.path.join(datadir, rmfoldername, pattern), 'RDL*.ruv')
        fns = [ os.path.basename(fn) for fn in fns ]
        rsfns = recursive_glob(os.path.join(datadir, 'RadialShorts_qcd', pattern), 'RDL*.ruv')
        rsfns = [ os.path.basename(fn) for fn in rsfns ]
        for idx, fn in enumerate(rsfns):
            rsfns[idx] = re.sub('RDL[xy]', 'RDL' + lluvtype, fn)

    fns = dict([ (fn, None) for fn in fns ])
    rsfns = dict([ (fn, None) for fn in rsfns ])
    newfns = [ fn for fn in fns if fn not in rsfns ]
    newfns.sort()
    if numfiles == 3:
        newfns = newfns[1:]
    else:
        if numfiles == 5:
            newfns = newfns[2:]
        print 'Files to process ...'
        print newfns
        for fn in newfns:
            fullfn = os.path.join(datadir, rmfoldername, pattern, fn)
            auto(datadir, pattern, fullfn)

    return


def main():
    """Run qccodar from the command line."""
    from docopt import docopt
    arguments = docopt(__doc__, version='qccodar %s' % __version__)
    datadir, pattern = arguments['--datadir'], arguments['--pattern']
    if arguments['manual']:
        runarg = 'manual'
    else:
        if arguments['auto']:
            runarg = 'auto'
        else:
            if arguments['catchup']:
                runarg = 'catchup'
            else:
                runarg = ''
            rmfoldername = get_radialmetric_foldername(datadir)
            indatadir = os.path.join(datadir, rmfoldername, pattern)
            if not os.path.isdir(indatadir):
                print 'Error: qccodar %s --datadir %s --pattern %s' % (runarg, datadir, pattern)
                print 'Directory does not exist: %s ' % indatadir
                return
            outdir1 = os.path.join(datadir, 'RadialShorts_qcd', pattern)
            if not os.path.exists(outdir1):
                os.makedirs(outdir1)
            outdir2 = os.path.join(datadir, 'Radials_qcd', pattern)
            if not os.path.isdir(outdir2):
                os.makedirs(outdir2)
            if arguments['manual']:
                manual(datadir, pattern)
                return
            if arguments['catchup']:
                catchup(datadir, pattern)
                return
        if arguments['auto']:
            catchup(datadir, pattern)
            return


if __name__ == '__main__':
    main()