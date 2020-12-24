# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/merge_calls_confs.py
# Compiled at: 2008-12-08 17:00:29
"""usage %prog [options]
Make a guide file from a cel_map file mapping a cel file to a sample name,
and a  list of celFiles in a calls file.
"""
from __future__ import division
import optparse, sys, string
from mpgutils import utils
lstRequiredOptions = [
 'pedigree', 'output', 'celMap']

def mergeFiles(lstFiles, outFile):
    lstFileHandles = [ open(f, 'r') for f in lstFiles ]
    startHandle = lstFileHandles[1]
    out = open(outFile, 'w')
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
        out.write(finalLine)

    out.close()
    return successFlag


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-o', '--output', default=None, help='(Required) Output a single calls or confs file that \n                      is the result of merging multiple calls/confs files')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    lstRequiredOptions = ['output']
    if not utils.validateRequiredOptions(dctOptions, lstRequiredOptions):
        parser.print_help()
        return 1
    lstFiles = lstArgs[1:len(lstArgs)]
    successFlag = mergeFiles(lstFiles, dctOptions.output)
    if successFlag:
        print 'Finished Merge Successfully'
    return


if __name__ == '__main__':
    sys.exit(main())