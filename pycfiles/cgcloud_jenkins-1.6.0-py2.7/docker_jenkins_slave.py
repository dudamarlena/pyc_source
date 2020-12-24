# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/docker_jenkins_slave.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.ubuntu_box import Python27UpdateUbuntuBox
from cgcloud.jenkins.generic_jenkins_slaves import UbuntuTrustyGenericJenkinsSlave
from cgcloud.core.docker_box import DockerBox

class DockerJenkinsSlave(UbuntuTrustyGenericJenkinsSlave, DockerBox, Python27UpdateUbuntuBox):
    """
    A box for running the cgl-docker-lib builds on. Probably a bit of a misnomer but so far the
    only cgl-docker-lib particular is the dependency on make.
    """

    def _list_packages_to_install(self):
        return super(DockerJenkinsSlave, self)._list_packages_to_install() + ['make']

    def _docker_users(self):
        return super(DockerJenkinsSlave, self)._docker_users() + ['jenkins']

    @classmethod
    def recommended_instance_type(cls):
        return 'm3.large'