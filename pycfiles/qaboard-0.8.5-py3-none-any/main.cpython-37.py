# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: qaboard/sample_project/qa/main.py
# Compiled at: 2020-03-15 11:02:25
# Size of source mod 2**32: 3986 bytes
"""
Sample implementation of a CLI wrapper using qatools.
"""
import sys, subprocess
from pathlib import Path
import click
from qaboard.config import is_ci

def run(context):
    """
  Runs you code, creates files under context.obj["output_directory], and returns metrics.
  """
    context.obj['parameters'] = {}
    for c in context.obj['configurations']:
        if isinstance(c, dict):
            context.obj['parameters'].update(c)

    if context.obj['extra_parameters']:
        context.obj['parameters'].update(context.obj['extra_parameters'])
    click.secho('TODO: Run *your* code using...', fg='cyan', bold=True)
    useful_context_keys = ('absolute_input_path', 'configurations', 'extra_parameters',
                           'parameters', 'platform', 'output_directory', 'forwarded_args')
    for key in useful_context_keys:
        click.secho(f" * {key}:  {context.obj[key]}", fg='cyan')

    arg_format = lambda a: (a.format)(**{**globals(), **locals(), **context.obj, **context.obj['parameters']})
    click.secho('Until then we run the extra CLI flags you gave qa. (e.g. qa run --input my/input.jpg echo OK)', fg='cyan', bold=True)
    command = ' '.join([arg_format(a) for a in context.obj['forwarded_args']])
    if command:
        click.secho(command)
    else:
        click.secho((f"Try to run something! eg '{' '.join(sys.argv[:1])}" + "echo {absolute_input_path}'"), fg='yellow')
        return {'is_failed': False}
        if context.obj['dryrun']:
            return
        pipe = subprocess.PIPE
        with subprocess.Popen(command, shell=True, cwd=(context.obj['output_directory']),
          encoding='utf-8',
          stdout=pipe,
          stderr=pipe) as (process):
            for line in process.stdout:
                print(line)

            process.wait()
            if process.returncode:
                return {'is_failed':True, 
                 'returncode':process.returncode}
            return {'is_failed': False}
        click.secho('TODO: Create plots/graphs...', fg='cyan', bold=True)
        click.secho('TODO: Return metrics...', fg='cyan', bold=True)
        return {'is_failed': False}