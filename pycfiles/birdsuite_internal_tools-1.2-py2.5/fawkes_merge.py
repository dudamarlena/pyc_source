# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plink_pipeline/fawkes_merge.py
# Compiled at: 2009-01-30 12:46:16
"""usage %prog [options]
Make a guide file from a cel_map file mapping a cel file to a sample name,
and a  list of celFiles in a calls file.
"""
from __future__ import division
import optparse, sys, string, shutil
from mpgutils import utils
import os, re

def main(argv=None):
    if argv is None:
        argv = sys.argv
    lstRequiredOptions = [
     'plateroot']
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-p', '--plateroot', help='(Required) Contains folders with larry-bird style files')
    parser.add_option('-o', '--outputname', default='Output', help='define the file name root for the output files')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    lstOptionsToCheck = [
     'plateroot']
    utils.validatePathArgs(dctOptions, lstOptionsToCheck, True)
    call_output = os.path.join(dctOptions.plateroot, dctOptions.outputname + '.merged.dip')
    conf_output = os.path.join(dctOptions.plateroot, dctOptions.outputname + '.merged.conf')
    pattern = re.compile('[.]diploid', re.IGNORECASE)
    CallsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    pattern = re.compile('[.]larry_bird_confs', re.IGNORECASE)
    ConfsPaths = utils.findFiles(dctOptions.plateroot, pattern)
    if len(CallsPaths) != len(ConfsPaths):
        print 'The number of Confidence Files and Calls files are not equal'
        print 'Calls Files =' + str(CallsPaths)
        print 'Confs Files =' + str(ConfsPaths)
        sys.exit(1)
    elif len(CallsPaths) > 1:
        successFlag = mergeFiles(CallsPaths, call_output)
        if not successFlag:
            print 'Calls Merge Failed'
            sys.exit(2)
        successFlag = mergeFiles(ConfsPaths, conf_output)
        if not successFlag:
            print 'Confs Merge Failed'
            sys.exit(2)
    elif len(CallsPaths) == 1:
        print 'There was only one file found, no merge required.'
        shutil.copy(CallsPaths[0], call_output)
        shutil.copy(ConfsPaths[0], conf_output)
    print 'Finished -- Fawkes_Merge.Py\n'
    return


def mergeFiles(lstFiles, outFile):
    lstFileHandles = [ open(f, 'r') for f in lstFiles ]
    startHandle = lstFileHandles[1]
    fOut = open(outFile, 'w')
    successFlag = True
    while startHandle:
        lines = [ f.readline() for f in lstFileHandles ]
        data = lines[0].split()
        if len(data) == 0:
            break
        id = data[0]
        otherLines = lines[1:]
        otherLines = [ l.split() for l in otherLines ]
        otherIDs = [ l[0] for l in otherLines ]
        for o in otherIDs:
            if o != id:
                print "Line of first file and subsequent file don't match:" + 'original[' + id + '] new [' + o + ']'
                successFlag = False

        otherLines = [ l[1:] for l in otherLines ]
        for l in otherLines:
            data.extend(l)

        data.append('\n')
        finalLine = ('\t').join(data)
        fOut.write(finalLine)

    fOut.close()
    return successFlag


if __name__ == '__main__':
    sys.exit(main())