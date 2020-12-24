# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/pem.py
# Compiled at: 2019-10-17 01:00:24
import base64, sys
(stSpam, stHam, stDump) = (0, 1, 2)

def readPemBlocksFromFile(fileObj, *markers):
    startMarkers = dict(map(lambda x: (x[1], x[0]), enumerate(map(lambda y: y[0], markers))))
    stopMarkers = dict(map(lambda x: (x[1], x[0]), enumerate(map(lambda y: y[1], markers))))
    idx = -1
    substrate = ''
    certLines = []
    state = stSpam
    while True:
        certLine = fileObj.readline()
        if not certLine:
            break
        certLine = certLine.strip()
        if state == stSpam:
            if certLine in startMarkers:
                certLines = []
                idx = startMarkers[certLine]
                state = stHam
                continue
        if state == stHam:
            if certLine in stopMarkers:
                if stopMarkers[certLine] == idx:
                    state = stDump
                else:
                    certLines.append(certLine)
        elif state == stDump:
            if sys.version_info[0] <= 2:
                substrate = ('').join([ base64.b64decode(x) for x in certLines ])
            else:
                substrate = ('').encode().join([ base64.b64decode(x.encode()) for x in certLines ])
            break

    return (
     idx, substrate)


def readPemFromFile(fileObj, startMarker='-----BEGIN CERTIFICATE-----', endMarker='-----END CERTIFICATE-----'):
    (idx, substrate) = readPemBlocksFromFile(fileObj, (startMarker, endMarker))
    return substrate


def readBase64fromText(text):
    if sys.version_info[0] <= 2:
        return base64.b64decode(text)
    else:
        return base64.b64decode(text.encode())


def readBase64FromFile(fileObj):
    return readBase64fromText(fileObj.read())