# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/info_file_parser.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 421 bytes


def info_file_parser(filename, verbose=False):
    results = {}
    infile = open(filename, 'r')
    for iline, line in enumerate(infile):
        if line[0] == '#':
            continue
        lines = line.split()
        if len(lines) < 2:
            continue
        if lines[0][0] == '#':
            continue
        infotype = lines[0]
        infotype = infotype.replace(':', '')
        info = lines[1]
        results[infotype] = info

    return results