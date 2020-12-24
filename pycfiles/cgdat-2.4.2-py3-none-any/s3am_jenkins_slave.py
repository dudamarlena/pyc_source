# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/s3am_jenkins_slave.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.ubuntu_box import Python27UpdateUbuntuBox
from cgcloud.jenkins.generic_jenkins_slaves import UbuntuTrustyGenericJenkinsSlave
from cgcloud.core.box import fabric_task
from cgcloud.core.common_iam_policies import s3_full_policy
from cgcloud.fabric.operations import remote_sudo_popen
from cgcloud.lib.util import abreviated_snake_case_class_name, heredoc

class S3amJenkinsSlave(UbuntuTrustyGenericJenkinsSlave, Python27UpdateUbuntuBox):
    """
    Jenkins slave for running the S3AM build
    """

    @classmethod
    def recommended_instance_type(cls):
        return 'm4.xlarge'

    def _list_packages_to_install(self):
        return super(S3amJenkinsSlave, self)._list_packages_to_install() + [
         'python-dev',
         'gcc', 'make', 'libcurl4-openssl-dev']

    def _post_install_packages(self):
        super(S3amJenkinsSlave, self)._post_install_packages()
        self.__patch_asynchat()

    def _get_iam_ec2_role(self):
        iam_role_name, policies = super(S3amJenkinsSlave, self)._get_iam_ec2_role()
        iam_role_name += '--' + abreviated_snake_case_class_name(S3amJenkinsSlave)
        policies.update(dict(s3_full=s3_full_policy))
        return (
         iam_role_name, policies)

    @fabric_task
    def __patch_asynchat(self):
        """
        This bites us in pyftpdlib during S3AM unit tests:

        http://jenkins.cgcloud.info/job/s3am/13/testReport/junit/src.s3am.test.s3am_tests/CoreTests/test_copy/

        The patch is from

        https://hg.python.org/cpython/rev/d422062d7d36
        http://bugs.python.org/issue16133
        Fixed in 2.7.9: https://hg.python.org/cpython/raw-file/v2.7.9/Misc/NEWS
        """
        if self._remote_python_version() < (2, 7, 9):
            with remote_sudo_popen('patch -d /usr/lib/python2.7 -p2') as (patch):
                patch.write(heredoc('\n                    diff --git a/Lib/asynchat.py b/Lib/asynchat.py\n                    --- a/Lib/asynchat.py\n                    +++ b/Lib/asynchat.py\n                    @@ -46,12 +46,17 @@ method) up to the terminator, and then c\n                     you - by calling your self.found_terminator() method.\n                     """\n\n                    +import asyncore\n                    +import errno\n                     import socket\n                    -import asyncore\n                     from collections import deque\n                     from sys import py3kwarning\n                     from warnings import filterwarnings, catch_warnings\n\n                    +_BLOCKING_IO_ERRORS = (errno.EAGAIN, errno.EALREADY, errno.EINPROGRESS,\n                    +                       errno.EWOULDBLOCK)\n                    +\n                    +\n                     class async_chat (asyncore.dispatcher):\n                         """This is an abstract class.  You must derive from this class, and add\n                         the two methods collect_incoming_data() and found_terminator()"""\n                    @@ -109,6 +114,8 @@ class async_chat (asyncore.dispatcher):\n                             try:\n                                 data = self.recv (self.ac_in_buffer_size)\n                             except socket.error, why:\n                    +            if why.args[0] in _BLOCKING_IO_ERRORS:\n                    +                return\n                                 self.handle_error()\n                                 return'))