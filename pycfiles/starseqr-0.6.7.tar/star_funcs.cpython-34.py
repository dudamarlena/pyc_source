# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/star_funcs.py
# Compiled at: 2017-12-07 17:16:00
# Size of source mod 2**32: 4023 bytes
from __future__ import absolute_import, division, print_function
import os, sys, logging, subprocess as sp, starseqr_utils as su
logger = logging.getLogger('STAR-SEQR')

def run_star(prefix, fq1, fq2, star_index, threads, mode):
    """
    Run STAR alignment for RNA or DNA with different sensitivity parameters.
    """
    logger.info('Starting STAR Alignment')
    if not os.path.isfile(prefix + '.Chimeric.out.junction'):
        if not os.path.isdir(star_index):
            logger.error('Error: STAR index was not found at ' + star_index + ' Please update the path.', exc_info=True)
            sys.exit(1)
        STAR_args = [
         'STAR', '--readFilesIn', fq1, fq2, '--readFilesCommand', 'zcat',
         '--runThreadN', str(threads), '--genomeDir', star_index,
         '--outFileNamePrefix ', prefix + '.', '--chimScoreJunctionNonGTAG', -1,
         '--outSAMtype', 'None', '--chimOutType', 'SeparateSAMold',
         '--alignSJDBoverhangMin', 5, '--outFilterMultimapScoreRange', 1,
         '--outFilterMultimapNmax', 5,
         '--outMultimapperOrder', 'Random', '--outSAMattributes', 'NH', 'HI', 'AS', 'nM', 'ch']
        if mode == 0:
            sens_params = [
             '--chimSegmentMin', 10, '--chimJunctionOverhangMin', 10,
             '--chimScoreMin', 1, '--chimScoreDropMax', 20,
             '--chimScoreSeparation', 10, '--chimSegmentReadGapMax', 3,
             '--chimFilter', 'None', '--twopassMode', 'None',
             '--alignSJstitchMismatchNmax', 5, -1, 5, 5,
             '--chimMainSegmentMultNmax', 1]
        else:
            if mode == 1:
                sens_params = [
                 '--chimSegmentMin', 10, '--chimJunctionOverhangMin', 10,
                 '--chimScoreMin', 1, '--chimScoreDropMax', 30,
                 '--chimScoreSeparation', 7, '--chimSegmentReadGapMax', 3,
                 '--chimFilter', 'None', '--twopassMode', 'None',
                 '--alignSJstitchMismatchNmax', 5, -1, 5, 5,
                 '--chimMainSegmentMultNmax', 10]
            STAR_args.extend(sens_params)
            STAR_args = list(map(str, STAR_args))
            logger.info('*STAR Command: ' + ' '.join(STAR_args))
            try:
                p = sp.Popen(STAR_args, stdout=sp.PIPE, stderr=sp.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    logger.info(stdout)
                if stderr:
                    logger.error(stderr)
                if p.returncode != 0:
                    logger.error('Error: STAR failed', exc_info=True)
                    sys.exit(1)
            except OSError as o:
                logger.error('Exception: ' + str(o))
                logger.error('STAR Failed', exc_info=True)
                sys.exit(1)

        su.common.check_file_exists(prefix + '.Chimeric.out.junction')
        su.common.check_file_exists(prefix + '.Chimeric.out.sam')
    else:
        su.common.check_file_exists(prefix + '.Chimeric.out.junction')
        su.common.check_file_exists(prefix + '.Chimeric.out.sam')
        logger.warn('Skipping STAR alignment as files already exist!')
    logger.info('STAR Alignment Finished!')