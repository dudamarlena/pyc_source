# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/utils.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 1259 bytes
CHR_PREFIX = 'chr'

def formatContig(contig):
    """
    Returns a formatted tuple of contigs. One has trimmed contig, the other appends a 'chr' prefix.

    :param contig: contig with or without 'chr' prefix
    :return: tuple of a trimmed (without 'chr') and full (with 'chr') contig names
    """
    contig_trimmed = contig.lstrip(CHR_PREFIX)
    contig_full = contig if contig.startswith(CHR_PREFIX) else '%s%s' % (CHR_PREFIX, contig)
    return (
     contig_trimmed, contig_full)