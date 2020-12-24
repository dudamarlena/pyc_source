# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/core/topology.py
# Compiled at: 2012-03-02 22:17:19
"""
Topology

This module contains classes used to manage a topology. All of these classes
are PersistentObjects, so the properties are defined separately from
the classes themselves, which can make the code a bit hard to read. 
Before diving into this code, you may want to check out the topology 
documentation (in the Globus Provision Documentation), which is automatically
generated from the code in this module.  

"""
from globus.provision.common.persistence import PersistentObject, PropertyTypes, Property

class Topology(PersistentObject):
    STATE_NEW = 1
    STATE_STARTING = 2
    STATE_CONFIGURING = 3
    STATE_RUNNING = 4
    STATE_STOPPING = 5
    STATE_STOPPED = 6
    STATE_RESUMING = 7
    STATE_TERMINATING = 8
    STATE_TERMINATED = 9
    STATE_FAILED = 10
    state_str = {STATE_NEW: 'New', STATE_STARTING: 'Starting', 
       STATE_CONFIGURING: 'Configuring', 
       STATE_RUNNING: 'Running', 
       STATE_STOPPING: 'Stopping', 
       STATE_STOPPED: 'Stopped', 
       STATE_RESUMING: 'Resuming', 
       STATE_TERMINATING: 'Terminating', 
       STATE_TERMINATED: 'Terminated', 
       STATE_FAILED: 'Failed'}

    def get_nodes(self):
        nodes = []
        for domain in self.domains.values():
            nodes += [ n for n in domain.get_nodes() ]

        return nodes

    def get_users(self):
        users = []
        for domain in self.domains.values():
            users += domain.get_users()

        return users

    def gen_hosts_file(self, filename):
        hosts = '127.0.0.1    localhost\n\n# The following lines are desirable for IPv6 capable hosts\n::1     localhost ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\nff02::3 ip6-allhosts\n\n'
        nodes = self.get_nodes()
        for n in nodes:
            hosts += (' ').join((n.ip, n.hostname, n.hostname.split('.')[0], '\n'))

        hostsfile = open(filename, 'w')
        hostsfile.write(hosts)
        hostsfile.close()

    def gen_chef_ruby_file(self, filename):

        def gen_topology_line(server_name, domain_id, recipes, multi=False):
            servers = domain.find_with_recipes(recipes)
            if len(servers) > 0:
                if not multi:
                    server_node = servers[0]
                    if len(servers) > 1:
                        pass
                    servers_hostnames = '"%s"' % server_node.hostname
                    servers_ips = '"%s"' % server_node.ip
                else:
                    servers_hostnames = '[%s]' % (',').join([ '"%s"' % s.hostname for s in servers ])
                    servers_ips = '[%s]' % (',').join([ '"%s"' % s.ip for s in servers ])
                hostname_line = 'default[:topology][:domains]["%s"][:%s] = %s\n' % (domain_id, server_name, servers_hostnames)
                ip_line = 'default[:topology][:domains]["%s"][:%s_ip] = %s\n' % (domain_id, server_name, servers_ips)
                return hostname_line + ip_line
            else:
                return ''

        topology = 'default[:topology] = %s\n' % self.to_ruby_hash_string()
        for domain in self.domains.values():
            topology += gen_topology_line('nis_server', domain.id, ['recipe[provision::nis_server]', 'role[domain-nfsnis]'])
            topology += gen_topology_line('myproxy_server', domain.id, ['recipe[globus::myproxy]'])
            topology += gen_topology_line('condor_head', domain.id, ['recipe[condor::condor_head]', 'role[domain-condor]'])
            topology += gen_topology_line('hadoop_master', domain.id, ['recipe[hadoop::hadoop-master]', 'role[domain-hadoop-master]'])
            if domain.has_property('glusterfs_type'):
                topology += 'default[:topology][:domains]["%s"][:glusterfs_type] = "%s"\n' % (domain.id, domain.glusterfs_type)
                topology += 'default[:topology][:domains]["%s"][:glusterfs_setsize] = %i\n' % (domain.id, domain.glusterfs_setsize)

        topologyfile = open(filename, 'w')
        topologyfile.write(topology)
        topologyfile.close()

    def get_depends(self, node):
        if not hasattr(node, 'depends'):
            return []
        else:
            return [ self.get_node_by_id(d[5:]) for d in node.depends ]

    def get_launch_order(self, nodes):
        order = []
        no_depends = [ n for n in nodes if len(self.get_depends(n)) == 0 or len(set(self.get_depends(n)) & set(nodes)) == 0 ]
        while len(no_depends) > 0:
            node = no_depends.pop()
            order.append(node)
            dependents = [ n for n in nodes if node in self.get_depends(n) ]
            for dependent in dependents:
                parents = self.get_depends(dependent)
                if set(parents) <= set(order):
                    no_depends.append(dependent)

        return order

    def get_node_by_id(self, node_id):
        nodes = self.get_nodes()
        node = [ n for n in nodes if n.id == node_id ]
        if len(node) == 1:
            return node[0]
        else:
            return
            return

    def get_deploy_data(self, node, deployer, p_name):
        if node.has_property('deploy_data') and node.deploy_data.has_property(deployer):
            deploy_data = node.deploy_data.get_property(deployer)
            if deploy_data.has_property(p_name):
                return deploy_data.get_property(p_name)
        if self.has_property('default_deploy_data') and self.default_deploy_data.has_property(deployer):
            deploy_data = self.default_deploy_data.get_property(deployer)
            if deploy_data.has_property(p_name):
                return deploy_data.get_property(p_name)
        return

    def get_go_endpoints(self):
        eps = []
        for (domain_name, domain) in self.domains.items():
            if domain.has_property('go_endpoints'):
                eps += domain.go_endpoints

        return eps

    def add_domain(self, domain):
        self.add_to_array('domains', domain)


