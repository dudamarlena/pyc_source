# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/interface/interface.py
# Compiled at: 2020-02-01 10:32:11
# Size of source mod 2**32: 559 bytes
from typing import List
from models.models import Job, Project, Routine
from .formatters import fmt_options, fmt_uses

def interface_factory(jobs: List[Job], projects: List[Project], routines: List[Routine]) -> str:
    uses = [f"{job.name} [{' '.join([<{p}> for p in job.context])}]" if job.context else job.name for job in jobs] + [routine.name for routine in routines]
    options = [('quiet', 'f'), ('silent', 'f'), ('check', 'f'), ('verbose', 'f')]
    return fmt_uses(uses) + '\n' + fmt_options(options)