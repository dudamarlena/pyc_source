# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_output_incidence.py
# Compiled at: 2020-05-10 15:00:16
# Size of source mod 2**32: 2254 bytes
from .._network import Network
from .._population import Population
from .._outputfiles import OutputFiles
from .._workspace import Workspace
from utils._get_functions import call_function_on_network
__all__ = [
 'output_incidence', 'output_incidence_serial']

def output_incidence_serial(network: Network, population: Population, output_dir: OutputFiles, workspace: Workspace, **kwargs):
    """This will incidence of infection for each ward for each timestep.
       This is the sum of infections from disease class 0 to 2 inclusive

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
    pfile = output_dir.open(f"incidence{name}.dat")
    pfile.write(str(population.day) + ' ')
    pfile.write(' '.join([str(x) for x in workspace.incidence[1:]]) + '\n')


def output_incidence(nthreads: int=1, **kwargs):
    """This will incidence of infection for each ward for each timestep.
       This is the sum of infections from disease class 0 to 2 inclusive

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
    call_function_on_network(nthreads=1, func=output_incidence_serial, 
     call_on_overall=True, **kwargs)