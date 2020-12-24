# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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