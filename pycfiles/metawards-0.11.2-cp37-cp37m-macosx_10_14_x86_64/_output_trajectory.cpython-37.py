# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_output_trajectory.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1569 bytes
from typing import Union as _Union
from .._network import Network
from .._networks import Networks
from .._population import Populations
from .._outputfiles import OutputFiles
__all__ = [
 'output_trajectory']

def output_trajectory(network: _Union[(Network, Networks)], output_dir: OutputFiles, trajectory: Populations, **kwargs) -> None:
    """Call in the "finalise" stage to output the
       population trajectory to the 'trajectory.csv' file
    """
    RESULTS = output_dir.open('trajectory.csv')
    has_date = trajectory[0].date
    if has_date:
        datestring = 'date,'
    else:
        datestring = ''
    RESULTS.write(f"day,{datestring}demographic,S,E,I,R,IW\n")
    for i, pop in enumerate(trajectory):
        if pop.date:
            d = pop.date.isoformat() + ','
        else:
            d = ''
        RESULTS.write(f"{pop.day},{d}overall,{pop.susceptibles},{pop.latent},{pop.total},{pop.recovereds},{pop.n_inf_wards}\n")
        if isinstance(network, Networks):
            for i, demographic in enumerate(network.demographics):
                subpop = pop.subpops[i]
                name = demographic.name
                if not name is None:
                    if len(name) == 0:
                        name = str(i)
                    RESULTS.write(f"{subpop.day},{d}{name},{subpop.susceptibles},{subpop.latent},{subpop.total},{subpop.recovereds},{subpop.n_inf_wards}\n")