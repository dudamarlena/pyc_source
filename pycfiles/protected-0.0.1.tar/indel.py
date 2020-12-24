# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protect/mutation_calling/indel.py
# Compiled at: 2018-05-07 13:54:25
from __future__ import print_function

def run_indel_caller(job, tumor_bam, normal_bam, univ_options, indel_options):
    """
    Run an indel caller on the DNA bams.  This module will be implemented in the future.

    :param dict tumor_bam: Dict of bam and bai for tumor DNA-Seq
    :param dict normal_bam: Dict of bam and bai for normal DNA-Seq
    :param dict univ_options: Dict of universal options used by almost all tools
    :param dict indel_options: Options specific to indel calling
    :return: fsID to the merged fusion calls
    :rtype: toil.fileStore.FileID
    """
    job.fileStore.logToMaster('INDELs are currently unsupported.... Skipping.')
    indel_file = job.fileStore.getLocalTempFile()
    output_file = job.fileStore.writeGlobalFile(indel_file)
    job.fileStore.logToMaster('Ran INDEL on %s successfully' % univ_options['patient'])
    return output_file