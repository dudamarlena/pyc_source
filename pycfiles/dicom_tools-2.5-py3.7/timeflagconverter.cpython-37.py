# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/timeflagconverter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 632 bytes


def timeflagconverter_int2string(timeflag):
    timestring = ''
    if timeflag == 0:
        timestring = 'pre'
    else:
        if timeflag == 1:
            timestring = 'int'
        else:
            if timeflag == 2:
                timestring = 'post'
            else:
                print('ERROR', 'timestring not recognized:', timestring)
    return timestring


def timeflagconverter_string2int(timestring):
    timeflag = -1
    if timestring == 'pre':
        timeflag = 0
    else:
        if timestring == 'int':
            timeflag = 1
        else:
            if timestring == 'post':
                timeflag = 2
            else:
                print('ERROR', 'timestring not recognized:', timeflag)
    return timeflag