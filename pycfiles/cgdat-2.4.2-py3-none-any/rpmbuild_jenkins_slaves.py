# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/rpmbuild_jenkins_slaves.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.box import fabric_task
from cgcloud.core.centos_box import CentosBox
from cgcloud.core.generic_boxes import GenericCentos5Box, GenericCentos6Box
from cgcloud.fabric.operations import sudo
from cgcloud.jenkins.jenkins_slave import JenkinsSlave

class CentosRpmbuildJenkinsSlave(CentosBox, JenkinsSlave):
    """
    Jenkins slave for building RPMs on CentOS
    """

    def _list_packages_to_install(self):
        return super(CentosRpmbuildJenkinsSlave, self)._list_packages_to_install() + [
         'rpmdevtools',
         'tk-devel',
         'tcl-devel',
         'expat-devel',
         'db4-devel',
         'gdbm-devel',
         'sqlite-devel',
         'bzip2-devel',
         'openssl-devel',
         'ncurses-devel',
         'readline-devel',
         'mock',
         'apr-devel',
         'apr-util-devel',
         'pcre-devel',
         'pam-devel']

    @fabric_task
    def _setup_build_user(self):
        super(CentosRpmbuildJenkinsSlave, self)._setup_build_user()
        sudo("echo 'Defaults:jenkins !requiretty' >> /etc/sudoers")
        sudo("echo 'jenkins ALL=(ALL) NOPASSWD: /bin/rpm' >> /etc/sudoers")
        sudo('useradd -s /sbin/nologin mockbuild')


class Centos5RpmbuildJenkinsSlave(CentosRpmbuildJenkinsSlave, GenericCentos5Box):
    """
    Jenkins slave for building RPMs on CentOS 5
    """


class Centos6RpmbuildJenkinsSlave(CentosRpmbuildJenkinsSlave, GenericCentos6Box):
    """
    Jenkins slave for building RPMs on CentOS 6
    """