class Domain(PersistentObject):

    def get_nodes(self):
        return self.nodes.values()

    def get_users(self):
        return self.users.values()

    def find_with_recipes(self, recipes):
        nodes = []
        for node in self.nodes.values():
            for r in recipes:
                if r in node.run_list:
                    nodes.append(node)
                    continue

        return nodes

    def add_user(self, user):
        self.add_to_array('users', user)

    def add_node(self, node):
        self.add_to_array('nodes', node)


class DeployData(PersistentObject):
    pass


class EC2DeployData(PersistentObject):
    pass


class Node(PersistentObject):
    STATE_NEW = 0
    STATE_STARTING = 1
    STATE_RUNNING_UNCONFIGURED = 2
    STATE_CONFIGURING = 3
    STATE_RUNNING = 4
    STATE_RECONFIGURING = 11
    STATE_STOPPING = 5
    STATE_STOPPING_CONFIGURING = 12
    STATE_STOPPING_CONFIGURED = 13
    STATE_STOPPED = 6
    STATE_RESUMING = 7
    STATE_RESUMED_UNCONFIGURED = 14
    STATE_RESUMED_RECONFIGURING = 15
    STATE_TERMINATING = 8
    STATE_TERMINATED = 9
    STATE_FAILED = 10
    state_str = {STATE_NEW: 'New', STATE_STARTING: 'Starting', 
       STATE_RUNNING_UNCONFIGURED: 'Running (unconfigured)', 
       STATE_CONFIGURING: 'Configuring', 
       STATE_RUNNING: 'Running', 
       STATE_RECONFIGURING: 'Running (reconfiguring)', 
       STATE_STOPPING: 'Stopping', 
       STATE_STOPPING_CONFIGURING: 'Stopping (configuring)', 
       STATE_STOPPING_CONFIGURED: 'Stopping (configured)', 
       STATE_STOPPED: 'Stopped', 
       STATE_RESUMING: 'Resuming', 
       STATE_RESUMED_UNCONFIGURED: 'Resumed (unconfigured)', 
       STATE_RESUMED_RECONFIGURING: 'Resumed (reconfiguring)', 
       STATE_TERMINATING: 'Terminating', 
       STATE_TERMINATED: 'Terminated', 
       STATE_FAILED: 'Failed'}

    def __repr__(self):
        return '<Node %s>' % self.id


class User(PersistentObject):
    pass


class FileSystem(PersistentObject):

    def has_nfs(self):
        if not self.has_property('nfs_mounts'):
            return False
        else:
            return len(self.nfs_mounts) > 0

    def has_glusterfs(self):
        if not self.has_property('glusterfs_vols'):
            return False
        else:
            return len(self.glusterfs_vols) > 0


class NFSMount(PersistentObject):
    pass


class GlusterFSVol(PersistentObject):
    pass


class GridMapEntry(PersistentObject):
    pass


