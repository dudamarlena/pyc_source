# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/record/search/file.py
# Compiled at: 2018-12-30 10:46:50
from pyasn1.compat.octets import str2octs

def getRecord(fileObj, lineNo=None, offset=0):
    line = fileObj.readline()
    if lineNo is not None and line:
        lineNo += 1
    while line:
        tline = line.strip()
        if not tline or tline.startswith(str2octs('#')):
            offset += len(line)
            line = fileObj.readline()
            if lineNo is not None and line:
                lineNo += 1
        else:
            break

    return (
     line, lineNo, offset)


def findEol(fileObj, offset, blockSize=256, eol=str2octs('\n')):
    while True:
        if offset < blockSize:
            offset, blockSize = 0, offset
        else:
            offset -= blockSize
        fileObj.seek(offset)
        chunk = fileObj.read(blockSize)
        try:
            return offset + chunk.rindex(eol) + 1
        except ValueError:
            if offset == 0:
                return offset
            continue


def searchRecordByOid(oid, fileObj, textParser):
    lo = mid = 0
    prev_mid = -1
    fileObj.seek(0, 2)
    hi = sz = fileObj.tell()
    while lo < hi:
        mid = (lo + hi) // 2
        fileObj.seek(mid)
        mid = findEol(fileObj, mid)
        fileObj.seek(mid)
        if mid == prev_mid:
            break
        if mid >= sz:
            return sz
        (line, _, skippedOffset) = getRecord(fileObj)
        if not line:
            return hi
        (midval, _) = textParser.evaluate(line, oidOnly=True)
        if midval < oid:
            lo = mid + skippedOffset + len(line)
        elif midval > oid:
            hi = mid
        else:
            return mid
        prev_mid = mid

    if lo == mid:
        return lo
    else:
        return hi