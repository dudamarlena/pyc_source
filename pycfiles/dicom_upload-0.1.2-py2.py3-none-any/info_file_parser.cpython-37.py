# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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