class GOEndpoint(PersistentObject):
    pass


Topology.properties = {'id': Property(name='id', proptype=PropertyTypes.STRING, required=False, description='\n                                Once an instance with this topology has been created,\n                                this property will contain the instance ID \n                                (e.g., ``gpi-12345678``) assigned by Globus Provision.\n                                '), 
   'state': Property(name='state', proptype=PropertyTypes.INTEGER, required=False, description='\n                                Once an instance has been created with this topology,\n                                this property indicates the state the instance is in.\n                                Possible values are:\n                                \n                                %s\n                                \n                                ' % ('\n                                ').join([ '* %i: %s' % (i, Topology.state_str[i]) for i in sorted(Topology.state_str.keys()) ])), 
   'domains': Property(name='domains', proptype=PropertyTypes.ARRAY, items=Domain, items_unique=True, editable=True, required=True, description='\n                                The domains in this topology.\n                                '), 
   'default_deploy_data': Property(name='default_deploy_data', proptype=DeployData, required=False, editable=True, description='\n                                The default deployment-specific data for this instance.\n                                Individual nodes can override the default values in their\n                                ``deploy_data`` property.\n                                ')}
DeployData.properties = {'ec2': Property(name='ec2', proptype=EC2DeployData, required=False, editable=True, description='\n                                     Used to specify EC2-specific deployment data.\n                                     ')}
EC2DeployData.properties = {'instance_type': Property(name='instance_type', proptype=PropertyTypes.STRING, required=False, editable=True, description='\n                                         An EC2 instance type (e.g., ``t1.micro``, ``m1.small``, etc.)\n                                         '), 
   'instance_id': Property(name='instance_id', proptype=PropertyTypes.STRING, required=False, description='\n                                         Once a host has been deployed on EC2,\n                                         this property will contain its EC2 instance identifier.                                        \n                                         '), 
   'ami': Property(name='ami', proptype=PropertyTypes.STRING, required=False, editable=True, description='\n                                         The Amazon Machine Image (AMI) to use when creating\n                                         new hosts on Amazon EC2.\n                                         '), 
   'security_groups': Property(name='security_groups', proptype=PropertyTypes.ARRAY, items=PropertyTypes.STRING, items_unique=True, required=False, editable=True, description='\n                                         A list of `Security Groups <http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/index.html?using-network-security.html>`_\n                                         to apply to hosts on EC2. If no security groups are specified,\n                                         Globus Provision will create one called ``globus-provision``\n                                         that opens the TCP/UDP ports for SSH, GridFTP, and MyProxy. \n                                         ')}
Domain.properties = {'id': Property(name='id', proptype=PropertyTypes.STRING, required=True, description='\n                              A unique name for the domain.\n                              '), 
   'nodes': Property(name='nodes', proptype=PropertyTypes.ARRAY, items=Node, items_unique=True, required=True, editable=True, description='\n                              The list of hosts (or *nodes*) in this domain.\n                              '), 
   'filesystem': Property(name='filesystem', proptype=FileSystem, required=True, editable=False, description='\n                              The filesystem type in this domain.\n                              '), 
   'go_endpoints': Property(name='go_endpoints', proptype=PropertyTypes.ARRAY, items=GOEndpoint, required=False, editable=True, description='\n                              The list of Globus Online endpoints defined for this domain.\n                              '), 
   'users': Property(name='users', proptype=PropertyTypes.ARRAY, items=User, items_unique=True, required=True, editable=True, description='\n                              The list of users in this domain.\n                              '), 
   'gridmap': Property(name='gridmap', proptype=PropertyTypes.ARRAY, items=GridMapEntry, required=False, editable=True, description='\n                              The list of gridmap entries for this domain. This\n                              is the gridmap that Globus services running on this\n                              domain will use to determine if a given user is\n                              authorized to access the service.\n                              ')}
