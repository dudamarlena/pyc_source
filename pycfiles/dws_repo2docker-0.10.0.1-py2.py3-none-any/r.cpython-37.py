# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/r.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 16132 bytes
import re, os, datetime
import distutils.version as V
from .python import PythonBuildPack

class RBuildPack(PythonBuildPack):
    __doc__ = '\n    Setup R for use with a repository\n\n    This sets up R + RStudio + IRKernel for a repository that contains:\n\n    1. A `runtime.txt` file with the text:\n\n       r-<year>-<month>-<date>\n\n       Where \'year\', \'month\' and \'date\' refer to a specific\n       date snapshot of https://mran.microsoft.com/timemachine\n       from which libraries are to be installed.\n\n    2. A `DESCRIPTION` file signaling an R package\n\n    3. A Stencila document (*.jats.xml) with R code chunks (i.e. language="r")\n\n    If there is no `runtime.txt`, then the MRAN snapshot is set to latest\n    date that is guaranteed to exist across timezones.\n\n    Additional R packages are installed if specified either\n\n    - in a file `install.R`, that will be executed at build time,\n      and can be used for installing packages from both MRAN and GitHub\n\n    - as dependencies in a `DESCRIPTION` file\n\n    - are needed by a specific tool, for example the package `stencila` is\n      installed and configured if a Stencila document is given.\n\n    The `r-base` package from Ubuntu apt repositories is used to install\n    R itself, rather than any of the methods from https://cran.r-project.org/.\n    '

    @property
    def runtime(self):
        """
        Return contents of runtime.txt if it exists, '' otherwise
        """
        runtime_path = hasattr(self, '_runtime') or self.binder_path('runtime.txt')
        try:
            with open(runtime_path) as (f):
                self._runtime = f.read().strip()
        except FileNotFoundError:
            self._runtime = ''

        return self._runtime

    @property
    def r_version(self):
        """Detect the R version for a given `runtime.txt`

        Will return the version specified by the user or the current default
        version.
        """
        version_map = {'3.4':'3.4', 
         '3.5':'3.5.3-1bionic', 
         '3.5.0':'3.5.0-1bionic', 
         '3.5.1':'3.5.1-2bionic', 
         '3.5.2':'3.5.2-1bionic', 
         '3.5.3':'3.5.3-1bionic', 
         '3.6':'3.6.1-3bionic', 
         '3.6.0':'3.6.0-2bionic', 
         '3.6.1':'3.6.1-3bionic'}
        r_version = '3.6'
        if not hasattr(self, '_r_version'):
            parts = self.runtime.split('-')
            if len(parts) == 5:
                r_version = parts[1]
                if r_version not in version_map:
                    raise ValueError("Version '{}' of R is not supported.".format(r_version))
            self._r_version = version_map.get(r_version)
        return self._r_version

    @property
    def checkpoint_date(self):
        """
        Return the date of MRAN checkpoint to use for this repo

        Returns '' if no date is specified
        """
        if not hasattr(self, '_checkpoint_date'):
            match = re.match('r-(\\d.\\d(.\\d)?-)?(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)', self.runtime)
            if not match:
                self._checkpoint_date = False
            else:
                self._checkpoint_date = (datetime.date)(*[int(s) for s in match.groups()[-3:]])
        return self._checkpoint_date

    def detect(self):
        """
        Check if current repo should be built with the R Build pack

        super().detect() is not called in this function - it would return
        false unless a `requirements.txt` is present and we do not want
        to require the presence of a `requirements.txt` to use R.
        """
        if self.checkpoint_date:
            return True
        description_R = 'DESCRIPTION'
        if self.binder_dir or os.path.exists(description_R) or 'r' in self.stencila_contexts:
            if not self.checkpoint_date:
                self._checkpoint_date = datetime.date.today() - datetime.timedelta(days=2)
                self._runtime = 'r-{}'.format(str(self._checkpoint_date))
            return True

    def get_path(self):
        return super().get_path() + ['/usr/lib/rstudio-server/bin/']

    def get_build_env(self):
        return super().get_build_env() + [
         ('R_LIBS_USER', '${APP_BASE}/rlibs')]

    def get_packages(self):
        packages = [
         'psmisc',
         'libapparmor1',
         'sudo',
         'lsb-release']
        if V(self.r_version) < V('3.5'):
            packages.append('r-base')
        return super().get_packages().union(packages)

    def get_build_scripts(self):
        rstudio_url = 'https://download2.rstudio.org/rstudio-server-1.1.419-amd64.deb'
        rstudio_checksum = '24cd11f0405d8372b4168fc9956e0386'
        shiny_url = 'https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.7.907-amd64.deb'
        shiny_checksum = '78371a8361ba0e7fec44edd2b8e425ac'
        devtools_version = '2018-02-01'
        irkernel_version = '1.0.2'
        mran_url = 'https://mran.microsoft.com/snapshot/{}'.format(self.checkpoint_date.isoformat())
        scripts = []
        if V(self.r_version) >= V('3.5'):
            scripts += [
             ('root', '\n                    echo "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/" > /etc/apt/sources.list.d/r3.6-ubuntu.list\n                    '),
             ('root', '\n                    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9\n                    '),
             (
              'root',
              '\n                    apt-get update && \\\n                    apt-get install --yes r-base={} && \\\n                    apt-get -qq purge && \\\n                    apt-get -qq clean && \\\n                    rm -rf /var/lib/apt/lists/*\n                    '.format(self.r_version))]
        else:
            scripts += [
             ('root', '\n                mkdir -p ${R_LIBS_USER} && \\\n                chown -R ${NB_USER}:${NB_USER} ${R_LIBS_USER}\n                '),
             (
              'root',
              "\n                curl --silent --location --fail {rstudio_url} > /tmp/rstudio.deb && \\\n                echo '{rstudio_checksum} /tmp/rstudio.deb' | md5sum -c - && \\\n                dpkg -i /tmp/rstudio.deb && \\\n                rm /tmp/rstudio.deb\n                ".format(rstudio_url=rstudio_url,
                rstudio_checksum=rstudio_checksum)),
             (
              'root',
              "\n                curl --silent --location --fail {url} > {deb} && \\\n                echo '{checksum} {deb}' | md5sum -c - && \\\n                dpkg -i {deb} && \\\n                rm {deb}\n                ".format(url=shiny_url,
                checksum=shiny_checksum,
                deb='/tmp/shiny.deb')),
             ('root', '\n                sed -i -e \'/^R_LIBS_USER=/s/^/#/\' /etc/R/Renviron && \\\n                echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron\n                '),
             ('${NB_USER}', '\n                pip install --no-cache-dir https://github.com/jupyterhub/jupyter-server-proxy/archive/7ac0125.zip && \\\n                pip install --no-cache-dir jupyter-rsession-proxy==1.0b6 && \\\n                jupyter serverextension enable jupyter_server_proxy --sys-prefix && \\\n                jupyter nbextension install --py jupyter_server_proxy --sys-prefix && \\\n                jupyter nbextension enable --py jupyter_server_proxy --sys-prefix\n                '),
             (
              '${NB_USER}',
              '\n                R --quiet -e "install.packages(\'devtools\', repos=\'https://mran.microsoft.com/snapshot/{devtools_version}\', method=\'libcurl\')" && \\\n                R --quiet -e "devtools::install_github(\'IRkernel/IRkernel\', ref=\'{irkernel_version}\')" && \\\n                R --quiet -e "IRkernel::installspec(prefix=\'$NB_PYTHON_PREFIX\')"\n                '.format(devtools_version=devtools_version,
                irkernel_version=irkernel_version)),
             (
              '${NB_USER}',
              '\n                R --quiet -e "install.packages(\'shiny\', repos=\'{}\', method=\'libcurl\')"\n                '.format(mran_url)),
             (
              'root',
              '\n                echo "options(repos = c(CRAN=\'{mran_url}\'), download.file.method = \'libcurl\')" > /etc/R/Rprofile.site\n                '.format(mran_url=mran_url)),
             ('root', '\n                install -o ${NB_USER} -g ${NB_USER} -d /var/log/shiny-server && \\\n                install -o ${NB_USER} -g ${NB_USER} -d /var/lib/shiny-server && \\\n                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/log/shiny-server.log && \\\n                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/run/shiny-server.pid\n                ')]
            if 'r' in self.stencila_contexts:
                if V(self.r_version) <= V('3.5'):
                    scripts += [
                     ('${NB_USER}', '\n                    R --quiet -e "source(\'https://bioconductor.org/biocLite.R\'); biocLite(\'graph\')" && \\\n                    R --quiet -e "devtools::install_github(\'stencila/r\', ref = \'361bbf560f3f0561a8612349bca66cd8978f4f24\')" && \\\n                    R --quiet -e "stencila::register()"\n                    ')]
                else:
                    scripts += [
                     ('${NB_USER}', '\n                    R --quiet -e "install.packages(\'BiocManager\'); BiocManager::install(); BiocManager::install(c(\'graph\'))" && \\\n                    R --quiet -e "devtools::install_github(\'stencila/r\', ref = \'361bbf560f3f0561a8612349bca66cd8978f4f24\')" && \\\n                    R --quiet -e "stencila::register()"\n                    ')]
        return super().get_build_scripts() + scripts

    def get_preassemble_script_files(self):
        files = super().get_preassemble_script_files()
        installR_path = self.binder_path('install.R')
        if os.path.exists(installR_path):
            files[installR_path] = installR_path
        return files

    def get_preassemble_scripts(self):
        scripts = []
        installR_path = self.binder_path('install.R')
        if os.path.exists(installR_path):
            scripts += [
             (
              '${NB_USER}',
              'Rscript %s && touch /tmp/.preassembled || true' % installR_path)]
        return super().get_preassemble_scripts() + scripts

    def get_assemble_scripts(self):
        assemble_scripts = super().get_assemble_scripts()
        installR_path = self.binder_path('install.R')
        if os.path.exists(installR_path):
            assemble_scripts += [
             (
              '${NB_USER}',
              'if [ ! -f /tmp/.preassembled ]; then Rscript {}; fi'.format(installR_path))]
        description_R = 'DESCRIPTION'
        if not self.binder_dir:
            if os.path.exists(description_R):
                assemble_scripts += [
                 ('${NB_USER}', 'R --quiet -e "devtools::install_local(getwd())"')]
        return assemble_scripts