# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/jenkins_slave.py
# Compiled at: 2016-11-22 15:21:45
from bd2k.util.xml.builder import E
from cgcloud.core.agent_box import AgentBox
from cgcloud.lib.util import snake_to_camel, UserError
from cgcloud.fabric.operations import sudo
from cgcloud.core.box import fabric_task
from cgcloud.core.source_control_client import SourceControlClient
from cgcloud.jenkins.jenkins_master import Jenkins, JenkinsMaster
build_dir = '/home/jenkins/builds'

class JenkinsSlave(SourceControlClient, AgentBox):
    """
    A box that represents EC2 instances which can serve as a Jenkins build agent. This class is
    typically used as a mix-in.
    """

    def other_accounts(self):
        return super(JenkinsSlave, self).other_accounts() + [Jenkins.user]

    def default_account(self):
        return Jenkins.user

    def _post_install_packages(self):
        super(JenkinsSlave, self)._post_install_packages()
        self._setup_build_user()

    def __get_master_pubkey(self):
        ec2_keypair_name = JenkinsMaster.ec2_keypair_name(self.ctx)
        ec2_keypair = self.ctx.ec2.get_key_pair(ec2_keypair_name)
        if ec2_keypair is None:
            raise UserError("Missing EC2 keypair named '%s'. You must create the master before creating slaves." % ec2_keypair_name)
        return self.ctx.download_ssh_pubkey(ec2_keypair)

    def _populate_ec2_keypair_globs(self, ec2_keypair_globs):
        super(JenkinsSlave, self)._populate_ec2_keypair_globs(ec2_keypair_globs)
        ec2_keypair_globs.append(JenkinsMaster.ec2_keypair_name(self.ctx))

    @fabric_task
    def _setup_build_user(self):
        """
        Setup a user account that accepts SSH connections from Jenkins such that it can act as a
        Jenkins slave.
        """
        kwargs = dict(user=Jenkins.user, dir=build_dir, ephemeral=self._ephemeral_mount_point(0), pubkey=self.__get_master_pubkey().strip())
        sudo(('useradd -m -s /bin/bash {0}').format(Jenkins.user))
        self._propagate_authorized_keys(Jenkins.user)
        sudo(("echo '{pubkey}' >> ~/.ssh/authorized_keys").format(**kwargs), user=Jenkins.user, sudo_args='-i')
        self.setup_repo_host_keys(user=Jenkins.user)
        if sudo(('test -d {ephemeral}').format(**kwargs), quiet=True).failed:
            sudo(('mkdir {ephemeral}').format(**kwargs))
        chown_cmd = ('mount {ephemeral} || true ; chown -R {user}:{user} {ephemeral}').format(**kwargs)
        sudo(chown_cmd)
        self._register_init_command(chown_cmd)
        sudo(('ln -snf {ephemeral} {dir}').format(**kwargs), user=Jenkins.user, sudo_args='-i')

    def __jenkins_labels(self):
        labels = self.role().split('-')
        return [ l for l in labels if l not in ('jenkins', 'slave') ]

    def slave_config_template(self, image, instance_type=None):
        """
        Returns the slave template, i.e. a fragment of Jenkins configuration that,
        if added to the master's main config file, controls how EC2 instances of this slave box
        are created and managed by the master.

        :param image: the image to boot slave instances from
        :type image: boto.ec2.image.Image

        :return: an XML element containing the slave template
        :rtype: xml.etree.ElementTree.Element
        """
        if instance_type is None:
            instance_type = self.recommended_instance_type()
        self._set_instance_options(image.tags)
        spec = dict(instance_type=instance_type)
        self._spec_block_device_mapping(spec, image)
        return E('hudson.plugins.ec2.SlaveTemplate', E.ami(image.id), E.description(self.role()), E.zone(self.ctx.availability_zone), E.securityGroups(self.ctx.to_aws_name(self._security_group_name())), E.remoteFS(build_dir), E.sshPort('22'), E.type(snake_to_camel(instance_type, separator='.')), E.labels((' ').join(self.__jenkins_labels())), E.mode('EXCLUSIVE'), E.initScript('while ! touch %s/.writable; do sleep 1; done' % build_dir), E.userData(spec.get('user_data', '')), E.numExecutors('1'), E.remoteAdmin(Jenkins.user), E.rootCommandPrefix(''), E.jvmopts(''), E.subnetId(''), E.idleTerminationMinutes('30'), E.iamInstanceProfile(self.get_instance_profile_arn()), E.useEphemeralDevices('true'), E.instanceCap('1'), E.stopOnTerminate('false'), E.tags(*[ E('hudson.plugins.ec2.EC2Tag', E.name(k), E.value(v)) for k, v in self._get_instance_options().iteritems() if v is not None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ]), E.usePrivateDnsName('false'))