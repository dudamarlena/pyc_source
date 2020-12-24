# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ensembl_map/sequence.py
# Compiled at: 2020-04-24 16:50:04
# Size of source mod 2**32: 1041 bytes
from .mapper import _map

def cds_sequence(cds, start, end=None, raise_error=True):
    """Return the sequence of a CDS at the given position(s)."""
    return _get_feature(cds, start, end, 'cds', raise_error).sequence


def protein_sequence(protein, start, end=None, raise_error=True):
    """Return the sequence of a protein at the given position(s)."""
    return _get_feature(protein, start, end, 'protein', raise_error).sequence


def transcript_sequence(transcript, start, end=None, raise_error=True):
    """Return the sequence of a transcript at the given position(s)."""
    return _get_feature(transcript, start, end, 'transcript', raise_error).sequence


def _get_feature(feature, start, end, feature_type, raise_error):
    result = _map(feature, start, end, feature_type, feature_type)
    if not result:
        if raise_error:
            raise ValueError(f"Could not get {feature_type} sequence of {feature}")
    elif len(result) > 1:
        raise ValueError(f"Got multiple matches for {feature_type} {feature}")
    return result[0]