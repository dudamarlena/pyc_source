# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/calculations/improve.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2215 bytes
from io import StringIO
from scipy.optimize import fmin_l_bfgs_b
from .exceptions import wrap_exceptions

def setup_project(projectf):
    from pyxrd.file_parsers.json_parser import JSONParser
    from pyxrd.project.models import Project
    type(Project).object_pool.clear()
    f = StringIO(projectf)
    project = JSONParser.parse(f)
    f.close()
    return project


@wrap_exceptions
def run_refinement(projectf, mixture_index):
    """
        Runs a refinement setup for 
            - projectf: project data
            - mixture_index: what mixture in the project to use
    """
    if projectf is not None:
        from pyxrd.data import settings
        settings.initialize()
        project = setup_project(projectf)
        del projectf
        import gc
        gc.collect()
        mixture = project.mixtures[mixture_index]
        mixture.refinement.update_refinement_treestore()
        refiner = mixture.refinement.get_refiner()
        refiner.refine()
        return (
         list(refiner.history.best_solution), refiner.history.best_residual)


@wrap_exceptions
def improve_solution(projectf, mixture_index, solution, residual, l_bfgs_b_kwargs={}):
    if projectf is not None:
        from pyxrd.data import settings
        settings.initialize()
        project = setup_project(projectf)
        del projectf
        mixture = project.mixtures[mixture_index]
        with mixture.data_changed.ignore():
            mixture.update_refinement_treestore()
            refiner = mixture.refinement.get_refiner()
            vals = fmin_l_bfgs_b(
 refiner.get_residual,
 solution, approx_grad=True, 
             bounds=refiner.ranges, **l_bfgs_b_kwargs)
            new_solution, new_residual = tuple(vals[0:2])
        return (
         new_solution, new_residual)
    else:
        return (
         solution, residual)