# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridjug/grid_jug.py
# Compiled at: 2015-08-24 13:16:46
# Size of source mod 2**32: 4668 bytes
from __future__ import absolute_import, division, print_function
import io
try:
    from contextlib import redirect_stdout
except ImportError:
    import sys
    from contextlib import contextmanager

    @contextmanager
    def redirect_stdout(new_target):
        old_target, sys.stdout = sys.stdout, new_target
        try:
            yield new_target
        finally:
            sys.stdout = old_target


def grid_jug(jugfile, jugdir=None, jug_args=None, jug_nworkers=4, name='gridjug', keep_going=False, verbose=False, capture_jug_stdout=False, **kwargs):
    """
    A light-weight wrapper to run Jug with GridMap on a Grid Engine cluster

    From their own description, GridMap is a package that allows to easily
    create jobs on a Grid Engine powered cluster directly from Python.
    This wrapper lets GridMap simply spawn several jug-execute workers on a
    Grid Engine cluster.
    Thus we have the benefit of programmatic (reproducible) execution of Jug
    processes.
    Furthermore, GridMap adds a convenient monitoring and reporting layer.
    Under the hood, of course, Jug keeps doing the actual work.

    Parameters
    ----------
    jugfile : path
        Path to the jugfile

    jugdir : path
        Where to save intermediate results

    jug_args : list
        Other jug command-line arguments.
        Note that ``'execute'`` is already included.
        The command line is roughly equivalent to:

            'jug execute {jugfile} ' + ' '.join(jug_args)

    jug_nworkers : int, optional
        number of Grid Engine tasks to start
        (i.e. number of times 'jug execute' is run)

    name : str, optional
        base name of the Grid Engine task

    keep_going : bool, optional
        Strongly recommended! Defaults to ``False``: if a single Jug task
        fails, GridMap will cancel all jobs!
        If ``True``, Jug does not raise an exception but keeps retrying the
        task.

    verbose : bool, optional
        If ``True``, Jug logs ``INFO`` events

    capture_jug_stdout : bool, optional
        Defaults to ``False``.
        If ``True``, captures Jug's task summary printed to stdout.

    **kwargs : keyword-dict, optional
        additional options passed through to :any:`gridmap.grid_map`

    See Also
    --------

    :any:`gridmap.grid_map` : The map function

    `Jug subcommands <http://jug.readthedocs.org/en/latest/subcommands.html>`_

    """
    import gridmap
    jug_argv = [
     'jug', 'execute']
    jug_argv.append('{}'.format(jugfile))
    if jugdir is not None:
        jug_argv.append('--jugdir={}'.format(jugdir))
    if keep_going:
        jug_argv.append('--keep-going')
    if verbose:
        jug_argv.append('--verbose=INFO')
    if jug_args is not None:
        jug_argv.extend(jug_args)
    args_list = jug_nworkers * [[capture_jug_stdout, jug_argv]]
    return gridmap.grid_map(f=_jug_main, args_list=args_list, name=name, **kwargs)


def _jug_main(capture_stdout, *args, **kwargs):
    """
    wrapper function for pickle
    """
    import jug
    if capture_stdout:
        f = io.StringIO()
        with redirect_stdout(f):
            ret = jug.jug.main(*args, **kwargs)
    else:
        ret = jug.jug.main(*args, **kwargs)
    return ret