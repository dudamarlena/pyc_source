# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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