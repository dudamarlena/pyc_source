# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/toil/toil_box.py
# Compiled at: 2016-11-22 15:21:45
import logging, os, re
from abc import abstractmethod
from bd2k.util import strict_bool
from bd2k.util.iterables import concat
from fabric.operations import put
from cgcloud.core.box import fabric_task
from cgcloud.core.cluster import ClusterBox, ClusterWorker, ClusterLeader
from cgcloud.core.common_iam_policies import ec2_full_policy, s3_full_policy, sdb_full_policy
from cgcloud.core.docker_box import DockerBox
from cgcloud.core.version import s3am_dep
from cgcloud.fabric.operations import pip, remote_sudo_popen, sudo, virtualenv
from cgcloud.lib.util import abreviated_snake_case_class_name, heredoc, UserError
from cgcloud.mesos.mesos_box import MesosBoxSupport, user, persistent_dir
log = logging.getLogger(__name__)

class ToilBoxSupport(MesosBoxSupport, DockerBox, ClusterBox):
    """
    A box with Mesos, Toil and their dependencies installed.
    """

    def _list_packages_to_install(self):
        return super(ToilBoxSupport, self)._list_packages_to_install() + [
         'python-dev', 'gcc', 'make',
         'libcurl4-openssl-dev',
         'libffi-dev']

    def _post_install_mesos(self):
        super(ToilBoxSupport, self)._post_install_mesos()
        self.__install_toil()
        self.__install_s3am()

    def _docker_users(self):
        return super(ToilBoxSupport, self)._docker_users() + [user]

    def _docker_data_prefixes(self):
        return concat(persistent_dir, super(ToilBoxSupport, self)._docker_data_prefixes())

    @fabric_task
    def _setup_docker(self):
        super(ToilBoxSupport, self)._setup_docker()
        with remote_sudo_popen('patch -d /etc/init') as (patch):
            patch.write(heredoc('\n                --- docker.conf.orig\t2015-12-18 23:28:48.693072560 +0000\n                +++ docker.conf\t2015-12-18 23:40:30.553072560 +0000\n                @@ -1,6 +1,6 @@\n                 description "Docker daemon"\n\n                -start on (local-filesystems and net-device-up IFACE!=lo)\n                +start on (local-filesystems and net-device-up IFACE!=lo and started mesosbox)\n                 stop on runlevel [!2345]\n                 limit nofile 524288 1048576\n                 limit nproc 524288 1048576'))

    def _enable_agent_metrics(self):
        return True

    @classmethod
    def get_role_options(cls):
        return super(ToilBoxSupport, cls).get_role_options() + [
         cls.RoleOption(name='persist_var_lib_toil', type=strict_bool, repr=repr, inherited=True, help='True if /var/lib/toil should be persistent.')]

    def _get_iam_ec2_role(self):
        iam_role_name, policies = super(ToilBoxSupport, self)._get_iam_ec2_role()
        iam_role_name += '--' + abreviated_snake_case_class_name(ToilBoxSupport)
        policies.update(dict(toil_iam_pass_role=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource=self._role_arn(), Action='iam:PassRole')]), ec2_full=ec2_full_policy, s3_full=s3_full_policy, sbd_full=sdb_full_policy, ec2_toil_box=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource='*', Action='ec2:CreateTags'),
         dict(Effect='Allow', Resource='*', Action='ec2:CreateVolume'),
         dict(Effect='Allow', Resource='*', Action='ec2:AttachVolume')])))
        return (iam_role_name, policies)

    @abstractmethod
    def _toil_pip_args(self):
        raise NotImplementedError()

    @fabric_task
    def __install_toil(self):
        pip('install --upgrade pip', use_sudo=True)
        pip(concat('install', self._toil_pip_args()), use_sudo=True)
        self._lazy_mkdir('/var/lib', 'toil', persistent=None)
        sudo('echo "TOIL_WORKDIR=/var/lib/toil" >> /etc/environment')
        return

    @fabric_task
    def __install_s3am(self):
        virtualenv(name='s3am', distributions=[
         s3am_dep], pip_distribution='pip==8.0.2', executable='s3am')


class ToilLegacyBox(ToilBoxSupport):
    """
    A box with Mesos, Toil 3.1.6 and their dependencies installed.
    """

    def _toil_pip_args(self):
        return [
         'toil[aws,mesos,encryption]==3.1.6']


class ToilBox(ToilBoxSupport):
    """
    A box with Mesos, the latest stable Toil release and their dependencies installed.
    """
    default_spec = 'toil[aws,mesos,encryption,cwl]==3.3.3'

    @classmethod
    def get_role_options(cls):
        return super(ToilBox, cls).get_role_options() + [
         cls.RoleOption(name='toil_sdists', type=cls.parse_sdists, repr=cls.unparse_sdists, inherited=False, help="A space-separated list of paths to sdists. If this option is present, pip will be used to install the specified sdists instead of %s. Each path may be immediately followed by a list of extras enclosed in square brackets. The Toil sdist should come last. An sdist is a .tar.gz file containing the source distribution of a Python project. It is typically created by running 'python setup.py sdist' from the project root, or, in the case of Toil and CGCloud, running 'make sdist'. Example: '%s'. " % (
          cls.default_spec,
          cls.unparse_sdists([
           ('../cgcloud-lib-1.4a1.dev0.tar.gz', ''),
           ('dist/toil-3.2.0a2.tar.gz', '[aws,mesos,cgcloud]')])))]

    sdist_re = re.compile('([^\\[\\]]+)((?:\\[[^\\]]+\\])?)$')

    @classmethod
    def parse_sdists(cls, s):
        try:
            return [ cls.sdist_re.match(sdist).groups() for sdist in s.split() ]
        except:
            raise UserError("'%s' is not a valid value for the toil_sdists option." % s)

    @classmethod
    def unparse_sdists(cls, sdists):
        return (' ').join(path + extra for path, extra in sdists)

    @fabric_task
    def _toil_pip_args(self):
        sdists = self.role_options.get('toil_sdists')
        if sdists:
            result = []
            for path, extra in sdists:
                put(local_path=path)
                result.append(os.path.basename(path) + extra)

            return result
        return ['--pre', self.default_spec]


class ToilLatestBox(ToilBox):
    """
    A box with Mesos, the latest unstable release of Toil and their dependencies installed
    """
    default_spec = 'toil[aws,mesos,encryption,cwl]<=3.5.0'


class ToilLeader(ToilBox, ClusterLeader):
    """
    Leader of a cluster of boxes booted from a toil-box, toil-latest-box or toil-legacy-box image
    """
    pass


class ToilWorker(ToilBox, ClusterWorker):
    """
    Worker in a cluster of boxes booted from a toil-box, toil-latest-box or toil-legacy-box image
    """
    pass