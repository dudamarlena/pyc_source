# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/spark/spark_box.py
# Compiled at: 2016-11-22 15:21:45
import logging
from StringIO import StringIO
from collections import namedtuple
from bd2k.util.iterables import concat
from bd2k.util.strings import interpolate as fmt
from fabric.context_managers import settings
from fabric.operations import run, put
from cgcloud.core.apache import ApacheSoftwareBox
from cgcloud.core.box import fabric_task
from cgcloud.core.cluster import ClusterBox, ClusterLeader, ClusterWorker
from cgcloud.core.common_iam_policies import ec2_read_only_policy
from cgcloud.core.generic_boxes import GenericUbuntuTrustyBox
from cgcloud.core.ubuntu_box import Python27UpdateUbuntuBox
from cgcloud.fabric.operations import sudo, remote_open, pip, sudov
from cgcloud.lib.util import abreviated_snake_case_class_name, heredoc
log = logging.getLogger(__name__)
user = 'sparkbox'
install_dir = '/opt/sparkbox'
log_dir = '/var/log/sparkbox'
ephemeral_dir = '/mnt/ephemeral'
persistent_dir = '/mnt/persistent'
var_dir = '/var/lib/sparkbox'
hdfs_replication = 1
hadoop_version = '2.6.0'
spark_version = '1.6.2'
spark_hadoop_version = '2.6'
Service = namedtuple('Service', [
 'init_name',
 'description',
 'start_script',
 'stop_script'])

def hdfs_service(name):
    script = '{install_dir}/hadoop/sbin/hadoop-daemon.sh {action} {name}'
    return Service(init_name='hdfs-' + name, description=fmt('Hadoop DFS {name} service'), start_script=fmt(script, action='start'), stop_script=fmt(script, action='stop'))


def spark_service(name, script_suffix=None):
    if script_suffix is None:
        script_suffix = name
    script = '{install_dir}/spark/sbin/{action}-{script_suffix}.sh'
    return Service(init_name='spark-' + name, description=fmt('Spark {name} service'), start_script=fmt(script, action='start'), stop_script=fmt(script, action='stop'))


hadoop_services = dict(master=[
 hdfs_service('namenode'), hdfs_service('secondarynamenode')], slave=[
 hdfs_service('datanode')])
spark_services = dict(master=[
 spark_service('master')], slave=[
 spark_service('slave', 'slaves')])

