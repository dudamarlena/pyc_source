# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/julia/julia_require.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 6765 bytes
"""Generates a Dockerfile based on an input matrix with REQUIRE for legacy Julia"""
import os
from ..python import PythonBuildPack

class JuliaRequireBuildPack(PythonBuildPack):
    __doc__ = '\n    Julia build pack which uses conda and REQUIRE.\n    '
    minor_julias = {'0.6':'0.6.4', 
     '0.7':'0.7.0',  '1.0':'1.0.4',  '1.1':'1.1.1'}
    major_julias = {'1': '1.1.1'}

    @property
    def julia_version(self):
        require = self.binder_path('REQUIRE')
        try:
            with open(require) as (f):
                julia_version_line = f.readline().strip()
        except FileNotFoundError:
            julia_version_line = ''

        if not julia_version_line.startswith('julia '):
            self._julia_version = self.minor_julias['0.6']
            return self._julia_version
        else:
            julia_version_info = julia_version_line.split(' ', 1)[1].split('.')
            julia_version = ''
            if len(julia_version_info) == 1:
                julia_version = self.major_julias[julia_version_info[0]]
            else:
                if len(julia_version_info) == 2:
                    julia_version = self.minor_julias['.'.join(julia_version_info)]
                else:
                    julia_version = '.'.join(julia_version_info)
        self._julia_version = julia_version
        return self._julia_version

    def get_build_env(self):
        return super().get_build_env() + [
         ('JULIA_PATH', '${APP_BASE}/julia'),
         ('JULIA_HOME', '${JULIA_PATH}/bin'),
         ('JULIA_BINDIR', '${JULIA_HOME}'),
         ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
         ('JULIA_DEPOT_PATH', '${JULIA_PKGDIR}'),
         (
          'JULIA_VERSION', self.julia_version),
         ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')]

    def get_path(self):
        return super().get_path() + ['${JULIA_HOME}']

    def get_build_scripts(self):
        return super().get_build_scripts() + [
         ('root', '\n                mkdir -p ${JULIA_PATH} && \\\n                curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1\n                '),
         ('root', '\n                mkdir -p ${JULIA_PKGDIR} && \\\n                chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}\n                '),
         ('${NB_USER}', '\n                julia -e \'if (VERSION > v"0.7-") using Pkg; else Pkg.init(); end; Pkg.add("IJulia"); using IJulia;\' && \\\n                mv ${HOME}/.local/share/jupyter/kernels/julia-${JULIA_VERSION%[.-]*}  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-${JULIA_VERSION%[.-]*}\n                ')]

    def get_assemble_scripts(self):
        require = self.binder_path('REQUIRE')
        return super().get_assemble_scripts() + [
         (
          '${NB_USER}',
          '\n            julia /tmp/install-repo-dependencies.jl "%(require)s"\n            ' % {'require': require})]

    def get_build_script_files(self):
        files = {'julia/install-repo-dependencies.jl': '/tmp/install-repo-dependencies.jl'}
        files.update(super().get_build_script_files())
        return files

    def detect(self):
        """
        Check if current repo should be built with the Julia Legacy Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Julia.

        Instead we just check if the path to `REQUIRE` exists and that there is
        no julia 1.0 style environment

        """
        return os.path.exists(self.binder_path('REQUIRE')) and not (os.path.exists(self.binder_path('Project.toml')) or os.path.exists(self.binder_path('JuliaProject.toml')))