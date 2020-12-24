# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/utils/functions.py
# Compiled at: 2020-02-19 16:27:22
# Size of source mod 2**32: 1303 bytes
from subprocess import run
from typing import Any, List, Tuple
from .colours import blue, fail
from .emojis import MUSHROOM, TOPHAT, CROWN, RICE_BALL
from multi_job.models.exceptions import ArgumentMissing, StepError

def get_required_from_context(keys: List[str], context: dict) -> Tuple[(Any, ...)]:
    missing_context = set(keys) - set(context.keys())
    if missing_context:
        msg = 'Missing non-optional arguments caught during runtime' + f"\nMissing context: {list(missing_context)}"
        raise ArgumentMissing(msg)
    context_values = [context[key] for key in keys]
    if len(context_values) == 1:
        return context_values.pop()
    else:
        return context_values


def get_optional_from_context(keys: List[str], context: dict) -> Tuple[(Any, ...)]:
    context_values = [context[key] if key in context else None for key in keys]
    if len(context_values) == 1:
        return context_values.pop()
    else:
        return context_values


def step(process: List[str], path: str) -> None:
    output = run(process, cwd=path)
    if output.returncode != 0:
        msg = f"Step: {process} returned a non zero exit code\nOutput: {output}"
        raise StepError(msg)


success_msg = TOPHAT + blue('Function exited successfully') + CROWN
failure_msg = RICE_BALL + fail('Function failed') + MUSHROOM