class SparkBox(ApacheSoftwareBox, ClusterBox, GenericUbuntuTrustyBox, Python27UpdateUbuntuBox):
    """
    A node in a Spark cluster; used only to create an image for master and worker boxes

    Workers and the master undergo the same setup. Whether a node acts as a master or a slave is
    determined at boot time, via user data. All slave nodes will be passed the IP of the master
    node. This implies that the master is started first. As soon as its private IP is assigned,
    typically seconds after the reservation has been submitted, the slaves can be started up.
    """

    @classmethod
    def get_role_options(cls):
        return super(SparkBox, cls).get_role_options() + [
         cls.RoleOption(name='etc_hosts_entries', type=str, repr=str, inherited=True, help="Additional entries for /etc/hosts in the form 'foo:1.2.3.4,bar:2.3.4.5'")]

    def other_accounts(self):
        return super(SparkBox, self).other_accounts() + [user]

    def default_account(self):
        return user

    def __init__(self, ctx):
        super(SparkBox, self).__init__(ctx)
        self.lazy_dirs = set()

    def _populate_security_group(self, group_id):
        return super(SparkBox, self)._populate_security_group(group_id) + [
         dict(ip_protocol='tcp', from_port=0, to_port=65535, src_security_group_group_id=group_id),
         dict(ip_protocol='udp', from_port=0, to_port=65535, src_security_group_group_id=group_id)]

    def _get_iam_ec2_role(self):
        iam_role_name, policies = super(SparkBox, self)._get_iam_ec2_role()
        iam_role_name += '--' + abreviated_snake_case_class_name(SparkBox)
        policies.update(dict(ec2_read_only=ec2_read_only_policy, ec2_spark_box=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource='*', Action='ec2:CreateTags'),
         dict(Effect='Allow', Resource='*', Action='ec2:CreateVolume'),
         dict(Effect='Allow', Resource='*', Action='ec2:AttachVolume')])))
        return (
         iam_role_name, policies)

    @fabric_task
    def _setup_package_repos(self):
        super(SparkBox, self)._setup_package_repos()
        sudo('add-apt-repository -y ppa:webupd8team/java')

    def _list_packages_to_install(self):
        return super(SparkBox, self)._list_packages_to_install() + [
         'oracle-java8-set-default']

    def _get_debconf_selections(self):
        return super(SparkBox, self)._get_debconf_selections() + [
         'debconf shared/accepted-oracle-license-v1-1 select true',
         'debconf shared/accepted-oracle-license-v1-1 seen true']

    def _pre_install_packages(self):
        super(SparkBox, self)._pre_install_packages()
        self.__setup_application_user()

    @fabric_task
    def __setup_application_user(self):
        sudo(fmt('useradd --home /home/{user} --create-home --user-group --shell /bin/bash {user}'))

    def _post_install_packages(self):
        super(SparkBox, self)._post_install_packages()
        self._propagate_authorized_keys(user, user)
        self.__setup_shared_dir()
        self.__setup_ssh_config()
        self.__create_spark_keypair()
        self.__install_hadoop()
        self.__install_spark()
        self.__setup_path()
        self.__install_tools()

    def _shared_dir(self):
        return '/home/%s/shared' % self.default_account()

    @fabric_task
    def __setup_shared_dir(self):
        sudov('install', '-d', self._shared_dir(), '-m', '700', '-o', self.default_account())

    @fabric_task
    def __setup_ssh_config(self):
        with remote_open('/etc/ssh/ssh_config', use_sudo=True) as (f):
            f.write(heredoc('\n                Host spark-master\n                    CheckHostIP no\n                    HashKnownHosts no'))

    @fabric_task(user=user)
    def __create_spark_keypair(self):
        self._provide_imported_keypair(ec2_keypair_name=self.__ec2_keypair_name(self.ctx), private_key_path=fmt('/home/{user}/.ssh/id_rsa'), overwrite_ec2=True)
        run('cd .ssh && cat id_rsa.pub >> authorized_keys2')

    def __ec2_keypair_name(self, ctx):
        return user + '@' + ctx.to_aws_name(self.role())

    @fabric_task
    def __install_hadoop(self):
        path = fmt('hadoop/common/hadoop-{hadoop_version}/hadoop-{hadoop_version}.tar.gz')
        self._install_apache_package(path, install_dir)
        hadoop_env = dict(HADOOP_LOG_DIR=self._lazy_mkdir(log_dir, 'hadoop'), JAVA_HOME='/usr/lib/jvm/java-8-oracle')
        hadoop_env_sh_path = fmt('{install_dir}/hadoop/etc/hadoop/hadoop-env.sh')
        with remote_open(hadoop_env_sh_path, use_sudo=True) as (hadoop_env_sh):
            hadoop_env_sh.write('\n')
            for name, value in hadoop_env.iteritems():
                hadoop_env_sh.write(fmt('export {name}="{value}"\n'))

        hdfs_dir = var_dir + '/hdfs'
        put(use_sudo=True, remote_path=fmt('{install_dir}/hadoop/etc/hadoop/hdfs-site.xml'), local_path=StringIO(self.__to_hadoop_xml_config({'dfs.replication': str(hdfs_replication), 
           'dfs.permissions': 'false', 
           'dfs.name.dir': self._lazy_mkdir(hdfs_dir, 'name', persistent=True), 
           'dfs.data.dir': self._lazy_mkdir(hdfs_dir, 'data', persistent=True), 
           'fs.checkpoint.dir': self._lazy_mkdir(hdfs_dir, 'checkpoint', persistent=True), 
           'dfs.namenode.http-address': 'spark-master:50070', 
           'dfs.namenode.secondary.http-address': 'spark-master:50090'})))
        put(use_sudo=True, remote_path=fmt('{install_dir}/hadoop/etc/hadoop/core-site.xml'), local_path=StringIO(self.__to_hadoop_xml_config({'fs.default.name': 'hdfs://spark-master:8020'})))
        sudo(fmt('find {install_dir}/hadoop -name "*.cmd" | xargs rm'))
        self.__register_upstart_jobs(hadoop_services)

    @staticmethod
    def __to_hadoop_xml_config(properties):
        """
        >>> print SparkBox._SparkBox__to_hadoop_xml_config( {'foo' : 'bar'} )
        <?xml version='1.0' encoding='utf-8'?>
        <?xml-stylesheet type='text/xsl' href='configuration.xsl'?>
        <configuration>
            <property>
                <name>foo</name>
                <value>bar</value>
            </property>
        </configuration>
        <BLANKLINE>
        """
        s = StringIO()
        s.write(heredoc("\n            <?xml version='1.0' encoding='utf-8'?>\n            <?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n            <configuration>"))
        for name, value in properties.iteritems():
            s.write(heredoc('\n                <property>\n                    <name>{name}</name>\n                    <value>{value}</value>\n                </property>', indent='    '))

        s.write('</configuration>\n')
        return s.getvalue()

    @fabric_task
    def __install_spark(self):
        path = fmt('spark/spark-{spark_version}/spark-{spark_version}-bin-hadoop{spark_hadoop_version}.tgz')
        self._install_apache_package(path, install_dir)
        spark_dir = var_dir + '/spark'
        spark_env_sh_path = fmt('{install_dir}/spark/conf/spark-env.sh')
        sudo(fmt('cp {spark_env_sh_path}.template {spark_env_sh_path}'))
        spark_env = dict(SPARK_LOG_DIR=self._lazy_mkdir(log_dir, 'spark'), SPARK_WORKER_DIR=self._lazy_mkdir(spark_dir, 'work'), SPARK_LOCAL_DIRS=self._lazy_mkdir(spark_dir, 'local'), JAVA_HOME='/usr/lib/jvm/java-8-oracle', SPARK_MASTER_IP='spark-master', HADOOP_CONF_DIR=fmt('{install_dir}/hadoop/etc/hadoop'))
        with remote_open(spark_env_sh_path, use_sudo=True) as (spark_env_sh):
            spark_env_sh.write('\n')
            for name, value in spark_env.iteritems():
                spark_env_sh.write(fmt('export {name}="{value}"\n'))

        spark_defaults = {'spark.eventLog.enabled': 'true', 
           'spark.eventLog.dir': self._lazy_mkdir(spark_dir, 'history'), 
           'spark.master': 'spark://spark-master:7077'}
        spark_defaults_conf_path = fmt('{install_dir}/spark/conf/spark-defaults.conf')
        sudo(fmt('cp {spark_defaults_conf_path}.template {spark_defaults_conf_path}'))
        with remote_open(spark_defaults_conf_path, use_sudo=True) as (spark_defaults_conf):
            for name, value in spark_defaults.iteritems():
                spark_defaults_conf.write(fmt('{name}\t{value}\n'))

        sudo(fmt('find {install_dir}/spark -name "*.cmd" | xargs rm'))
        self.__register_upstart_jobs(spark_services)

    @fabric_task
    def __install_tools(self):
        """
        Installs the spark-master-discovery init script and its companion spark-tools. The latter
        is a Python package distribution that's included in cgcloud-spark as a resource. This is
        in contrast to the cgcloud agent, which is a standalone distribution.
        """
        tools_dir = install_dir + '/tools'
        admin = self.admin_account()
        sudo(fmt('mkdir -p {tools_dir}'))
        sudo(fmt('chown {admin}:{admin} {tools_dir}'))
        run(fmt('virtualenv --no-pip {tools_dir}'))
        run(fmt('{tools_dir}/bin/easy_install pip==1.5.2'))
        with settings(forward_agent=True):
            with self._project_artifacts('spark-tools') as (artifacts):
                pip(use_sudo=True, path=tools_dir + '/bin/pip', args=concat('install', artifacts))
        sudo(fmt('chown -R root:root {tools_dir}'))
        spark_tools = 'SparkTools(**%r)' % dict(user=user, shared_dir=self._shared_dir(), install_dir=install_dir, ephemeral_dir=ephemeral_dir, persistent_dir=persistent_dir, lazy_dirs=self.lazy_dirs)
        self.lazy_dirs = None
        self._register_init_script('sparkbox', heredoc('\n                description "Spark/HDFS master discovery"\n                console log\n                start on (local-filesystems and net-device-up IFACE!=lo)\n                stop on runlevel [!2345]\n                pre-start script\n                for i in 1 2 3; do if {tools_dir}/bin/python2.7 - <<END\n                import logging\n                logging.basicConfig( level=logging.INFO )\n                from cgcloud.spark_tools import SparkTools\n                spark_tools = {spark_tools}\n                spark_tools.start()\n                END\n                then exit 0; fi; echo Retrying in 60s; sleep 60; done; exit 1\n                end script\n                post-stop script\n                {tools_dir}/bin/python2.7 - <<END\n                import logging\n                logging.basicConfig( level=logging.INFO )\n                from cgcloud.spark_tools import SparkTools\n                spark_tools = {spark_tools}\n                spark_tools.stop()\n                END\n                end script'))
        script_path = '/usr/local/bin/sparkbox-manage-slaves'
        put(remote_path=script_path, use_sudo=True, local_path=StringIO(heredoc('\n            #!{tools_dir}/bin/python2.7\n            import sys\n            import logging\n            # Prefix each log line to make it more obvious that it\'s the master logging when the\n            # slave calls this script via ssh.\n            logging.basicConfig( level=logging.INFO,\n                                 format="manage_slaves: " + logging.BASIC_FORMAT )\n            from cgcloud.spark_tools import SparkTools\n            spark_tools = {spark_tools}\n            spark_tools.manage_slaves( slaves_to_add=sys.argv[1:] )')))
        sudo(fmt('chown root:root {script_path} && chmod 755 {script_path}'))
        return

    @fabric_task
    def _lazy_mkdir(self, parent, name, persistent=False):
        """
        __lazy_mkdir( '/foo', 'dir', True ) creates /foo/dir now and ensures that
        /mnt/persistent/foo/dir is created and bind-mounted into /foo/dir when the box starts.
        Likewise, __lazy_mkdir( '/foo', 'dir', False) creates /foo/dir now and ensures that
        /mnt/ephemeral/foo/dir is created and bind-mounted into /foo/dir when the box starts.

        Note that at start-up time, /mnt/persistent may be reassigned  to /mnt/ephemeral if no
        EBS volume is mounted at /mnt/persistent.

        _lazy_mkdir( '/foo', 'dir', None ) will look up an instance tag named 'persist_foo_dir'
        when the box starts and then behave like _lazy_mkdir( '/foo', 'dir', True ) if that tag's
        value is 'True', or _lazy_mkdir( '/foo', 'dir', False ) if that tag's value is False.
        """
        assert self.lazy_dirs is not None
        assert '/' not in name
        assert parent.startswith('/')
        for location in (persistent_dir, ephemeral_dir):
            assert location.startswith('/')
            assert not location.startswith(parent) and not parent.startswith(location)

        logical_path = parent + '/' + name
        sudo('mkdir -p "%s"' % logical_path)
        self.lazy_dirs.add((parent, name, persistent))
        return logical_path

    def __register_upstart_jobs(self, service_map):
        for node_type, services in service_map.iteritems():
            start_on = 'sparkbox-start-' + node_type
            for service in services:
                self._register_init_script(service.init_name, heredoc('\n                        description "{service.description}"\n                        console log\n                        start on {start_on}\n                        stop on runlevel [016]\n                        setuid {user}\n                        setgid {user}\n                        env USER={user}\n                        pre-start exec {service.start_script}\n                        post-stop exec {service.stop_script}'))
                start_on = 'started ' + service.init_name

    @fabric_task
    def __setup_path(self):
        globally = True
        if globally:
            with remote_open('/etc/environment', use_sudo=True) as (f):
                new_path = [ fmt('{install_dir}/{package}/bin') for package in ('spark',
                                                                                'hadoop') ]
                self._patch_etc_environment(f, dirs=new_path)
        else:
            for _user in (user, self.admin_account()):
                with settings(user=_user):
                    with remote_open('~/.profile') as (f):
                        f.write('\n')
                        for package in ('spark', 'hadoop'):
                            f.write(fmt('PATH="$PATH:{install_dir}/{package}/bin"\n'))


class SparkMaster(SparkBox, ClusterLeader):
    """
    The master of a cluster of boxes created from a spark-box image
    """


class SparkSlave(SparkBox, ClusterWorker):
    """
    A slave in a cluster of boxes created from a spark-box image
    """