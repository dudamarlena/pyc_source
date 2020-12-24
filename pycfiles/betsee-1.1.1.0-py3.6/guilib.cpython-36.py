# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/guilib.py
# Compiled at: 2019-04-13 01:37:52
# Size of source mod 2**32: 6589 bytes
"""
High-level **application dependency** (i.e., both mandatory and optional
third-party Python packages required by this application) facilities.

This low-level submodule defines functions intended to be called by high-level
submodules (e.g., :mod:`betse.util.cli.cliabc`) *before* attempting to import
any such dependencies.
"""
from betse.lib import libs as betse_libs
from betse.util.type.iterable.mapping import mappings
from betse.util.type.types import type_check
from betsee import guimetadeps

def die_unless_runtime_mandatory_all() -> None:
    """
    Raise an exception unless all mandatory runtime dependencies of this
    application are **satisfiable** (i.e., both importable and of a
    satisfactory version) *and* all external commands required by these
    dependencies (e.g., GraphViz's ``dot`` command) reside in the current
    ``${PATH}``.

    Raises
    ----------
    BetseLibException
        If at least one mandatory runtime dependency is unsatisfiable.

    See Also
    ----------
    :func:`betse_libs.die_unless_runtime_mandatory_all`
        Further details.
    """
    RUNTIME_MANDATORY_SANS_BETSE = mappings.copy_map_sans_key(mapping=(guimetadeps.RUNTIME_MANDATORY),
      key='BETSE')
    betse_libs.die_unless_requirements_dict(RUNTIME_MANDATORY_SANS_BETSE)


@type_check
def die_unless_runtime_optional(*requirement_names: str) -> None:
    """
    Raise an exception unless all optional runtime dependencies of this
    application with the passed :mod:`setuptools`-specific project names are
    **satisfiable** (i.e., both importable and of a satisfactory version)
    *and* all external commands required by these dependencies (e.g.,
    GraphViz's ``dot`` command) reside in the current ``${PATH}``.

    Parameters
    ----------
    requirement_names : Tuple[str]
        Tuple of the names of all :mod:`setuptools`-specific projects
        implementing these dependencies (e.g., ``NetworkX``). If any such name
        is unrecognized (i.e., is *not* a key of the
        :data:`guimetadeps.RUNTIME_OPTIONAL` dictionary), an exception is
        raised.

    Raises
    ----------
    BetseLibException
        If at least one such dependency is unsatisfiable.

    See Also
    ----------
    :func:`betse_libs.die_unless_runtime_mandatory_all`
        Further details.
    """
    (betse_libs.die_unless_requirements_dict_keys)(guimetadeps.RUNTIME_OPTIONAL, *requirement_names)


@type_check
def is_runtime_optional(*requirement_names: str) -> bool:
    """
    ``True`` only if all optional runtime dependencies of this application with
    the passed :mod:`setuptools`-specific project names are **satisfiable**
    (i.e., both importable and of a satisfactory version) *and* all external
    commands required by these dependencies (e.g., GraphViz's ``dot`` command)
    reside in the current ``${PATH}``.

    Parameters
    ----------
    requirement_names : Tuple[str]
        Tuple of the names of all :mod:`setuptools`-specific projects
        implementing these dependencies (e.g., ``NetworkX``). If any such
        name is *not* a key of the :data:`guimetadeps.RUNTIME_OPTIONAL`
        dictionary and is thus unrecognized, an exception is raised.

    See Also
    ----------
    :func:`betse_libs.die_unless_runtime_mandatory_all`
        Further details.
    """
    return (betse_libs.is_requirements_dict_keys)(guimetadeps.RUNTIME_OPTIONAL, *requirement_names)


@type_check
def import_runtime_optional(*requirement_names: str) -> object:
    """
    Import and return the top-level module object satisfying each optional
    runtime dependency of this application with the passed name.

    Parameters
    ----------
    requirement_names : tuple[str]
        Tuple of the names of all :mod:`setuptools`-specific projects
        implementing these dependencies (e.g., ``NetworkX``). If any such name
        is unrecognized (i.e., is *not* a key of the
        :data:`guimetadeps.RUNTIME_OPTIONAL` dictionary), an exception is
        raised.

    See Also
    ----------
    :func:`betse_libs.import_requirements_dict_keys`
        Further details.
    """
    return (betse_libs.import_requirements_dict_keys)(guimetadeps.RUNTIME_OPTIONAL, *requirement_names)