# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo/cognitivegeo/src\segpy\revisions.py
# Compiled at: 2017-02-16 13:30:26
# Size of source mod 2**32: 898 bytes
SEGY_REVISION_0 = 0
SEGY_REVISION_1 = 1
VARIANTS = {SEGY_REVISION_0: SEGY_REVISION_0, 
 SEGY_REVISION_1: SEGY_REVISION_1, 
 0: SEGY_REVISION_0, 
 1: SEGY_REVISION_1, 
 100: SEGY_REVISION_1, 
 256: SEGY_REVISION_1}

class SegYRevisionError(Exception):
    pass


def canonicalize_revision(revision):
    """Canonicalize a SEG Y revision.

    Various SEG Y revisions are seen in the wild; this function canonicalizes the supplies revision
    to either SEGY_REVISION_0 or SEGY_REVISION_1.

    Args:
        revision: Any object representing a SEG Y revision.

    Returns:
        Either SEGY_REVISION_0 or SEGY_REVISION_1.

    Raises:
        SegYRevisionError: If the revision is not known.
    """
    try:
        return VARIANTS[revision]
    except KeyError:
        raise SegYRevisionError('Unknown SEG Y Revision {!r}'.format(revision))