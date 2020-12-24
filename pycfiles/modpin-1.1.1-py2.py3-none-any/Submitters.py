# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/boliva/sit_sbi/modppi/src/BioLib/Tools/Submitters.py
# Compiled at: 2018-11-29 11:31:12
import sys, os, subprocess

class LocalSubmitter(object):
    """
        Submit jobs to Local computer
        """

    def __init__(self, log_path='./'):
        self.log_path = log_path

    def submit(self, cmd, job_id, verbose=True):
        """
                Submits a job to Local computer
                """
        if verbose:
            sys.stdout.write('Processing %s...\n' % job_id)
        CLI = '%s > %s.out 2> %s.err' % (cmd, os.path.join(self.log_path, job_id), os.path.join(self.log_path, job_id))
        subprocess.call(CLI, shell=True)


class GaudiSubmitter(object):
    """
        Submit jobs to Gaudi Cluster
        """

    def __init__(self, qsub='sbi', log_path='./'):
        self.qsub = qsub
        self.log_path = log_path

    def submit(self, cmd, job_id):
        """
                Submits a job to Gaudi cluster
                Cluster params:
                -q   : Bind job to queue
                -cwd : Use current working directory
                -V   : Export all environmental variables
                -e   : Standard error stream log_path
                -o   : Standard out stream path
                -N   : Job name
                """
        CLI = 'echo "%s" | qsub -q %s -cwd -V -o %s -e %s -N %s' % (cmd, self.qsub, self.log_path, self.log_path, job_id)
        subprocess.call(CLI, shell=True)