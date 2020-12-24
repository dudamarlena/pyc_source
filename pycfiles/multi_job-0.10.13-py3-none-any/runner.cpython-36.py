# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/cli/runner.py
# Compiled at: 2020-01-23 17:38:06
# Size of source mod 2**32: 3639 bytes
from os import getcwd
from typing import Any, List, Optional, Mapping
from parser.models import Job, Project, Routine, Subprocess
from parser.utils import join_paths, remove_tags, sub_to_exec, get_tags
from parser.exceptions import ArgumentNotGiven

def resolve(jobs: List[Job], projects: List[Project], routines: List[Routine], full_cli_params: dict, config_path: str) -> None:
    plan = []
    cli_params = {k:v for k, v in full_cli_params.items() if v if v}
    job_dict = {job.name:job for job in jobs}
    routine_dict = {routine.name:routine for routine in routines}
    project_dict = {project.name:project for project in projects}
    for param in cli_params:
        if param in job_dict:
            choice = job_dict[param]
        else:
            if param in routine_dict:
                choice = routine_dict[param]

    if type(choice) is Routine:
        jobs = [job_dict[job] for job in choice.jobs]
    else:
        if type(choice) is Job:
            jobs = [
             choice]
    for job in jobs:
        if job.targets:
            targets = [project_dict[name] for name in job.targets]
        else:
            if job.skips:
                targets = [project_dict[name] for name in list(set(project_dict) - set(job.skips))]
            else:
                targets = [
                 Project(name='Default', config_path=config_path, path=(getcwd()))]
        plan += [make_process(job, cli_params, project) for project in targets]

    output(plan, full_cli_params['--quiet'], full_cli_params['--check'], full_cli_params['--verbose'])


def make_process(job: Job, cli_params: List[Mapping[(str, str)]], project: Optional[Project]) -> Subprocess:
    params = make_params(job, cli_params, project)
    check_params(job, params, project)
    call = make_call(job, params)
    return Subprocess(call,
      cwd=(join_paths(project.config_path, project.path) if project else None),
      description=f"{job.command or job.function} with {params}")


def make_params(job: Job, cli_params: List[Mapping[(str, str)]], project: Optional[Project]) -> List[Mapping[(str, str)]]:
    if job.params:
        cli_params.update(job.params)
    if type(project.params) is dict:
        if job.name in project.params:
            cli_params.update(project.params[job.name])
    return cli_params


def check_params(job: Job, params: List[Mapping[(str, str)]]) -> None:
    specified_params = job.params if job.function else get_tags(job.command)
    if not set(specified_params) <= set(params):
        missing = ', '.join(list(set(specified_params) - set(params)))
        msg = f"When constructing job: {job} for project: {project} no argument for '{missing}' was provided"
        raise ArgumentNotGiven(msg)


def make_call(job: Job, params: List[Mapping[(str, str)]]) -> str:
    if job.command:
        return sub_to_exec(job.command, params)
    if job.function:
        module_path = join_paths(job.config_path, job.function['path'])
        kwargs = ', '.join([f"{remove_tags(k)}={v}" for k, v in params.items() if type(job.params) is dict if remove_tags(k) in job.params])
        return f"getattr(__import__(rsplit({module_path}, '/', 1)), {job.function['name']})({kwargs})"


def output(plan: List[Subprocess], quiet: bool, check: bool, verbose: bool) -> None:
    if not quiet:
        print('Plan:')
        for process in plan:
            print('Run:', process.fmt(verbose))

    if not check:
        for process in plan:
            if not quiet:
                print('Running:', process.fmt(verbose))
            print(process.run())