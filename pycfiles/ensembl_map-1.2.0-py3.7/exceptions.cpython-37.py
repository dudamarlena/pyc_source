# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/exceptions.py
# Compiled at: 2020-04-24 16:50:04
# Size of source mod 2**32: 1234 bytes


class ConvertError(ValueError):
    __doc__ = 'Base error for `convert` function errors.'


class OutOfRangeErrorBase(ConvertError):
    __doc__ = "Base error for 'OutOfRange' errors."

    def __init__(self, transcript, position):
        self.transcript = transcript
        self.position = position
        self.feature_type = None
        self.range = (None, None)

    def __str__(self):
        return f"{self.position} is outside {self.feature_type} {self.range}"


class CdsOutOfRange(OutOfRangeErrorBase):

    def __init__(self, transcript, position):
        self.transcript = transcript
        self.position = position
        self.feature_type = 'CDS'
        self.range = (1, len(self.transcript.coding_sequence))


class ExonOutOfRange(OutOfRangeErrorBase):

    def __init__(self, transcript, position):
        self.transcript = transcript
        self.position = position
        self.feature_type = 'exons'
        self.range = transcript.exon_intervals


class TranscriptOutOfRange(OutOfRangeErrorBase):

    def __init__(self, transcript, position):
        self.transcript = transcript
        self.position = position
        self.feature_type = 'transcript'
        self.range = (1, len(self.transcript.sequence))