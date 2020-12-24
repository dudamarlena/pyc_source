# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mount/SDC/crowdai/repo2docker/repo2docker/buildpacks/julia.py
# Compiled at: 2018-06-09 10:26:45
# Size of source mod 2**32: 4594 bytes
__doc__ = 'Generates a Dockerfile based on an input matrix for Julia'
import os
from .conda import CondaBuildPack

class JuliaBuildPack(CondaBuildPack):
    """JuliaBuildPack"""

    def get_env(self):
        return super().get_env() + [
         ('JULIA_PATH', '${APP_BASE}/julia'),
         ('JULIA_HOME', '${JULIA_PATH}/bin'),
         ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
         ('JULIA_VERSION', '0.6.0'),
         ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')]

    def get_path(self):
        return super().get_path() + ['${JULIA_HOME}']

    def get_build_scripts(self):
        return super().get_build_scripts() + [
         ('root', '\n                mkdir -p ${JULIA_PATH} && \\\n                curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1\n                '),
         ('root', '\n                mkdir -p ${JULIA_PKGDIR} && \\\n                chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}\n                '),
         ('${NB_USER}', '\n                julia -e \'Pkg.init(); Pkg.add("IJulia"); using IJulia;\' && \\\n                mv ${HOME}/.local/share/jupyter/kernels/julia-0.6  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-0.6\n                ')]

    def get_assemble_scripts(self):
        require = self.binder_path('REQUIRE')
        return super().get_assemble_scripts() + [
         (
          '${NB_USER}',
          '\n            cat "%(require)s" >> ${JULIA_PKGDIR}/v0.6/REQUIRE && \\\n            julia -e \' \\\n               Pkg.resolve(); \\\n               for pkg in keys(Pkg.Reqs.parse("%(require)s")) \\\n                pkg != "julia" && eval(:(using $(Symbol(pkg)))) \\\n               end \\\n            \'\n            ' % {'require': require})]

    def detect(self):
        """
        Check if current repo should be built with the Julia Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Julia.

        Instead we just check if the path to `REQUIRE` exists

        """
        return os.path.exists(self.binder_path('REQUIRE'))