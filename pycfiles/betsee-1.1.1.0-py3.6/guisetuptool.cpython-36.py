# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/setuptools/guisetuptool.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5634 bytes
"""
High-level support facilities for :mod:`pkg_resources`, a mandatory runtime
dependency simplifying inspection of application dependencies.

Caveats
----------
This submodule partially duplicates the existing
:mod:`betse.lib.setuptools.setuptool` submodule -- specifically, those
functions of that submodule required by the top-level installation-time
``setup.py`` script. Since BETSE is a third-party mandatory dependency of this
application, the :mod:`betse.lib.setuptools.setuptool` submodule provided by
that dependency is *not* necessarily importable from within this application's
``setup.py`` script.

This submodule thus violates the Don't Repeat Yourself (DRY) principle.
Unfortunately, doing so requires dropping support for type validation
implemented by the BETSE-specific :func:`betse.util.type.types.type_check`
decorator.
"""
from betsee.guiexception import BetseeLibException
from collections.abc import Mapping

def convert_requirements_dict_to_tuple(requirements_dict: Mapping) -> tuple:
    """
    Convert the passed dictionary of :mod:`setuptools`-specific requirements
    strings into a tuple of such strings.

    This dictionary is assumed to map from the :mod:`setuptools`-specific
    project name of a third-party dependency (e.g., ``NetworkX``) to the suffix
    of a :mod:`setuptools`-specific requirements string constraining this
    dependency (e.g., ``>= 1.11``). Each element of the resulting tuple is a
    string of the form `{key} {value}`, converted from a key-value pair of this
    dictionary in arbitrary order.

    Parameters
    ----------
    requirements_dict : MappingType
        Dictionary of :mod:`setuptools`-specific requirements strings in the
        format described above.

    Returns
    ----------
    tuple
        Tuple of :mod:`setuptools`-specific requirements strings in the format
        described above.
    """
    return convert_requirements_dict_keys_to_tuple(requirements_dict, *requirements_dict.keys())


def convert_requirements_dict_keys_to_tuple(requirements_dict: Mapping, *requirement_names: str) -> tuple:
    """
    Convert all key-value pairs of the passed dictionary of :mod:`setuptools`-
    specific requirements strings whose keys are the passed strings into a
    tuple of :mod:`setuptools`-specific requirements strings.

    Parameters
    ----------
    requirements_dict : MappingType
        Dictionary of requirements strings.
    requirement_names : Tuple[str]
        Tuple of keys identifying the key-value pairs of this dictionary to
        convert.

    Returns
    ----------
    tuple
        Tuple of :mod:`setuptools`-specific requirements strings in the above
        format.

    Raises
    ----------
    BetseeLibException
        If the passed key is *not* a key of this dictionary.

    See Also
    ----------
    :func:`convert_requirements_dict_to_tuple`
        Further details on the format of this dictionary and resulting strings.
    """
    return tuple(convert_requirements_dict_key_to_str(requirements_dict, requirement_name) for requirement_name in requirement_names)


def convert_requirements_dict_key_to_str(requirements_dict: Mapping, requirement_name: str) -> str:
    """
    Convert the key-value pair of the passed dictionary of :mod:`setuptools`-
    specific requirements strings whose key is the passed string into a
    :mod:`setuptools`-specific requirements string.

    Parameters
    ----------
    requirements_dict : MappingType
        Dictionary of requirements strings.
    requirement_names : str
        Key identifying the key-value pairs of this dictionary to convert.

    Returns
    ----------
    str
        Requirements string converted from this key-value pair.

    Raises
    ----------
    BetseeLibException
        If the passed key is *not* a key of this dictionary.

    See Also
    ----------
    :func:`convert_requirements_dict_to_tuple`
        Further details on the format of this dictionary and resulting string.
    """
    if requirement_name not in requirements_dict:
        raise BetseeLibException('Dependency "{}" unrecognized.'.format(requirement_name))
    requirement_constraints = requirements_dict[requirement_name]
    if requirement_constraints:
        return '{} {}'.format(requirement_name, requirement_constraints)
    else:
        return requirement_name