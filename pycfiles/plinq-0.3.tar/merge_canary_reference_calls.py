# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/merge_canary_reference_calls.py
# Compiled at: 2010-07-13 12:32:47
__doc__ = 'usage %prog merge_file input_canary_reference_calls > output_canary_reference_calls\n\nEach line in the merge file contains two or more CNP names.\nRead the input_canary_reference_calls, and write to stdout a reference calls file that has\nthe calls for the CNPs from the merge file merged.  The first CNP on each line in the merge\nfile is used as the output name for the merged CNP.  If the CNPs to be merged have conflicting\ncalls for a sample, this is replaced with a no-call.  If one has a call and the other a no-call,\nthe call is kept.'
from __future__ import division
import optparse, sys
from mpgutils import utils

def mergeCalls(lstOfLsts):
    """If more than one set of calls in list, merge them.  If all the actual calls for a sample agree,
    the output gets that call.  Otherwise, that sample gets a no-call (-1)"""
    if len(lstOfLsts) == 1:
        return lstOfLsts[0]
    lstRet = [None] * len(lstOfLsts[0])
    for lst in lstOfLsts:
        assert len(lst) == len(lstRet)

    for i in xrange(len(lstRet)):
        strValue = '-1'
        for lst in lstOfLsts:
            if lst[i] == '-1':
                continue
            if strValue == '-1':
                strValue = lst[i]
            elif strValue != lst[i]:
                strValue = '-1'
                break

        lstRet[i] = strValue

    return lstRet


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(__doc__)
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) != 3:
        parser.print_help()
        return 1
    strMergePath = lstArgs[1]
    strReferenceCallPath = lstArgs[2]
    dctMergedCNPNameMap = {}
    for lstFields in utils.iterateWhitespaceDelimitedFile(strMergePath):
        strNewName = lstFields[0]
        for strCNP in lstFields:
            dctMergedCNPNameMap[strCNP] = strNewName

    dctCNPRefCallsAccumulator = {}
    iterCalls = iter(utils.iterateWhitespaceDelimitedFile(strReferenceCallPath, bSkipHeader=False))
    lstHeaders = iterCalls.next()
    print ('\t').join(lstHeaders)
    while True:
        try:
            lstFields = iterCalls.next()
        except StopIteration:
            break

        strNewName = dctMergedCNPNameMap.get(lstFields[0], lstFields[0])
        lstCalls = lstFields[1:]
        dctCNPRefCallsAccumulator.setdefault(strNewName, []).append(lstCalls)

    lstKeys = dctCNPRefCallsAccumulator.keys()
    lstKeys.sort()
    for strCNP in lstKeys:
        lstCalls = mergeCalls(dctCNPRefCallsAccumulator[strCNP])
        print ('\t').join([strCNP] + lstCalls)

    return


if __name__ == '__main__':
    sys.exit(main())