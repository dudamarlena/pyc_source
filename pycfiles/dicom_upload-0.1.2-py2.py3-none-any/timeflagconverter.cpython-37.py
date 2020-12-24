# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/timeflagconverter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 632 bytes


def timeflagconverter_int2string(timeflag):
    timestring = ''
    if timeflag == 0:
        timestring = 'pre'
    elif timeflag == 1:
        timestring = 'int'
    elif timeflag == 2:
        timestring = 'post'
    else:
        print('ERROR', 'timestring not recognized:', timestring)
    return timestring


def timeflagconverter_string2int(timestring):
    timeflag = -1
    if timestring == 'pre':
        timeflag = 0
    elif timestring == 'int':
        timeflag = 1
    elif timestring == 'post':
        timeflag = 2
    else:
        print('ERROR', 'timestring not recognized:', timeflag)
    return timeflag