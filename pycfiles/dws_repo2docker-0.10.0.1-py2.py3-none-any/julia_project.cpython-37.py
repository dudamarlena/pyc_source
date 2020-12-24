# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/julia/julia_project.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 5384 bytes
"""Generates a Dockerfile based on an input matrix for Julia"""
import os, toml
from ..python import PythonBuildPack
from .semver import find_semver_match

class JuliaProjectTomlBuildPack(PythonBuildPack):
    __doc__ = '\n    Julia build pack which uses conda.\n    '
    all_julias = [
     '0.7.0',
     '1.0.0',
     '1.0.1',
     '1.0.2',
     '1.0.3',
     '1.0.4',
     '1.1.0',
     '1.1.1',
     '1.2.0']

    @property
    def julia_version(self):
        default_julia_version = self.all_julias[(-1)]
        if os.path.exists(self.binder_path('JuliaProject.toml')):
            project_toml = toml.load(self.binder_path('JuliaProject.toml'))
        else:
            project_toml = toml.load(self.binder_path('Project.toml'))
        if 'compat' in project_toml:
            if 'julia' in project_toml['compat']:
                julia_version_str = project_toml['compat']['julia']
                _julia_version = find_semver_match(julia_version_str, self.all_julias)
                if _julia_version is not None:
                    return _julia_version
        return default_julia_version

    def get_build_env(self):
        return super().get_build_env() + [
         ('JULIA_PATH', '${APP_BASE}/julia'),
         ('JULIA_DEPOT_PATH', '${JULIA_PATH}/pkg'),
         (
          'JULIA_VERSION', self.julia_version),
         ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter'),
         ('JUPYTER_DATA_DIR', '${NB_PYTHON_PREFIX}/share/jupyter')]

    def get_env(self):
        return super().get_env() + [('JULIA_PROJECT', '${REPO_DIR}')]

    def get_path(self):
        return super().get_path() + ['${JULIA_PATH}/bin']

    def get_build_scripts(self):
        return super().get_build_scripts() + [
         ('root', '\n                mkdir -p ${JULIA_PATH} && \\\n                curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1\n                '),
         ('root', '\n                mkdir -p ${JULIA_DEPOT_PATH} && \\\n                chown ${NB_USER}:${NB_USER} ${JULIA_DEPOT_PATH}\n                ')]

    def get_assemble_scripts(self):
        return super().get_assemble_scripts() + [
         ('${NB_USER}', '\n                JULIA_PROJECT="" julia -e "using Pkg; Pkg.add(\\"IJulia\\"); using IJulia; installkernel(\\"Julia\\", \\"--project=${REPO_DIR}\\");" && \\\n                julia --project=${REPO_DIR} -e \'using Pkg; Pkg.instantiate(); pkg"precompile"\'\n                ')]

    def detect(self):
        """
        Check if current repo should be built with the Julia Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Julia.

        Instead we just check if the path to `Project.toml` or
        `JuliaProject.toml` exists.

        """
        return os.path.exists(self.binder_path('Project.toml')) or os.path.exists(self.binder_path('JuliaProject.toml'))