# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mi/marscher/sources/mdtraj/examples/test_examples.py
# Compiled at: 2018-02-27 10:14:14
# Size of source mod 2**32: 2098 bytes
"""
Execute each notebook as a test, reporting an error if any cell throws an exception.
Adapted from https://gist.github.com/minrk/2620876.
"""
from __future__ import print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys, nbformat, pytest
from jupyter_client import KernelManager
from six.moves.queue import Empty
FLAKEY_LIST = [
 'centroids.ipynb', 'native-contact.ipynb']
TIMEOUT = 60
test_dir = os.path.dirname(os.path.abspath(__file__))
examples = [pytest.mark.flaky(fn) if fn in FLAKEY_LIST else fn for fn in os.listdir(test_dir) if fn.endswith('.ipynb')]

@pytest.fixture(params=examples)
def example_fn(request):
    if 'openmm' in request.param:
        try:
            from simtk.openmm import app
        except ImportError:
            pytest.skip('Openmm required for example notebook `{}`'.format(request.param))

    cwd = os.path.abspath('.')
    os.chdir(test_dir)
    yield request.param
    os.chdir(cwd)


def test_example_notebook(example_fn):
    with open(example_fn) as (f):
        nb = nbformat.reads(f.read(), nbformat.NO_CONVERT)
    run_notebook(nb)


def run_notebook(nb):
    km = KernelManager()
    km.start_kernel(stderr=(open(os.devnull, 'w')))
    kc = km.client()
    kc.start_channels()
    shell = kc.shell_channel
    kc.execute('pass')
    shell.get_msg()
    failures = 0
    for cell in nb.cells:
        if cell.cell_type != 'code':
            pass
        else:
            kc.execute(cell.source)
            try:
                reply = shell.get_msg(timeout=TIMEOUT)['content']
            except Empty:
                raise Exception('Timeout (%.1f) when executing the following %s cell: "%s"' % (
                 TIMEOUT, cell.cell_type, cell.source.strip()))

            if reply['status'] == 'error':
                failures += 1
                print('\nFAILURE:', file=(sys.stderr))
                print(('\n'.join(reply['traceback'])), file=(sys.stderr))
                print(file=(sys.stderr))

    kc.stop_channels()
    km.shutdown_kernel()
    del km
    if failures > 0:
        raise Exception()