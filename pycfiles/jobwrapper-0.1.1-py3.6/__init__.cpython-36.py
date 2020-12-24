# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/__init__.py
# Compiled at: 2018-09-07 06:05:16
# Size of source mod 2**32: 591 bytes
"""Top-level package for jobWrapper."""
__author__ = 'Antoine Tavant'
__email__ = 'antoinetavant@hotmail.fr'
__version__ = '0.1'
name = 'jobwrapper'
from .inputclass import inputparams
from .inspect_exec import is_debug
from .job_watcher import JobState, is_memo_created, last_file_created, get_errfile_notempty
from .mail import sendmail
from .preporc import test_expected, main as preproc, get_hostname
from .readTemp import main as readTemp
from .run_sbatch import main as runSbatch
from .slurm_wrapper import launch_job, return_status, kill_job, exist_job