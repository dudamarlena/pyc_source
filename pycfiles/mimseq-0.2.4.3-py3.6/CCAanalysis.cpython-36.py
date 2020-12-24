# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimseq/CCAanalysis.py
# Compiled at: 2020-03-17 12:13:32
# Size of source mod 2**32: 792 bytes
import os, subprocess, logging
log = logging.getLogger(__name__)

def plotDinuc(out_dir):
    log.info("\n+-----------------+\t\t\n| 3'-CCA analysis |\t\t\n+-----------------+")
    out = out_dir + 'CCAanalysis/'
    script_path = os.path.dirname(os.path.realpath(__file__))
    command = ['Rscript', script_path + '/ccaPlots.R', out + 'AlignedDinucProportions.csv', out + '/CCAcounts.csv', out]
    subprocess.check_call(command)
    log.info('CCA analysis done and plots created. Located in {}'.format(out))