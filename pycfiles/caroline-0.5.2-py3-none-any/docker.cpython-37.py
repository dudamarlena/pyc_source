# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/a1fred/Devel/carnival/carnival-contrib/carnival_contrib/docker.py
# Compiled at: 2020-02-29 15:09:44
# Size of source mod 2**32: 1535 bytes
from carnival import Step
from carnival import cmd
from carnival.utils import log

class CeInstallUbuntu(Step):

    def run(self, docker_version=None):
        """
        Returns true if installed, false if was already installed
        """
        from carnival.cmd import apt
        pkgname = 'docker-ce'
        if apt.is_pkg_installed(pkgname, docker_version):
            log(f"{pkgname} already installed")
            return False
        log(f"Installing {pkgname}...")
        cmd.cli.run('sudo apt-get update')
        cmd.cli.run('sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common')
        cmd.cli.run('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -', pty=True)
        cmd.cli.run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
        apt.force_install(pkgname=pkgname, version=docker_version, update=True, hide=True)
        return True


class ComposeInstall(Step):

    def run(self, docker_compose_version='1.25.1', docker_compose_dest='/usr/local/bin/docker-compose'):
        log('Installing compose...')
        download_link = f"https://github.com/docker/compose/releases/download/{docker_compose_version}/docker-compose-`uname -s`-`uname -m`"
        cmd.cli.run(f"sudo curl -sL {download_link} -o {docker_compose_dest}")
        cmd.cli.run(f"sudo chmod a+x {docker_compose_dest}")