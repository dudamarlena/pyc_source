# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/__init__.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 1869 bytes
from .cnf import CNF
from .graphs import readGraph, writeGraph
from .cnfgen import command_line_utility as cnfgen
__all__ = [
 'CNF', 'readGraph', 'writeGraph']

def _load_formula_generators():
    """Load CNF generators from `cnfformula.families`.

    This code explores the submodules of `cnfformula.families` and
    load the formula generators, or at least the objects marked as
    such with the `cnfformula.families.register_cnf_generator`
    function decorator.
    """
    import sys
    from . import families
    from .cmdline import find_methods_in_package
    from .families import is_cnf_generator
    loot = dict((g.__name__, g) for g in find_methods_in_package(families, is_cnf_generator))
    self_ref = sys.modules[__name__]
    self_ref.__dict__.update(loot)
    __all__.extend(name for name in loot.keys() if name not in __all__)


def _load_formula_transformations():
    """Load CNF transformations from `cnfformula.transformations`.

    This code explores the submodules of `cnfformula.transformations` and
    load the formula transformations, or at least the objects marked as
    such with the `cnfformula.transformations.register_cnf_transformation`
    function decorator.
    """
    import sys
    from . import transformations
    from .cmdline import find_methods_in_package
    from .transformations import is_cnf_transformation
    loot = dict((g.__name__, g) for g in find_methods_in_package(transformations, is_cnf_transformation))
    self_ref = sys.modules[__name__]
    self_ref.__dict__.update(loot)
    __all__.extend(name for name in loot.keys() if name not in __all__)


_load_formula_generators()
_load_formula_transformations()