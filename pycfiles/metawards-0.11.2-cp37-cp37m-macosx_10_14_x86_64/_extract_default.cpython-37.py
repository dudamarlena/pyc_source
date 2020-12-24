# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_extract_default.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 1746 bytes
from typing import List as _List
from utils._get_functions import MetaFunction
__all__ = [
 'extract_default']

def extract_default(stage: str, **kwargs) -> _List[MetaFunction]:
    """This returns the default list of 'output_XXX' functions that
       are called in sequence for each iteration of the model run.
       These functions are used to output data to files for
       future processing

       Parameters
       ----------
       stage: str
         Which stage of the day is to be modelled

       Returns
       -------
       funcs: List[MetaFunction]
         The list of functions that will be called in sequence
    """
    if stage == 'initialise':
        from ._output_core import setup_core, output_core
        return [
         setup_core, output_core]
    if stage == 'infect':
        from ._output_core import output_core
        return [
         output_core]
    if stage == 'analyse':
        from ._output_basic import output_basic
        from ._output_dispersal import output_dispersal
        from ._output_incidence import output_incidence
        from ._output_prevalence import output_prevalence
        return [output_basic, output_dispersal,
         output_incidence, output_prevalence]
    if stage == 'finalise':
        from ._output_trajectory import output_trajectory
        return [
         output_trajectory]
    if stage == 'summary':
        from ._output_final_report import output_final_report
        return [output_final_report]
    return []