# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mount/SDC/crowdai/repo2docker/repo2docker/buildpacks/r.py
# Compiled at: 2018-06-09 10:26:45
# Size of source mod 2**32: 9520 bytes
import re, os, datetime
from .python import PythonBuildPack

class RBuildPack(PythonBuildPack):
    """RBuildPack"""

    @property
    def runtime(self):
        """
        Return contents of runtime.txt if it exists, '' otherwise
        """
        if not hasattr(self, '_runtime'):
            runtime_path = self.binder_path('runtime.txt')
            try:
                with open(runtime_path) as (f):
                    self._runtime = f.read().strip()
            except FileNotFoundError:
                self._runtime = ''

        return self._runtime

    @property
    def checkpoint_date(self):
        """
        Return the date of MRAN checkpoint to use for this repo

        Returns '' if no date is specified
        """
        if not hasattr(self, '_checkpoint_date'):
            match = re.match('r-(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)', self.runtime)
            if not match:
                self._checkpoint_date = False
            else:
                self._checkpoint_date = (datetime.date)(*[int(s) for s in match.groups()])
        return self._checkpoint_date

    def detect(self):
        """
        Check if current repo should be built with the R Build pack

        super().detect() is not called in this function - it would return false
        unless a `requirements.txt` is present and we do not want to require the
        presence of a `requirements.txt` to use R.

        Instead we just check if runtime.txt contains a string of the form
        `r-<YYYY>-<MM>-<DD>`
        """
        return bool(self.checkpoint_date)

    def get_path(self):
        return super().get_path() + [
         '/usr/lib/rstudio-server/bin/']

    def get_env(self):
        return super().get_env() + [
         ('R_LIBS_USER', '${APP_BASE}/rlibs')]

    def get_packages(self):
        return super().get_packages().union([
         'r-base',
         'psmisc',
         'libapparmor1',
         'sudo',
         'lsb-release'])

    def get_build_scripts(self):
        rstudio_url = 'https://download2.rstudio.org/rstudio-server-1.1.419-amd64.deb'
        rstudio_checksum = '24cd11f0405d8372b4168fc9956e0386'
        shiny_url = 'https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.7.907-amd64.deb'
        shiny_checksum = '78371a8361ba0e7fec44edd2b8e425ac'
        devtools_version = '2018-02-01'
        irkernel_version = '0.8.11'
        return super().get_build_scripts() + [
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
         ('${NB_USER}', '\n                pip install --no-cache-dir nbrsessionproxy==0.7.0 && \\\n                jupyter serverextension enable nbrsessionproxy --sys-prefix && \\\n                jupyter nbextension install --py nbrsessionproxy --sys-prefix && \\\n                jupyter nbextension enable --py nbrsessionproxy --sys-prefix\n                '),
         (
          '${NB_USER}',
          '\n                R --quiet -e "install.packages(\'devtools\', repos=\'https://mran.microsoft.com/snapshot/{devtools_version}\', method=\'libcurl\')" && \\\n                R --quiet -e "devtools::install_github(\'IRkernel/IRkernel\', ref=\'{irkernel_version}\')" && \\\n                R --quiet -e "IRkernel::installspec(prefix=\'$NB_PYTHON_PREFIX\')"\n                '.format(devtools_version=devtools_version,
            irkernel_version=irkernel_version)),
         (
          '${NB_USER}',
          '\n                R --quiet -e "install.packages(\'shiny\', repos=\'https://mran.microsoft.com/snapshot/{}\', method=\'libcurl\')"\n                '.format(self.checkpoint_date.isoformat()))]

    def get_assemble_scripts(self):
        mran_url = 'https://mran.microsoft.com/snapshot/{}'.format(self.checkpoint_date.isoformat())
        assemble_scripts = super().get_assemble_scripts() + [
         (
          'root',
          '\n                echo "options(repos = c(CRAN=\'{mran_url}\'), download.file.method = \'libcurl\')" > /etc/R/Rprofile.site\n                '.format(mran_url=mran_url)),
         ('root', '\n                install -o ${NB_USER} -g ${NB_USER} -d /var/log/shiny-server && \\\n                install -o ${NB_USER} -g ${NB_USER} -d /var/lib/shiny-server && \\\n                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/log/shiny-server.log && \\\n                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/run/shiny-server.pid\n                ')]
        installR_path = self.binder_path('install.R')
        if os.path.exists(installR_path):
            assemble_scripts += [
             (
              '${NB_USER}',
              'Rscript %s' % installR_path)]
        return assemble_scripts