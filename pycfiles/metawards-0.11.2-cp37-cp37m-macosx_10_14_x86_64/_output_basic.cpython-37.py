# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_output_basic.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 2838 bytes
from .._network import Network
from .._population import Population
from .._outputfiles import OutputFiles
from .._workspace import Workspace
from utils._get_functions import call_function_on_network
__all__ = [
 'output_basic']

def output_basic_serial(network: Network, population: Population, output_dir: OutputFiles, workspace: Workspace, **kwargs):
    """This will write basic trajectory data to the output
       files. This will be the number of infected wards,
       total infections, play infections and work infections
       for each disease stage for each timestep

       Parameters
       ----------
       network: Network
         The network over which the outbreak is being modelled
       population: Population
         The population experiencing the outbreak
       output_dir: OutputFiles
         The directory in which to place all output files
       workspace: Workspace
         A workspace that can be used to extract data
       kwargs
         Extra argumentst that are ignored by this function
    """
    if network.name is None:
        name = ''
    else:
        name = '_' + network.name.replace(' ', '_')
    n_inf_wards_file = output_dir.open(f"NumberWardsInfected{name}.dat")
    total_file = output_dir.open(f"TotalInfections{name}.dat")
    work_file = output_dir.open(f"WorkInfections{name}.dat")
    play_file = output_dir.open(f"PlayInfections{name}.dat")
    ts = f"{population.day} "

    def _join(array):
        return ' '.join([str(x) for x in array])

    total_file.write(str(population.total) + '\n')
    n_inf_wards_file.write(ts + _join(workspace.n_inf_wards) + '\n')
    work_file.write(ts + _join(workspace.inf_tot) + '\n')
    play_file.write(ts + _join(workspace.pinf_tot) + '\n')


def output_basic(nthreads: int=1, **kwargs):
    """This will write basic trajectory data to the output
       files. This will be the number of infected wards,
       total infections, play infections and work infections
       for each disease stage for each timestep

       Parameters
       ----------
       network: Network
         The network over which the outbreak is being modelled
       population: Population
         The population experiencing the outbreak
       output_dir: OutputFiles
         The directory in which to place all output files
       workspace: Workspace
         A workspace that can be used to extract data
       kwargs
         Extra argumentst that are ignored by this function
    """
    call_function_on_network(nthreads=1, func=output_basic_serial, 
     call_on_overall=True, **kwargs)