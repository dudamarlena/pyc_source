# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/ValidateClass.py
# Compiled at: 2019-06-04 15:47:23
import gzip, bz2, zipfile

class Validate:

    def __init__(self):
        self.info = {'compressed': False, 
           'fileType': None}
        self.magic_dict = {b'\x1f\x8b\x08': 'gz', 
           'BZh': 'bz2', 
           'PK\x03\x04': 'zip'}
        self.max_len = max(len(x) for x in self.magic_dict)
        return

    def compressed(self, filename):
        try:
            f = open(filename)
        except Exception as e:
            f = open(filename + '.gz')

        file_start = f.read(self.max_len)
        for magic, filetype in self.magic_dict.items():
            if file_start.startswith(magic):
                return filetype

        return 'raw'

    def isFasta(self, line):
        if '>' in line[0]:
            return True
        else:
            return False

    def isFastq(self, line):
        if '@' in line[0]:
            return True
        else:
            return False

    def isGz(self, line):
        if 'gz' in line:
            return True
        else:
            return False

    def dataType(self, filename):
        comp = self.compressed(filename)
        self.info['compressed'] = comp
        if comp == 'gz':
            try:
                x = gzip.open(filename)
            except:
                x = gzip.open(filename + '.gz')

            x = x.read(10)
        elif comp == 'bz2':
            x = bz2.open(filename)
            x = x.read(10)
        elif comp == 'zip':
            x = zipfile.open(filename)
            x = x.read(10)
        elif comp == 'raw':
            x = open(filename)
            x = x.read(10)
        else:
            self.info['compressed'] = 'undefined'
        if self.isFasta(x):
            self.info['fileType'] = 'fasta'
            return self.info
        else:
            if self.isFastq(x):
                self.info['fileType'] = 'fastq'
                return self.info
            self.info['fileType'] = 'undefined'
            return self.info