Node.properties = {'id': Property(name='id', proptype=PropertyTypes.STRING, required=True, description='\n                            A unique identifier for this host. The value of this\n                            property is only used for identification purposes\n                            (e.g., when printing the status of an instance with\n                            ``gp-instance-describe``), and will not affect other\n                            properties, like its hostname, etc. (except when using\n                            the ``dummy`` deployer).\n                            '), 
   'state': Property(name='state', proptype=PropertyTypes.INTEGER, required=False, editable=False, description='\n                            Once an instance with this topology has been created,\n                            this property will indicate the state of this particular\n                            host.\n                            \n                            Possible values are:\n                                \n                                %s\n                                \n                                ' % ('\n                                ').join([ '* %i: %s' % (i, Node.state_str[i]) for i in sorted(Node.state_str.keys()) ])), 
   'run_list': Property(name='run_list', proptype=PropertyTypes.ARRAY, items=PropertyTypes.STRING, required=True, editable=True, description='\n                            The list of Chef recipes to run on this node.\n                            See :ref:`sec_runlist` for more details.\n                            '), 
   'depends': Property(name='depends', proptype=PropertyTypes.ARRAY, items=PropertyTypes.STRING, required=False, editable=True, description='\n                            Sometimes, a host cannot be configured until others hosts\n                            in the topology is configured. For example, NFS clients cannot\n                            start until the NFS server is starting. This property is\n                            used to specify such dependencies. The value of this property\n                            must be of the form node:*node_id*, where *node_id* is\n                            the identifier of another node in the domain.\n                            \n                            For example, if this node depends on ``simple-nfs`` the value\n                            of this property would be a list with a single entry: ``node:simple-nfs``.\n                            '), 
   'hostname': Property(name='hostname', proptype=PropertyTypes.STRING, required=False, description='\n                            The fully-qualified hostname assigned by the deployer.\n                            '), 
   'ip': Property(name='ip', proptype=PropertyTypes.STRING, required=False, description='\n                            The IP address assigned by the deployer.\n                            '), 
   'public_ip': Property(name='public_ip', proptype=PropertyTypes.STRING, required=False, description='\n                            If the IP address assigned in ``ip`` is a private, non-routable,\n                            IP address, but the host is also assigned a public IP, it will\n                            be assigned to this property by the deployer.\n                            '), 
   'deploy_data': Property(name='deploy_data', proptype=DeployData, required=False, description="\n                            Host-specific deployment data. The values specified here\n                            will override any values specified in the topology's\n                            ``default_deploy__data`` property.\n                            "), 
   'gc_setupkey': Property(name='gc_setupkey', proptype=PropertyTypes.STRING, required=False, description='\n                            Globus Connect setup key used to obtain a certificate\n                            for use by services in this node. \n                            ')}
User.properties = {'id': Property(name='id', proptype=PropertyTypes.STRING, required=True, description="\n                            The user's login name.\n                            "), 
   'description': Property(name='description', proptype=PropertyTypes.STRING, required=False, editable=True, description='\n                            A description of the user.\n                            '), 
   'password_hash': Property(name='password_hash', proptype=PropertyTypes.STRING, required=True, editable=True, description='\n                            The password hash for the user, exactly as it will appear\n                            in the shadow file (``/etc/shadow``). To generate a password,\n                            you can use the ``mkpasswd`` command. We recommend you generate\n                            SHA-512 password hashes. For example::\n                            \n                                $ mkpasswd -m sha-512 mypassword\n                                $6$XrtqyXi4LO$8M/sk6t8zE5Ac.acLPBt577f1eGv.YnUVZPhGmBlQF/YrYnkWQPq7EMfryWEdHm664B.RaY3O8oZtbiQjXfu10\n                            \n                            The string starting with ``$6$`` is the password hash.\n                            \n                            You can disable password access for this user by setting this \n                            property to ``!``. \n                            '), 
   'ssh_pkey': Property(name='ssh_pkey', proptype=PropertyTypes.STRING, required=False, editable=True, description="\n                            A public SSH key. If a value is specified for this property,\n                            this public key will be added to the user's ``authorized_keys``\n                            file.\n                            "), 
   'admin': Property(name='admin', proptype=PropertyTypes.BOOLEAN, required=False, editable=True, description='\n                            If ``true``, this user will be granted passwordless sudo\n                            access on all hosts in this domain.\n                            '), 
   'certificate': Property(name='certificate', proptype=PropertyTypes.STRING, required=False, description='\n                            This property can take on the following values:\n                            \n                            * ``"generated"``: A user certificate must be generated for this user.\n                            * ``"none"``: Do not generate a certificate for this user.\n                            ')}
