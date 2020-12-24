# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/core/config.py
# Compiled at: 2012-03-02 22:17:19
from globus.provision.common.utils import gen_sha512
from globus.provision import AMI
from globus.provision.core.topology import Domain, User, Node, Topology, DeployData, EC2DeployData, GridMapEntry, GOEndpoint, FileSystem, NFSMount
from globus.provision.common.config import Config, Section, Option, OPTTYPE_INT, OPTTYPE_FLOAT, OPTTYPE_STRING, OPTTYPE_BOOLEAN, OPTTYPE_FILE
import os.path, getpass

class GPConfig(Config):
    """
    The instance configuration file.
    """
    sections = []
    general = Section('general', required=True, doc='This section is used for general options affecting Globus Provision as a whole.')
    general.options = [
     Option(name='ca-cert', getter='ca-cert', type=OPTTYPE_FILE, required=False, doc='\n            Location of CA certificate (PEM-encoded) used to generate user\n            and host certificates. If blank, Globus Provision will generate a self-signed\n            certificate from scratch.        \n            '),
     Option(name='ca-key', getter='ca-key', type=OPTTYPE_FILE, required=False, doc='\n            Location of the private key (PEM-encoded) for the certificate\n            specified in ``ca-cert``.\n            '),
     Option(name='ca-dn', getter='ca-dn', type=OPTTYPE_STRING, required=False, doc='\n            Distinguished Name of the certificates that will be signed with \n            the CA certificate specified in ``ca-cert``. \n            \n            For example, if you set this value to ``O=Foo, OU=Bar``, the certificates\n            will have subjects like ``/O=Foo/OU=Bar/CN=borja``, ``/O=Foo/OU=Bar/CN=host/foo.example.org``, etc.\n            '),
     Option(name='scratch-dir', getter='scratch-dir', type=OPTTYPE_STRING, required=False, default='/var/tmp', doc='\n            Scratch directory that Chef will use (on the provisioned machines)\n            while configuring them.\n            '),
     Option(name='deploy', getter='deploy', type=OPTTYPE_STRING, required=True, valid=[
      'ec2', 'dummy'], doc='\n            Globus Provision can support various "deployers" that are used to\n            deploy the hosts in a topology. Two deployers are currently supported:\n            \n            * ``ec2``: Hosts are deployed as Amazon EC2 instances.\n            * ``dummy``: Hosts are not actually deployed and are assigned dummy\n              hostnames and IP addresses.\n              \n            See the Globus Provision documentation for more details on the\n            available deployers.\n            ')]
    sections.append(general)
    ec2 = Section('ec2', required=False, required_if=[
     (('general', 'deploy'), 'ec2')], doc='\n                         When the EC2 deployer is selected, Globus Provision will need certain information about\n                         your EC2 account to be able to request EC2 instances on which to deploy your topology. This account\n                         information is specified in this section of the configuration file. If you are unclear on what values\n                         you need to specify here, see :ref:`chap_ec2` for more detailed instructions (including how to set up\n                         an Amazon EC2 account)')
    ec2.options = [
     Option(name='keypair', getter='ec2-keypair', type=OPTTYPE_STRING, required=True, doc='\n            The *name* of the Amazon EC2 keypair you will use to log into the VMs.\n            See :ref:`chap_ec2` for instructions on how to obtain this keypair.\n            '),
     Option(name='keyfile', getter='ec2-keyfile', type=OPTTYPE_FILE, required=True, doc='\n            The actual location of the keypair on your local filesystem.\n            See :ref:`chap_ec2` for instructions on how to obtain this keypair.\n            '),
     Option(name='username', getter='ec2-username', type=OPTTYPE_STRING, required=True, doc='\n            The username that Globus Provision will use to connect to the EC2 instances,\n            using the keypair specified in ``keypair``. If you are using one of the\n            Globus Provision AMIs, you need to set this value to ``ubuntu``.\n            '),
     Option(name='server-hostname', getter='ec2-server-hostname', type=OPTTYPE_STRING, required=False, doc="\n            The hostname of the EC2 server. If you are using Amazon AWS, leave this option\n            unspecified. If you are using an EC2-compatible system, such as OpenNebula, Nimbus,\n            Eucalyptus, etc. set this to the server running that system's EC2 interface.\n            "),
     Option(name='server-port', getter='ec2-server-port', type=OPTTYPE_INT, required=False, doc="\n            The TCP port of the EC2 server. If you are using Amazon AWS, leave this option\n            unspecified. If you are using an EC2-compatible system, such as OpenNebula, Nimbus,\n            Eucalyptus, etc. set this to the port on which that system's EC2 interface is listening on.\n            "),
     Option(name='server-path', getter='ec2-server-path', type=OPTTYPE_STRING, required=False, doc="\n            The path portion of the EC2 server. If you are using Amazon AWS, leave this option\n            unspecified. If you are using an EC2-compatible system, such as OpenNebula, OpenStack,\n            Eucalyptus, etc. set this to the path (in the host specified in ``server-hostname``)\n            that the system's EC2 interface is available on.\n            ")]
    sections.append(ec2)
    go = Section('globusonline', required=False, doc="\n                  When a topology includes Globus Online transfer endpoints, Globus Provision will\n                  use GO's API to set up those endpoints. To do so, it will need some information\n                  about your GO account. If you are unclear on what values you need to specify here, \n                  see :ref:`chap_go` for more detailed instructions.\n                  ")
    go.options = [
     Option(name='ssh-key', getter='go-ssh-key', type=OPTTYPE_FILE, default='~/.ssh/id_rsa', required=False, doc='\n            SSH key to use when connecting to the Globus Online CLI. The public key\n            for this SSH key must have been previously added to your Globus Online\n            profile.\n            '),
     Option(name='cert-file', getter='go-cert-file', type=OPTTYPE_FILE, required=False, doc="\n            When this option is specified, Globus Provision will access your GO\n            account using Globus Online's Transfer API (instead of sending commands\n            to Globus Online's CLI via SSH). To do so, Globus Provision needs the\n            location of a user certificate (PEM-encoded) that is authorized to access \n            the accounts specified in your topology's endpoints.\n            \n            See :ref:`chap_go` for more details on the differences between using the\n            Transfer API, instead of the CLI via SSH.\n            "),
     Option(name='key-file', getter='go-key-file', type=OPTTYPE_FILE, required=False, doc='\n            Location of the private key (PEM-encoded) for the certificate\n            specified in ``cert-file``.\n            '),
     Option(name='server-ca-file', getter='go-server-ca-file', type=OPTTYPE_STRING, required=False, doc='\n            To verify the server certificate of the Globus Online Transfer API server,\n            Globus Provision needs the certificate of the CA that signed that certificate.\n            This file is already bundled with Globus Provision. The only reason for using\n            this option to specify a different CA certificate is in the unlikely case that\n            the API server decides to switch to a different CA (and the file bundled\n            with Globus Provision has not been updated to that CA yet).\n            ')]
    sections.append(go)

    def __init__(self, config_file):
        Config.__init__(self, config_file, self.sections)


