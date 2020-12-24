# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/merge_smart_probes.py
# Compiled at: 2008-12-08 17:00:29
"""usage %prog merge_file input_smart_probes > output_smart_probes

Each line in the merge file contains two or more CNP names.
Read the input_smart_probes, and write to stdout a smart probes file that has
the CNP names from the merge file merged.  The first CNP on each line in the merge
file is used as the output name for the merged CNP."""
from __future__ import division
import optparse, sys
from mpgutils import utils

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(__doc__)
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) != 3:
        parser.print_help()
        return 1
    strMergePath = lstArgs[1]
    strSmartProbesPath = lstArgs[2]
    dctMergedCNPNameMap = {}
    for lstFields in utils.iterateWhitespaceDelimitedFile(strMergePath):
        strNewName = lstFields[0]
        for strCNP in lstFields:
            dctMergedCNPNameMap[strCNP] = strNewName

    stCNPProbePairsSeen = set()
    print ('\t').join(['cnp_id', 'probeset_id'])
    for lstFields in utils.iterateWhitespaceDelimitedFile(strSmartProbesPath, iNumFieldsExpected=2, bSkipHeader=True):
        strNewName = dctMergedCNPNameMap.get(lstFields[0], lstFields[0])
        tupOut = (
         strNewName, lstFields[1])
        if tupOut in stCNPProbePairsSeen:
            continue
        stCNPProbePairsSeen.add(tupOut)
        print ('\t').join(tupOut)

    return


if __name__ == '__main__':
    sys.exit(main())