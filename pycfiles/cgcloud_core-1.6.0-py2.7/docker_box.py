# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/docker_box.py
# Compiled at: 2016-11-22 15:21:45
import logging
from pipes import quote
from fabric.operations import run
from bd2k.util.strings import interpolate as fmt
from cgcloud.core.box import fabric_task
from cgcloud.core.ubuntu_box import UbuntuBox
from cgcloud.fabric.operations import sudo
from cgcloud.lib.util import heredoc
log = logging.getLogger(__name__)

class DockerBox(UbuntuBox):
    """
    A mixin for Docker. Based on the official shell script from

    https://docs.docker.com/installation/ubuntulinux/#installation
    """

    @fabric_task
    def _setup_package_repos(self):
        assert run('test -e /usr/lib/apt/methods/https', warn_only=True).succeeded, 'Need HTTPS support in apt-get in order to install from the Docker repository'
        super(DockerBox, self)._setup_package_repos()
        sudo((' ').join(['apt-key', 'adv',
         '--keyserver', 'hkp://p80.pool.sks-keyservers.net:80',
         '--recv-keys', '58118E89F3A912897C070ADBF76221572C52609D']))
        codename = self.release().codename
        sudo(fmt('echo deb https://apt.dockerproject.org/repo ubuntu-{codename} main > /etc/apt/sources.list.d/docker.list'))

    @fabric_task
    def _list_packages_to_install(self):
        kernel = run('uname -r')
        kernel_version = tuple(map(int, kernel.split('.')[:2]))
        assert kernel_version >= (3, 10), "Need at least kernel version 3.10, found '%s'." % kernel
        kernel = run('uname -r')
        assert kernel.endswith('-generic'), 'Current kernel is not supported by the linux-image-extra-virtual package.'
        packages = super(DockerBox, self)._list_packages_to_install()
        packages += ['docker-engine=1.9.1-0~trusty', 'linux-image-extra-' + kernel, 'linux-image-extra-virtual']
        if run('cat /sys/module/apparmor/parameters/enabled').lower().startswith('y'):
            packages += ['apparmor']
        return packages

    def _post_install_packages(self):
        super(DockerBox, self)._post_install_packages()
        self._setup_docker()

    def _docker_users(self):
        return [
         self.admin_account()]

    def _docker_data_prefixes(self):
        return [
         self._ephemeral_mount_point(0)]

    @fabric_task
    def _setup_docker(self):
        for docker_user in set(self._docker_users()):
            sudo('usermod -aG docker ' + docker_user)

        prefixes = self._docker_data_prefixes()
        if prefixes:
            prefixes = (' ').join(map(quote, prefixes))
            self._run_init_script('docker', 'stop')
            sudo('umount /var/lib/docker/aufs', warn_only=True)
            sudo('tar -czC /var/lib docker > /var/lib/docker.tar.gz')
            sudo('rm -rf /var/lib/docker && mkdir /var/lib/docker')
            self._register_init_script('dockerbox', heredoc('\n                    description "Placement of /var/lib/docker"\n                    console log\n                    start on starting docker\n                    stop on stopped docker\n                    pre-start script\n                        echo\n                        echo "This is the dockerbox pre-start script"\n                        set -ex\n                        if mountpoint -q /var/lib/docker; then\n                            echo "The directory \'/var/lib/docker\' is already mounted, exiting."\n                        else\n                            for prefix in {prefixes}; do\n                                # Prefix must refer to a separate volume, e.g. ephemeral or EBS\n                                if mountpoint -q "$prefix"; then\n                                    # Make sure Docker\'s aufs backend isn\'t mounted anymore\n                                    umount /var/lib/docker/aufs || true\n                                    if test -d "$prefix/var/lib/docker"; then\n                                        echo "The directory \'$prefix/var/lib/docker\' already exists, using it."\n                                    else\n                                        mkdir -p "$prefix/var/lib"\n                                        # If /var/lib/docker contains files ...\n                                        if python -c \'import os, sys; sys.exit( 0 if os.listdir( sys.argv[1] ) else 1 )\' /var/lib/docker; then\n                                            # ... move it to prefix ...\n                                            mv /var/lib/docker "$prefix/var/lib"\n                                            # ... and recreate it as an empty mount point, ...\n                                            mkdir -p /var/lib/docker\n                                        else\n                                            # ... otherwise untar the initial backup.\n                                            tar -xzC "$prefix/var/lib" < /var/lib/docker.tar.gz\n                                        fi\n                                    fi\n                                    # Now bind-mount into /var/lib/docker\n                                    mount --bind "$prefix/var/lib/docker" /var/lib/docker\n                                    break\n                                else\n                                    echo "The prefix directory \'$prefix\' is not a mount point, skipping."\n                                fi\n                            done\n                        fi\n                    end script'))
            self._run_init_script('docker', 'start')