# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PCM2Wav/PCM/PCM.py
# Compiled at: 2019-05-02 09:21:26
# Size of source mod 2**32: 1568 bytes
"""
    File name: PCM.py
    Author: Roel Postelmans
    Date created: 2017
"""
import errno, os

class PCM(object):
    __doc__ = '\n        PCM data parser (parent class)\n    '

    def __init__(self, csv_file, first):
        """
            PCM data parser initiator
        """
        self.csv = open(csv_file, 'r')
        if not self.csv:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), csv_file)
        nbr = 0
        for nbr, self.line in enumerate(self.csv):
            if nbr == first:
                self.start_time = self.line

        self.end_time = self.line
        self.sample_count = nbr
        self.sample_rate = 0

    def determine_sample_rate(self):
        """
            Calculate the sample rate
            Not supported by all kind of PCM data files!
        """
        self.sample_rate = self.end_time - self.start_time
        self.sample_rate /= self.sample_count
        self.sample_rate **= -1

    def pop_data(self):
        """
            Pop one line of data from the parse file
        """
        self.line = self.csv.readline()
        if self.line == '':
            raise EOFError
        self.sample_count += 1

    def reset(self):
        """
            Reset the parsing
        """
        self.sample_count = 0
        self.csv.seek(0, 0)

    def close(self):
        """
            Close the being parsed file
        """
        self.csv.close()