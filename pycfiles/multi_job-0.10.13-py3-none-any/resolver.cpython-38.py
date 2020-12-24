# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/runtime/resolver.py
# Compiled at: 2020-02-01 17:12:42
# Size of source mod 2**32: 1471 bytes
from typing import List, Optional, Mapping, Tuple
from utils.strings import has_prefix
from utils.tags import is_tagged, strip_tags
from models.models import Job, Project, Routine, Process

def resolve(jobs: List[Job], projects: List[Project], routines: List[Routine], cli_params: dict, config_path: str) -> Tuple[(List[Process], Mapping[(str, bool)])]:
    choice, overrides, options = parse_cli_params(cli_params)
    chosen_jobs = resolve_job_matches(choice, jobs, routines)
    processes = [job.resolve_process(target, overrides, config_path) for job in chosen_jobs for target in job.resolve_targets(projects)]
    return (
     processes, options)


def parse_cli_params(cli_params) -> Tuple[(str, dict, dict)]:
    choice = [k for k, v in cli_params.items() if not is_tagged(k) if not has_prefix(k, '--') if v].pop()
    overrides = {v:strip_tags(k) for k, v in cli_params.items() if is_tagged(k) if is_tagged(k)}
    options = {v:k[2:] for k, v in cli_params.items() if has_prefix(k, '--') if has_prefix(k, '--')}
    return (choice, overrides, options)


def resolve_job_matches(choice: str, jobs: List[Job], routines: List[Routine]) -> List[Job]:
    chosen_routine = next((routine for routine in routines if routine.name == choice), None)
    chosen_jobs = [job for job in jobs if chosen_routine and job.name in chosen_routine.jobs or job.name == choice]
    return chosen_jobs