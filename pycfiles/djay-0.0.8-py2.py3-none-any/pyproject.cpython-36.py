# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/pyproject.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 6464 bytes
from __future__ import absolute_import
import io, os, sys
from pip._vendor import pytoml, six
from pip._internal.exceptions import InstallationError
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Tuple, Optional, List

def _is_list_of_str(obj):
    return isinstance(obj, list) and all(isinstance(item, six.string_types) for item in obj)


def make_pyproject_path(setup_py_dir):
    path = os.path.join(setup_py_dir, 'pyproject.toml')
    if six.PY2:
        if isinstance(path, six.text_type):
            path = path.encode(sys.getfilesystemencoding())
    return path


def load_pyproject_toml(use_pep517, pyproject_toml, setup_py, req_name):
    """Load the pyproject.toml file.

    Parameters:
        use_pep517 - Has the user requested PEP 517 processing? None
                     means the user hasn't explicitly specified.
        pyproject_toml - Location of the project's pyproject.toml file
        setup_py - Location of the project's setup.py file
        req_name - The name of the requirement we're processing (for
                   error reporting)

    Returns:
        None if we should use the legacy code path, otherwise a tuple
        (
            requirements from pyproject.toml,
            name of PEP 517 backend,
            requirements we should check are installed after setting
                up the build environment
        )
    """
    has_pyproject = os.path.isfile(pyproject_toml)
    has_setup = os.path.isfile(setup_py)
    if has_pyproject:
        with io.open(pyproject_toml, encoding='utf-8') as (f):
            pp_toml = pytoml.load(f)
        build_system = pp_toml.get('build-system')
    else:
        build_system = None
    if has_pyproject:
        if not has_setup:
            if use_pep517 is not None:
                if not use_pep517:
                    raise InstallationError('Disabling PEP 517 processing is invalid: project does not have a setup.py')
            use_pep517 = True
        elif build_system and 'build-backend' in build_system:
            if use_pep517 is not None:
                if not use_pep517:
                    raise InstallationError('Disabling PEP 517 processing is invalid: project specifies a build backend of {} in pyproject.toml'.format(build_system['build-backend']))
            use_pep517 = True
        else:
            if use_pep517 is None:
                use_pep517 = has_pyproject
        assert use_pep517 is not None
        return use_pep517 or None
    else:
        if build_system is None:
            build_system = {'requires':[
              'setuptools>=40.8.0', 'wheel'], 
             'build-backend':'setuptools.build_meta:__legacy__'}
        else:
            if not build_system is not None:
                raise AssertionError
            else:
                error_template = '{package} has a pyproject.toml file that does not comply with PEP 518: {reason}'
                if 'requires' not in build_system:
                    raise InstallationError(error_template.format(package=req_name, reason="it has a 'build-system' table but not 'build-system.requires' which is mandatory in the table"))
                requires = build_system['requires']
                raise _is_list_of_str(requires) or InstallationError(error_template.format(package=req_name,
                  reason="'build-system.requires' is not a list of strings."))
            backend = build_system.get('build-backend')
            check = []
            if backend is None:
                backend = 'setuptools.build_meta:__legacy__'
                check = ['setuptools>=40.8.0', 'wheel']
        return (
         requires, backend, check)