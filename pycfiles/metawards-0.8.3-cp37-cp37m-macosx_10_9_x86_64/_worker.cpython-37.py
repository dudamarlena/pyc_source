# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/utils/_worker.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 2776 bytes
from .._network import Network
from .._parameters import Parameters
from .._outputfiles import OutputFiles
import os, sys
from contextlib import contextmanager
__all__ = [
 'run_worker', 'prepare_worker']
global_network = None

@contextmanager
def silence_output():
    """Nice way to silence stdout and stderr - thanks to
       Emil Stenström in
       https://stackoverflow.com/questions/6735917/redirecting-stdout-to-nothing-in-python
    """
    new_out = open(os.devnull, 'w')
    old_out = sys.stdout
    sys.stdout = new_out
    new_err = open(os.devnull, 'w')
    old_err = sys.stderr
    sys.stderr = new_err
    try:
        yield new_out
    finally:
        sys.stdout = old_out
        sys.stderr = old_err


def prepare_worker(params: Parameters):
    """Prepare a worker to receive work to run a model using the passed
       parameters. This will build the network specified by the
       parameters and will store it in global memory ready to
       be used for a model run. Note that these are
       silent, printing nothing to stdout or stderr
    """
    global global_network
    with silence_output():
        if global_network is None:
            global_network = Network.build(params=params, calculate_distances=True,
              profile=False)
        else:
            global_network.update(params)


def run_worker(arguments):
    """Ask the worker to run a model using the passed variables and
       options. This will write to options['output_dir'] and will
       also return the population object that contains the final
       population data.

       WARNING - the iterator and extractor arguments rely on the
       workers starting in the same directory as the main process,
       so that they can load the same python files (if the user
       is using a custom iterator or extractor)
    """
    params = arguments['params']
    options = arguments['options']
    prepare_worker(params)
    from ._runner import redirect_output
    outdir = options['output_dir']
    auto_bzip = options['auto_bzip']
    del options['auto_bzip']
    with OutputFiles(outdir, check_empty=False, force_empty=False, prompt=None,
      auto_bzip=auto_bzip) as (output_dir):
        options['output_dir'] = output_dir
        with redirect_output(output_dir.get_path()):
            output = (global_network.run)(**options)
            return output