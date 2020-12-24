# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: qatools/main.py
# Compiled at: 2018-07-15 10:16:21
# Size of source mod 2**32: 5777 bytes
"""
Sample implementation of a CLI wrapper using qatools.
"""
import subprocess, time
from pathlib import Path
from qatools.config import on_windows, on_linux, on_lsf, on_vdi
from qatools.config import is_ci

def find_executable():
    """Returns the executable's path.
  The only different between running on Windows, Linux, LSF or the CI
  should be where the executable is located.
  Of course, if your code is pure python, you don't have to worry about this.
  """
    if is_ci or on_lsf or on_vdi:
        executable = 'build/sample_project'
    else:
        if on_windows:
            executable = 'x64/release/sample_project.exe'
        else:
            executable = 'build/sample_project'
    return Path(executable)


def find_working_directory():
    """
  It's usually best to execute programs from what "should" be their working directory.
  The QA tools are executed from the project's root; but maybe you expect a different location.
  If you need this, either cd into it in your CLI invokation, or pass it as some "working_directory" to your executable.
  """
    if is_ci:
        working_directory = ''
    else:
        working_directory = ''
    return Path(working_directory)


def run(context):
    """Sample implementation of a run() function."""
    command = ' '.join([
     f'cd "{find_working_directory()}";{find_executable()}',
     '--paramfile configurations/base.json',
     '--no-live-view --no-movie' if is_ci else '',
     ' '.join([f"--paramfile configurations/{c}.json" for c in context.obj['configuration'].split(':')]),
     f"--paramfile {context.obj['tuning_filepath']}" if 'tuning_filepath' in context.obj else '',
     f"""--input "{context.obj['database'] / context.obj['input_path']}"""",
     f"""--output "{context.obj['output_directory']}"""",
     ' '.join(context.obj['forwarded_args'])])
    print(command)
    if context.obj['dryrun']:
        return
    else:
        start = time.time()
        pipes = subprocess.Popen(command, shell=True,
          encoding='utf-8',
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        std_out, std_err = pipes.communicate()
        print(std_err.strip(), std_out.strip())
        return {'compute_time': time.time() - start}


from utils import read_poses, drift_after_loop_metrics, objective_metrics

def postprocess(runtime_metrics, context):
    """
  Postprocessing functions should
    1. return a dict with metrics to save in metrics.json
    2. Create any qualitative outputs you would like to view later (images, movies...)
  args:
    context: Click.Context, context.obj has information from the CLI arguments
    runtime_metrics: metrics from the run
  """
    poses_path = context.obj['output_directory'] / 'camera_poses_debug.txt'
    metrics = {'is_failed': not poses_path.exists()}
    if metrics['is_failed']:
        return metrics
    else:
        poses_estimated = read_poses(poses_path)
        metrics = {**metrics, **runtime_metrics, **(drift_after_loop_metrics(poses_estimated))}
        ground_truth_path = context.obj['database'] / context.obj['input_path'].parent / 'GT_final.txt'
        if ground_truth_path.exists():
            print('INFO: found ground truth')
            poses_groundtruth = read_poses(ground_truth_path)
            metrics = {**metrics, **(objective_metrics(poses_estimated, poses_groundtruth))}
        return metrics