# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/compliance_suite/utils.py
# Compiled at: 2018-09-28 03:06:41
# Size of source mod 2**32: 1520 bytes
import os
TEST_SUITE = os.path.dirname(__file__)
SEQUENCE_FILES = os.path.join(TEST_SUITE, 'sequences/')

class Sequence:
    __doc__ = 'Sequence model object used to store sequence data in a defined manner\n    '

    def __init__(self, name, sequence, is_circular, sha512, md5, size):
        self.name = name
        self.sequence = sequence
        self.is_circular = is_circular
        self.sha512 = sha512
        self.md5 = md5
        self.size = size


def read_sequence(chr_name):
    with open(SEQUENCE_FILES + chr_name + '.faa', 'r') as (sequence_file):
        next(sequence_file)
        sequence_data = sequence_file.read().replace('\n', '')
    return sequence_data


def read_sequence_data(chr_name):
    import json
    with open(SEQUENCE_FILES + 'checksums.json', 'r') as (checksums_file):
        checksums = json.load(checksums_file)
    return checksums[chr_name]


def get_seq_obj(chr):
    data = read_sequence_data(chr)
    if data['is_circular'] == 1:
        data['is_circular'] = True
    else:
        data['is_circular'] = False
    return Sequence(chr, read_sequence(chr), data['is_circular'], data['sha512'], data['md5'], len(read_sequence(chr)))


def data():
    """data fixture loads all the data and return data variable for use in tests
    """
    data = []
    data.append(get_seq_obj('I'))
    data.append(get_seq_obj('VI'))
    data.append(get_seq_obj('NC'))
    return data