class SimpleTopologyConfig(Config):
    """
    The simple topology file
    """
    sections = []
    general = Section('general', required=True, doc='This section is used for general options affecting all the topology.')
    general.options = [
     Option(name='domains', getter='domains', type=OPTTYPE_STRING, required=True, doc='\n            The names of the domains you are defining in this topology. They must each be separated by\n            a single space.      \n            '),
     Option(name='deploy', getter='deploy', type=OPTTYPE_STRING, required=True, valid=[
      'ec2', 'dummy'], doc='\n            See the :ref:`deploy option <GPConfig_deploy>` in :ref:`chap_config_ref` \n            '),
     Option(name='ssh-pubkey', getter='ssh-pubkey', type=OPTTYPE_FILE, required=False, default='~/.ssh/id_rsa.pub', doc="\n            When creating users, an SSH public key must be added to their ``authorized_keys`` file\n            to allow the creator of the topology to log in as those users. When using a topology file,\n            each SSH key is specified separately for each user; in a simple topology, you can specify\n            a single SSH public key for all the users (by default, the SSH key of the topology's creator \n            will be used)\n            \n            Take into account that you *can* specify per-user SSH keys in a simple topology by using the\n            :ref:`users-file option<SimpleTopologyConfig_users-file>`.\n            ")]
    sections.append(general)
    domain = Section('domain', required=False, multiple=('general', 'domains'), doc='\n                     For each domain specified in the ``domains`` option, you will need to specify a section\n                     titled ``[domain-DDD]`` where ``DD`` is the name of the domain. For example, if you specify the following::\n                     \n                         [general]\n                         domains: foo bar\n                         \n                     You will need to specify the following sections::\n                     \n                         [domain-foo]\n                         ...\n                         \n                         [domain-bar]\n                         ...\n                         \n                     Each section provides a few high-level options about each domain.\n                     This provides a simple, but constrained, way of specifying what services and users\n                     should be created in each domain. For more complex topologies, you may have\n                     to write a regular :ref:`topology file <chap_topology>`.                     \n                     ')
    domain.options = [
     Option(name='users', getter='users', type=OPTTYPE_STRING, required=False, default='0', doc='\n            This option can be either a number, or a list of usernames separated by spaces.\n            \n            If a number is specified, the users will be named ``D-userN``, where ``D`` is the\n            domain name and ``N`` is a number between 1 and the number specified in this option.\n            \n            If a list of usernames is specified, users with those login names will be created.\n            Optionally, a password for each user can be specified by adding a colon and the password\n            after the login name (e.g., ``alice:foo bob:bar carol:baz``)\n            \n            These users will be created with corresponding user certificates. To create users without user certificates\n            use option ``users-no-cert``.        \n            '),
     Option(name='users-no-cert', getter='users-no-cert', type=OPTTYPE_STRING, default='0', required=False, doc='\n            Same as ``users`` but creating users without certificates.\n            \n            Note that if you specify a number for *both* the ``users`` and ``users-no-cert`` option \n            (with values N and M, respectively), the first N users will have certificates, and the \n            remaining M will not.        \n            '),
     Option(name='users-file', getter='users-file', type=OPTTYPE_FILE, required=False, doc="\n            The path to a file with a specification of the users to create in this domain. This file will have one line\n            per user, each with three fields (separated by whitespace):\n            \n            #. A single character, ``C`` or ``N``. If ``C`` is specified, the user will have a user certificate created\n               for it. Otherwise, it will nor.\n            #. The user's UNIX login name.\n            #. (Optional) An SSH public key to add to the user's ``authorized_keys`` file. If not specified, the public\n               key specified in :ref:`option ssh-pubkey<SimpleTopologyConfig_ssh-pubkey>` will be used.\n              \n            For example::\n            \n                C borja     ssh-rsa FOOFOOFOO...BARBARBAR borja@example.org\n                C childers  ssh-rsa FOOFOOFOO...BARBARBAR childers@example.org\n                N foster\n                N madduri\n            \n            "),
     Option(name='nis', getter='nis', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether an NIS server should be setup in this domain. When ``True``, there will be a\n            user account space in the domain. When ``False``, user accounts and home directories will be \n            created on every individual host. This option can be useful if you are creating a single-host domain.       \n            '),
     Option(name='barebones-nodes', getter='barebones-nodes', type=OPTTYPE_INT, default=0, required=False, doc='\n            A "barebones node" is a node on which no software will be installed. If ``nfs-nis`` is ``True``,\n            these nodes *will* be configured as NFS/NIS clients. These nodes can be useful for testing.   \n            '),
     Option(name='filesystem', getter='filesystem', type=OPTTYPE_STRING, required=False, default='local-only', valid=[
      'local-only', 'nfs'], doc='\n            Specifies what type of filesystem the nodes in the instance will have:\n            \n            * ``local-only``:  Nodes will only have their local filesystems.\n            * ``nfs``: Nodes will share an NFS filesystem (this will create an extra node\n              that will act as the NFS server)     \n            '),
     Option(name='login', getter='login', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether a separate "login node" should be created in the topology. This option can be useful if you\n            want a distinct node that users can log into but that does not host one of the topology\'s servers (like the NFS\n            server, a GridFTP server, etc.)        \n            '),
     Option(name='myproxy', getter='myproxy', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether to set up a MyProxy server on this domain.        \n            '),
     Option(name='gram', getter='gram', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether to set up a GRAM5 server on this domain.             \n            '),
     Option(name='gridftp', getter='gridftp', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether to set up a GridFTP server on this domain.             \n            '),
     Option(name='simpleca', getter='simpleca', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether to set up a node with SimpleCA.             \n            '),
     Option(name='gridmap', getter='gridmap', type=OPTTYPE_BOOLEAN, required=False, default=True, doc='\n            Specifies whether to set up a gridmap file with all the users in this domain.             \n            '),
     Option(name='condor', getter='condor', type=OPTTYPE_BOOLEAN, default=False, required=False, doc='\n            Specifies whether to set up a `Condor <http://www.cs.wisc.edu/condor/>`_ cluster\n            in this domain.   \n            '),
     Option(name='condor-nodes', getter='condor-nodes', type=OPTTYPE_INT, required=False, doc='\n            The number of Condor worker nodes to create.        \n            '),
     Option(name='hadoop', getter='hadoop', type=OPTTYPE_BOOLEAN, default=False, required=False, doc='\n            Specifies whether to set up a `Hadoop <http://hadoop.apache.org/>`_ cluster\n            in this domain.   \n            '),
     Option(name='hadoop-nodes', getter='hadoop-nodes', type=OPTTYPE_INT, required=False, doc='\n            The number of Hadoop slave nodes to create.        \n            '),
     Option(name='R', getter='R', type=OPTTYPE_BOOLEAN, default=False, required=False, doc='\n            Specifies whether to install R in this domain.   \n            '),
     Option(name='galaxy', getter='galaxy', type=OPTTYPE_BOOLEAN, required=False, default=False, doc='\n            Specifies whether to set up a Galaxy server on this domain.        \n            '),
     Option(name='go-endpoint', getter='go-endpoint', type=OPTTYPE_STRING, required=False, doc='\n            If this domain has a GridFTP server, it can be configured as a GO endpoint.\n            The format for this option is <username>#<name> (e.g., johnsmith#test-ep).\n            Take into account that you must be authorized to use the GO account for <username>,\n            and that you must specify the appropriate credentials in the \n            :ref:`[globusonline] section<GPConfig_section_globusonline>` of the configuration file.\n            \n            See :ref:`chap_go` for more details.    \n            '),
     Option(name='go-auth', getter='go-auth', type=OPTTYPE_STRING, required=False, valid=[
      'myproxy', 'go'], doc='\n            The authentication method that Globus Online will use when contacting the endpoint on\n            behalf of a user. The valid options are:\n            \n            * ``myproxy``: Contact the MyProxy server specified in the topology. Note that \n              the :ref:`myproxy option<SimpleTopologyConfig_myproxy>` must be set to ``true`` \n              for this to work\n            * ``go``: Use Globus Online authentication.\n              \n            See :ref:`chap_go`, and specifically :ref:`Globus Online Authentication Methods <sec_go_auth>`,\n            for more details on the implications of each authentication method.            \n            '),
     Option(name='go-gc', getter='go-gc', type=OPTTYPE_BOOLEAN, required=False, default=True, doc='\n            If true, the endpoint will use a Globus Connect certificate.\n            If not, it will use the host certificate generated by Globus Provision.\n            Take into account that, for the GridFTP server to be trusted by\n            Globus Online, it must use a certificate trusted by Globus Online.\n            Unless you used a CA trusted by Globus Online to generate the certificates\n            for the topology, you must use a Globus Connect certificate.\n            ')]
    sections.append(domain)
    ec2 = Section('ec2', required=False, required_if=[
     (
      (
       'general', 'deploy'), 'ec2')], doc='\n                         When the EC2 deployer is selected, this section will allow you to\n                         specify EC2 deployment options that are specific to this topology.')
    ec2.options = [
     Option(name='ami', getter='ec2-ami', type=OPTTYPE_STRING, required=False, default=AMI['us-east-1']['32-bit'], doc='\n            This is the AMI (`Amazon Machine Image <http://en.wikipedia.org/wiki/Amazon_Machine_Image>`_) \n            that Globus Provision will use to create each host in the domain. Any recent Ubuntu or Debian\n            AMI should work. Nonetheless, take into account that we provide an AMI that has most of the\n            necessary software pre-installed in it, considerably speeding up the setup of the machines. \n            The latest Globus Provision AMI is always listed in the Globus Provision website.\n            \n            If "latest-32bit", "latest-64bit", or "latest-hvm" is specified for this value, then the\n            latest AMI (32-bit, 64-bit, or HVM, respectively) known to work with this version of\n            Globus Provision will be used. If no AMI is specified, the latest 32-bit AMI will be used.\n            '),
     Option(name='instance-type', getter='ec2-instance-type', type=OPTTYPE_STRING, required=True, default='t1.micro', doc='\n            This is the `EC2 instance type <http://en.wikipedia.org/wiki/Amazon_Machine_Image>`_ that will\n            be used to launch the machines in this domain. The default is to use micro-instances (t1.micro),\n            which tend to be enough if you are just tinkering around.\n            '),
     Option(name='availability-zone', getter='ec2-availability-zone', type=OPTTYPE_STRING, required=False, default=None, doc='\n            The `availability zone <http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/concepts-regions-availability-zones.html>`_ \n            you want the VMs to be deployed in. \n            Unless you have a good reason for choosing a specific availability zone,\n            you should let Globus Provision choose a default zone for you.\n            ')]
    sections.append(ec2)

    def __init__(self, configfile):
        Config.__init__(self, configfile, self.sections)

    def to_topology(self):
        ssh_pubkeyf = os.path.expanduser(self.get('ssh-pubkey'))
        ssh_pubkeyf = open(ssh_pubkeyf)
        ssh_pubkey = ssh_pubkeyf.read().strip()
        ssh_pubkeyf.close()
        topology = Topology()
        if self.get('deploy') == 'dummy':
            pass
        elif self.get('deploy') == 'ec2':
            deploy_data = DeployData()
            ec2_deploy_data = EC2DeployData()
            ami = self.get('ec2-ami')
            if ami == 'latest-32bit':
                ami = AMI['us-east-1']['32-bit']
            elif ami == 'latest-64bit':
                ami = AMI['us-east-1']['64-bit']
            elif ami == 'latest-hvm':
                ami = AMI['us-east-1']['hvm']
            ec2_deploy_data.set_property('ami', ami)
            ec2_deploy_data.set_property('instance_type', self.get('ec2-instance-type'))
            deploy_data.set_property('ec2', ec2_deploy_data)
            topology.set_property('default_deploy_data', deploy_data)
        domains = self.get('domains').split()
        for domain_name in domains:
            domain = Domain()
            domain.set_property('id', domain_name)
            topology.add_to_array('domains', domain)
            glusterfs_servers = []
            has_go_ep = self.get((domain_name, 'go-endpoint')) != None
            user = User()
            user.set_property('id', getpass.getuser())
            user.set_property('password_hash', '!')
            user.set_property('certificate', 'generated')
            user.set_property('admin', True)
            user.set_property('ssh_pkey', ssh_pubkey)
            domain.add_user(user)
            usersfile = self.get((domain_name, 'users-file'))
            if usersfile != None:
                usersfile = open(usersfile, 'r')
                for line in usersfile:
                    fields = line.split()
                    type = fields[0]
                    username = fields[1]
                    if len(fields) >= 3:
                        user_ssh_pubkey = (' ').join(fields[2:])
                    else:
                        user_ssh_pubkey = ssh_pubkey
                    user = User()
                    user.set_property('id', username)
                    user.set_property('password_hash', '!')
                    user.set_property('ssh_pkey', user_ssh_pubkey)
                    if type == 'C':
                        user.set_property('certificate', 'generated')
                    else:
                        user.set_property('certificate', 'none')
                    domain.add_user(user)

                usersfile.close()
            else:
                users = self.get((domain_name, 'users'))
                users_nocert = self.get((domain_name, 'users-no-cert'))
                if users.isdigit():
                    num_users = int(users)
                    usernames = [ ('%s-user%i' % (domain_name, i), True) for i in range(1, num_users + 1) ]
                else:
                    num_users = 0
                    usernames = [ (u, True) for u in users.split() if u != getpass.getuser() ]
                if users_nocert.isdigit():
                    usernames += [ ('%s-user%i' % (domain_name, i), False) for i in range(num_users + 1, num_users + int(users_nocert) + 1) ]
                else:
                    usernames += [ (u, False) for u in users_nocert.split() if u != getpass.getuser() ]
                for (username, cert) in usernames:
                    userpass = username.split(':')
                    login = userpass[0]
                    if len(userpass) == 1:
                        password = '!'
                    elif len(userpass) > 1:
                        password = gen_sha512(userpass[1])
                    user = User()
                    user.set_property('id', login)
                    user.set_property('password_hash', password)
                    user.set_property('ssh_pkey', ssh_pubkey)
                    if cert:
                        user.set_property('certificate', 'generated')
                    else:
                        user.set_property('certificate', 'none')
                    domain.add_user(user)

                if self.get((domain_name, 'gridmap')):
                    for user in domain.users.values():
                        gme = GridMapEntry()
                        gme.set_property('dn', '/O=Grid/OU=Globus Provision (generated)/CN=%s' % user.id)
                        gme.set_property('login', user.id)
                        domain.add_to_array('gridmap', gme)

                nis_server = None
                fs = FileSystem()
                domain.set_property('filesystem', fs)
                fs_type = self.get((domain_name, 'filesystem'))
                fs_headnode = None
                if self.get((domain_name, 'nis')) or fs_type == 'nfs':
                    server_node = Node()
                    server_name = '%s-server' % domain_name
                    server_node.set_property('id', server_name)
                    server_node.add_to_array('run_list', 'recipe[provision::gp_node]')
                    server_node.add_to_array('run_list', 'recipe[provision::nis_server]')
                    if not self.get((domain_name, 'login')):
                        server_node.add_to_array('run_list', 'role[globus]')
                    fs_headnode = server_node
                    if self.get((domain_name, 'nis')):
                        nis_server = server_node
                    domain.add_node(server_node)
                if fs_type == 'local-only':
                    fs.set_property('dir_homes', '/home')
                    fs.set_property('dir_software', '/usr/local')
                    fs.set_property('dir_scratch', '/var/tmp')
                if fs_type == 'nfs':
                    fs_headnode.add_to_array('run_list', 'recipe[provision::nfs_server]')
                    fs.set_property('dir_homes', '/nfs/home')
                    fs.set_property('dir_software', '/nfs/software')
                    fs.set_property('dir_scratch', '/nfs/scratch')
                    mounts = [
                     ('/nfs/home', '0755', '/nfs/home'),
                     ('/nfs/software/', '0755', '/nfs/software'),
                     ('/ephemeral/0/scratch', '1777', '/nfs/scratch')]
                    for (path, mode, mountpoint) in mounts:
                        mount = NFSMount()
                        mount.set_property('server', 'node:%s' % fs_headnode.id)
                        mount.set_property('owner', 'root')
                        mount.set_property('mode', mode)
                        mount.set_property('path', path)
                        mount.set_property('mountpoint', mountpoint)
                        fs.add_to_array('nfs_mounts', mount)

                if fs_type == 'glusterfs':
                    glusterfs_servers_num = self.get((domain_name, 'glusterfs-servers'))
                    glusterfs_type = self.get((domain_name, 'glusterfs-type'))
                    glusterfs_setsize = self.get((domain_name, 'glusterfs-setsize'))
                    domain.set_property('glusterfs_type', glusterfs_type)
                    domain.set_property('glusterfs_setsize', glusterfs_setsize)
                    glusterfs_servers = []
                    name = 'glusterfsd-1'
                    head_node = self.__create_node(domain, name, nis_server)
                    head_node.add_to_array('run_list', 'recipe[glusterfs::glusterfs-server-head]')
                    glusterfs_servers.append('%s-%s' % (domain_name, name))
                    fs_headnode = head_node
                    for i in range(1, glusterfs_servers_num):
                        name = 'glusterfsd-%i' % (i + 1)
                        node = self.__create_node(domain, name, nis_server)
                        node.add_to_array('run_list', 'recipe[glusterfs::glusterfs-server]')
                        node_name = '%s-%s' % (domain_name, name)
                        glusterfs_servers.append(node_name)
                        head_node.add_to_array('depends', 'node:%s' % node_name)

                if self.get((domain_name, 'nis')):
                    nis_server.add_to_array('run_list', 'recipe[provision::domain_users]')
                if fs_headnode != None:
                    fs_headnode.add_to_array('run_list', 'recipe[provision::software_path-common]')
                    if self.get((domain_name, 'R')):
                        fs_headnode.add_to_array('run_list', 'recipe[R::Rlibs-dir-common]')
                    if self.get((domain_name, 'galaxy')):
                        fs_headnode.add_to_array('run_list', 'recipe[galaxy::galaxy-globus-common]')
                        fs_headnode.add_to_array('run_list', 'recipe[galaxy::blast-nfsserver]')
                    if self.get((domain_name, 'hadoop')):
                        fs_headnode.add_to_array('run_list', 'recipe[hadoop::hadoop-common]')
                        if self.get((domain_name, 'R')):
                            fs_headnode.add_to_array('run_list', 'recipe[hadoop::rhadoop-common]')
                for i in range(self.get((domain_name, 'barebones-nodes'))):
                    node = self.__create_node(domain, 'blank-%i' % (i + 1), nis_server)
                    node.add_to_array('run_list', 'role[globus]')

                if self.get((domain_name, 'login')):
                    node = self.__create_node(domain, 'login', nis_server)
                    node.add_to_array('run_list', 'role[globus]')
                    if self.get((domain_name, 'R')):
                        node.add_to_array('run_list', 'recipe[R]')
                        node.add_to_array('run_list', 'recipe[R::Rlibs-dir]')
                if self.get((domain_name, 'simpleca')):
                    node = self.__create_node(domain, 'simpleca', nis_server)
                    node.add_to_array('run_list', 'role[globus]')
                    node.add_to_array('run_list', 'recipe[provision::simpleca]')
                gridftp_node = None
                myproxy_node = None
                if self.get((domain_name, 'myproxy')) and self.get((domain_name, 'gridftp')) and has_go_ep and self.get((domain_name, 'go-gc')):
                    node = self.__create_node(domain, 'myproxy-gridftp', nis_server)
                    node.add_to_array('run_list', 'role[domain-myproxy-gc]')
                    node.add_to_array('run_list', 'role[domain-gridftp-gc]')
                    gridftp_node = myproxy_node = node
                else:
                    if self.get((domain_name, 'myproxy')):
                        myproxy_node = self.__create_node(domain, 'myproxy', nis_server)
                        if has_go_ep:
                            if self.get((domain_name, 'go-gc')):
                                myproxy_node.add_to_array('run_list', 'role[domain-myproxy-gc]')
                            else:
                                myproxy_node.add_to_array('run_list', 'recipe[globus::go_cert]')
                                myproxy_node.add_to_array('run_list', 'role[domain-myproxy-default]')
                        else:
                            myproxy_node.add_to_array('run_list', 'role[domain-myproxy-default]')
                    if self.get((domain_name, 'gridftp')):
                        gridftp_node = self.__create_node(domain, 'gridftp', nis_server)
                        if has_go_ep:
                            if self.get((domain_name, 'go-gc')):
                                gridftp_node.add_to_array('run_list', 'role[domain-gridftp-gc]')
                            else:
                                gridftp_node.add_to_array('run_list', 'recipe[globus::go_cert]')
                                gridftp_node.add_to_array('run_list', 'role[domain-gridftp-default]')
                        else:
                            gridftp_node.add_to_array('run_list', 'role[domain-gridftp-default]')
                if self.get((domain_name, 'galaxy')) and not self.get((domain_name, 'condor')):
                    node = self.__create_node(domain, 'galaxy', nis_server)
                    if fs_type == 'local-only':
                        node.add_to_array('run_list', 'recipe[galaxy::galaxy-globus-common]')
                    if self.get((domain_name, 'go-endpoint')) != None:
                        node.add_to_array('run_list', 'recipe[globus::go_cert]')
                    node.add_to_array('run_list', 'recipe[galaxy::galaxy-globus]')
            if self.get((domain_name, 'condor')):
                galaxy = self.get((domain_name, 'galaxy'))
                if self.get((domain_name, 'gram')):
                    head_name = 'gram-condor'
                    head_role = 'role[domain-gram-condor]'
                else:
                    if galaxy:
                        head_name = 'galaxy-condor'
                    else:
                        head_name = 'condor'
                    head_role = 'role[domain-condor]'
                worker_name = 'condor-wn'
                worker_role = 'role[domain-clusternode-condor]'
                num_workers = self.get((domain.id, 'condor-nodes'))
                (head_node, workers) = self.__gen_cluster(domain, nis_server, None, head_name, head_role, worker_name, worker_role, num_workers)
                if self.get((domain_name, 'galaxy')):
                    if fs_type == 'local-only':
                        head_node.add_to_array('run_list', 'recipe[galaxy::galaxy-globus-common]')
                    if self.get((domain_name, 'go-endpoint')) != None:
                        head_node.add_to_array('run_list', 'recipe[globus::go_cert]')
                    head_node.add_to_array('run_list', 'recipe[galaxy::galaxy-globus]')
            if self.get((domain_name, 'hadoop')):
                head_name = 'hadoop-master'
                head_role = 'role[domain-hadoop-master]'
                worker_name = 'hadoop-slave'
                worker_role = 'role[domain-hadoop-slave]'
                num_workers = self.get((domain.id, 'hadoop-nodes'))
                if fs_type == 'local-only':
                    common_recipe = 'recipe[hadoop::hadoop-common]'
                else:
                    common_recipe = None
                (head_node, workers) = self.__gen_cluster(domain, nis_server, common_recipe, head_name, head_role, worker_name, worker_role, num_workers, head_depends_on_workers=True)
                if self.get((domain_name, 'R')):
                    for n in [head_node] + workers:
                        n.add_to_array('run_list', 'recipe[R]')
                        n.add_to_array('run_list', 'recipe[R::Rlibs-dir]')

            if has_go_ep:
                goep = GOEndpoint()
                (gouser, goname) = self.get((domain_name, 'go-endpoint')).split('#')
                goep.set_property('user', gouser)
                goep.set_property('name', goname)
                goep.set_property('public', False)
                goep.set_property('gridftp', 'node:%s' % gridftp_node.id)
                if self.get((domain_name, 'go-auth')) == 'myproxy':
                    goep.set_property('myproxy', 'node:%s' % myproxy_node.id)
                else:
                    goep.set_property('myproxy', 'myproxy.globusonline.org')
                goep.set_property('globus_connect_cert', self.get((domain_name, 'go-gc')))
                domain.add_to_array('go_endpoints', goep)
                for user in domain.users.values():
                    if self.get((domain_name, 'go-auth')) == 'go':
                        gme = GridMapEntry()
                        gme.set_property('dn', '/C=US/O=Globus Consortium/OU=Globus Connect User/CN=%s' % user.id)
                        gme.set_property('login', user.id)
                        domain.add_to_array('gridmap', gme)

        return topology

    def __gen_cluster(self, domain, nis_server, common_recipe, head_name, head_role, worker_name, worker_role, num_workers, head_depends_on_workers=False):
        head_node = self.__create_node(domain, head_name, nis_server)
        if common_recipe != None:
            head_node.add_to_array('run_list', common_recipe)
        head_node.add_to_array('run_list', head_role)
        workers = []
        for i in range(num_workers):
            wn_name = '%s%i' % (worker_name, i + 1)
            wn_node = self.__create_node(domain, wn_name, nis_server)
            if head_depends_on_workers:
                head_node.add_to_array('depends', 'node:%s' % wn_node.id)
            else:
                wn_node.add_to_array('depends', 'node:%s' % head_node.id)
            if common_recipe != None:
                head_node.add_to_array('run_list', common_recipe)
            wn_node.add_to_array('run_list', worker_role)
            workers.append(wn_node)

        return (head_node, workers)

    def __create_node(self, domain, name, nis_server):
        domain_name = domain.id
        node = Node()
        node.set_property('id', '%s-%s' % (domain_name, name))
        node.add_to_array('run_list', 'recipe[provision::gp_node]')
        node.add_to_array('run_list', 'recipe[provision::software_path]')
        depends = set()
        if nis_server != None:
            depends.add('node:%s' % nis_server.id)
            node.add_to_array('run_list', 'recipe[provision::nis_client]')
        else:
            node.add_to_array('run_list', 'recipe[provision::domain_users]')
        if domain.filesystem.has_nfs():
            nfs_servers = set([ mount.server for mount in domain.filesystem.nfs_mounts ])
            for nfs_server in nfs_servers:
                depends.add(nfs_server)
                node.add_to_array('run_list', 'recipe[provision::nfs_client]')

        if domain.filesystem.has_glusterfs():
            node.add_to_array('run_list', 'recipe[glusterfs::glusterfs-client]')
        for d in depends:
            node.add_to_array('depends', d)

        domain.add_node(node)
        return node