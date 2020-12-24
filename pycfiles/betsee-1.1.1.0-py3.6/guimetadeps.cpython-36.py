# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guimetadeps.py
# Compiled at: 2019-10-10 00:42:33
# Size of source mod 2**32: 13225 bytes
"""
Metadata constants synopsizing high-level application dependencies.
"""
from betsee.guimetadata import VERSION
from collections import namedtuple
SETUPTOOLS_VERSION_MIN = '38.2.0'
BETSE_VERSION = VERSION[:VERSION.rindex('.')]
RUNTIME_MANDATORY = {'BETSE':'== ' + BETSE_VERSION, 
 'PySide2':'', 
 'PySide2.QtGui':'', 
 'PySide2.QtSvg':'', 
 'PySide2.QtWidgets':''}
RUNTIME_OPTIONAL = {'pyside2uic': ''}
TESTING_MANDATORY = {'pytest':'>= 3.7.0', 
 'pytest-qt':'>= 3.2.0', 
 'pytest-xvfb':'>= 1.2.0'}
RequirementCommand = namedtuple('RequirementCommand', ('name', 'basename'))
RequirementCommand.__doc__ = '\n    Lightweight metadata describing a single external command required by an\n    application dependency of arbitrary type (including optional, mandatory,\n    runtime, testing, and otherwise).\n\n    Attributes\n    ----------\n    name : str\n        Human-readable name associated with this command (e.g., ``Graphviz``).\n    basename : str\n        Basename of this command to be searched for in the current ``${PATH}``.\n    '
REQUIREMENT_NAME_TO_COMMANDS = {'pytest-xvfb': (RequirementCommand(name='Xvfb', basename='Xvfb'),)}

def get_runtime_mandatory_tuple() -> tuple:
    """
    Tuple listing the :mod:`setuptools`-specific requirement string containing
    the mandatory name and optional version and extras constraints of each
    mandatory runtime dependency for this application, dynamically converted
    from the :data:`metadata.RUNTIME_MANDATORY` dictionary.

    Caveats
    ----------
    This dictionary notably excludes all submodules whose fully-qualified names
    are prefixed by ``PySide2.`` (e.g., :mod:`PySide2.QtGui`). These submodules
    signify optional :mod:`PySide2` components required by this application but
    unavailable on PyPI. Including these submodules here would erroneously halt
    setuptools-based installation for up to several minutes with output
    resembling:

        Searching for PySide2.QtSvg
        Reading https://pypi.python.org/simple/PySide2.QtSvg/
        Couldn't find index page for 'PySide2.QtSvg' (maybe misspelled?)
        Scanning index of all packages (this may take a while)
        Reading https://pypi.python.org/simple/
    """
    from betsee.lib.setuptools import guisetuptool
    runtime_mandatory_sans_submodules = {dependency_name:dependency_constraints for dependency_name, dependency_constraints in RUNTIME_MANDATORY.items() if not dependency_name.startswith(('PySide2.',
                                                                                                                                                                                            'pyside2uic')) if not dependency_name.startswith(('PySide2.',
                                                                                                                                                                                                                                              'pyside2uic'))}
    return guisetuptool.convert_requirements_dict_to_tuple(runtime_mandatory_sans_submodules)


def get_runtime_optional_tuple() -> tuple:
    """
    Tuple listing the :mod:`setuptools`-specific requirement string containing
    the mandatory name and optional version and extras constraints of each
    optional runtime dependency for this application, dynamically converted
    from the :data:`metadata.RUNTIME_OPTIONAL` dictionary.
    """
    from betsee.lib.setuptools import guisetuptool
    return guisetuptool.convert_requirements_dict_to_tuple(RUNTIME_OPTIONAL)


def get_testing_mandatory_tuple() -> tuple:
    """
    Tuple listing the :mod:`setuptools`-specific requirement string containing
    the mandatory name and optional version and extras constraints of each
    mandatory testing dependency for this application, dynamically converted
    from the :data:`metadata.TESTING_MANDATORY` dictionary.
    """
    from betsee.lib.setuptools import guisetuptool
    return guisetuptool.convert_requirements_dict_to_tuple(TESTING_MANDATORY)