FileSystem.properties = {'dir_homes': Property(name='dir_homes', proptype=PropertyTypes.STRING, required=True, description='\n                            The directory containing the home directories.\n                            '), 
   'dir_software': Property(name='dir_software', proptype=PropertyTypes.STRING, required=True, description='\n                            The directory for additional software.\n                            '), 
   'dir_scratch': Property(name='dir_scratch', proptype=PropertyTypes.STRING, required=True, description='\n                            The scratch directory.\n                            '), 
   'nfs_mounts': Property(name='nfs_mounts', proptype=PropertyTypes.ARRAY, items=NFSMount, required=False, description='\n                            A list of NFS mounts.\n                            ')}
NFSMount.properties = {'server': Property(name='server', proptype=PropertyTypes.STRING, required=True, description='\n                            NFS server for this domain.\n                            '), 
   'path': Property(name='path', proptype=PropertyTypes.STRING, required=True, description='\n                            The path being mounted.\n                            '), 
   'mode': Property(name='mode', proptype=PropertyTypes.STRING, required=True, description='\n                            Mode to set for the mount.\n                            '), 
   'owner': Property(name='owner', proptype=PropertyTypes.STRING, required=True, description='\n                            User that will be set as owner of the mount.\n                            '), 
   'mountpoint': Property(name='mountpoint', proptype=PropertyTypes.STRING, required=True, description='\n                            The directory where this NFS mount will be mounted.\n                            ')}
GridMapEntry.properties = {'dn': Property(name='dn', proptype=PropertyTypes.STRING, required=True, description='\n                                    The distinguished name in the gridmap entry\n                                    (e.g., ``"/O=Grid/OU=My Grid/CN=J.Random User"``)\n                                    '), 
   'login': Property(name='login', proptype=PropertyTypes.STRING, required=True, editable=True, description='\n                                    The login the distinguished name will map to.\n                                    Must be a valid login in the domain.\n                                    ')}
GOEndpoint.properties = {'user': Property(name='user', proptype=PropertyTypes.STRING, required=True, description='\n                                    The Globus Online user account in which to create\n                                    this endpoint.\n                                    '), 
   'name': Property(name='name', proptype=PropertyTypes.STRING, required=True, description='\n                                    The endpoint name.\n                                    '), 
   'public': Property(name='public', proptype=PropertyTypes.BOOLEAN, required=True, description='\n                                    Whether the endpoint should be public or not.\n                                    '), 
   'gridftp': Property(name='gridftp', proptype=PropertyTypes.STRING, required=True, editable=True, description='\n                                    The GridFTP server for this endpoint. You can specify\n                                    either a fully qualified hostname, or refer to an existing\n                                    node in this domain by writing node:*node_id*, \n                                    where *node_id* is the identifier of another node in the domain.\n                                    '), 
   'myproxy': Property(name='myproxy', proptype=PropertyTypes.STRING, required=True, editable=True, description='\n                                    The MyProxy server that will be used for authenticating\n                                    users that want to use this endpoint. You can specify\n                                    either a fully qualified hostname, or refer to an existing\n                                    node in this domain by writing node:*node_id*, \n                                    where *node_id* is the identifier of another node in the domain.\n                                    \n                                    Take into account that, to set up this endpoint for\n                                    "Globus Online Authentication" (as described in :ref:`sec_go_auth`)\n                                    you will need to do the following:\n                                    \n                                    * Set this property to ``myproxy.globusonline.org``\n                                    * For each GO user you want to authorize in this endpoint,\n                                      add an entry with the following distinguished name::\n                                       \n                                           "/C=US/O=Globus Consortium/OU=Globus Connect User/CN=username"\n                                      \n                                      Where ``username`` is the username of the GO account you\n                                      want to authorized. Usually, you will want that DN to map\n                                      to the same username in the domain, although this is not\n                                      required.\n\n                                    '), 
   'globus_connect_cert': Property(name='globus_connect_cert', proptype=PropertyTypes.BOOLEAN, required=False, description='\n                                    If true, this endpoint will use a Globus Connect certificate.\n                                    If not, it will use the host certificate generated by Globus Provision.\n                                    Take into account that, for the GridFTP server to be trusted by\n                                    Globus Online, it must use a certificate trusted by Globus Online.\n                                    Unless you used a CA trusted by Globus Online to generate the certificates\n                                    for the topology, you must use a Globus Connect certificate.\n                                    '), 
   'globus_connect_cert_dn': Property(name='globus_connect_cert', proptype=PropertyTypes.STRING, required=False, description='\n                                    The DN of the Globus Connect certificate for this endpoint.\n                                    ')}