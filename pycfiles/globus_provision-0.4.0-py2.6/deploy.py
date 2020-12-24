# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/core/deploy.py
# Compiled at: 2012-03-02 22:17:19
"""
Core deployment classes.

These classes contain code that is common to all deployers (i.e., they don't 
contain any infrastructure-specific code).

To create a new deployer, you will need to extend classes the classes
in this module.

"""
from globus.provision.common.threads import GPThread
from globus.provision.common.ssh import SSH, SSHCommandFailureException
from globus.provision.common import log
from globus.provision.core.topology import Node
from abc import ABCMeta, abstractmethod

class DeploymentException(Exception):
    """A simple exception class used for deployment exceptions"""
    pass


class BaseDeployer(object):
    """
    The base class for a deployer.
    
    A deployer must implement all the abstract methods in this class
    """
    __metaclass__ = ABCMeta

    def __init__(self, extra_files=[], run_cmds=[]):
        self.instance = None
        self.extra_files = extra_files
        self.run_cmds = run_cmds
        return

    @abstractmethod
    def set_instance(self, inst):
        pass

    @abstractmethod
    def allocate_vm(self, node):
        pass

    @abstractmethod
    def post_allocate(self, node, vm):
        pass

    @abstractmethod
    def stop_vms(self, nodes):
        pass

    @abstractmethod
    def resume_vm(self, node):
        pass

    @abstractmethod
    def terminate_vms(self, nodes):
        pass

    @abstractmethod
    def get_node_vm(self, nodes):
        pass

    @abstractmethod
    def get_wait_thread_class(self):
        pass

    @abstractmethod
    def get_configure_thread_class(self):
        pass


class VM(object):
    """
    A VM object represents a virtual machine managed by a
    deployer. It is basically meant as an opaque type that
    can be returned by the deployer to the core, and then
    passed from the core to other functions in the deployer.
    """

    def __init__(self):
        pass


class WaitThread(GPThread):
    """
    The base class for "waiter threads".
    
    A derived class must implement the wait() method, with the
    deployer-specific code that will wait until a VM
    has reached a given state.
    """
    __metaclass__ = ABCMeta

    def __init__(self, multi, name, node, vm, deployer, state, depends):
        GPThread.__init__(self, multi, name, depends)
        self.node = node
        self.vm = vm
        self.deployer = deployer
        self.state = state

    def run2(self):
        topology = self.deployer.instance.topology
        self.wait()
        self.node.state = self.state
        topology.save()

    @abstractmethod
    def wait(self):
        pass


class ConfigureThread(GPThread):
    """
    The base class for "configure threads".
    
    This is a thread that takes care of configuring a single VM.
    Most of the actions (e.g., SSH'ing to the VM and running Chef)
    will be the same in most deployers. So, this class simply
    requires that derived classes implement pre_configure()
    and post_configure(), in case there are deployer-specific
    actions that must be taken. The connect() method must
    also be implemented, although it can usually just be
    a call to ssh_connect.
    """
    __metaclass__ = ABCMeta

    def __init__(self, multi, name, node, vm, deployer, depends=None, basic=True, chef=True, dryrun=False):
        GPThread.__init__(self, multi, name, depends)
        self.domain = node.parent_Domain
        self.node = node
        self.vm = vm
        self.deployer = deployer
        self.config = deployer.instance.config
        self.basic = basic
        self.chef = chef
        self.dryrun = dryrun

    def run2(self):
        topology = self.deployer.instance.topology
        if self.node.state in (Node.STATE_RUNNING_UNCONFIGURED, Node.STATE_RUNNING, Node.STATE_RESUMED_UNCONFIGURED):
            if self.node.state == Node.STATE_RUNNING_UNCONFIGURED:
                log.debug('Configuring node for the first time', self.node)
                self.node.state = Node.STATE_CONFIGURING
                next_state = Node.STATE_RUNNING
            elif self.node.state == Node.STATE_RUNNING:
                log.debug('Reconfiguring already-running node', self.node)
                self.node.state = Node.STATE_RECONFIGURING
                next_state = Node.STATE_RUNNING
            elif self.node.state == Node.STATE_RESUMED_UNCONFIGURED:
                log.debug('Reconfiguring resumed node', self.node)
                self.node.state = Node.STATE_RESUMED_RECONFIGURING
                next_state = Node.STATE_RUNNING
            topology.save()
            if not self.dryrun:
                ssh = self.connect()
                self.check_continue()
                self.pre_configure(ssh)
                self.check_continue()
                self.configure(ssh)
                self.check_continue()
                self.post_configure(ssh)
                self.check_continue()
            self.node.state = next_state
            topology.save()
        elif self.node.state == Node.STATE_STOPPING:
            log.debug('Doing pre-shutdown configuration', self.node)
            self.node.state = Node.STATE_STOPPING_CONFIGURING
            topology.save()
            if not self.dryrun:
                ssh = self.connect()
                self.check_continue()
                self.configure_stop(ssh)
                self.check_continue()
            self.node.state = Node.STATE_STOPPING_CONFIGURED
            topology.save()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def pre_configure(self):
        pass

    @abstractmethod
    def post_configure(self):
        pass

    def ssh_connect(self, username, hostname, keyfile):
        node = self.node
        log.debug('Establishing SSH connection', node)
        ssh = SSH(username, hostname, keyfile, default_outf=None, default_errf=None)
        try:
            ssh.open()
        except Exception, e:
            log.debug('SSH connection timed out', node)
            raise e

        log.debug('SSH connection established', node)
        return ssh

    def configure(self, ssh):
        domain = self.domain
        node = self.node
        instance_dir = self.deployer.instance.instance_dir
        if self.basic:
            if node.state in (Node.STATE_CONFIGURING, Node.STATE_RESUMED_RECONFIGURING):
                ssh.run('sudo cp /etc/hosts /etc/hosts.gp-bak', expectnooutput=True)
                ssh.run('sudo cp /etc/hostname /etc/hostname.gp-bak', expectnooutput=True)
            log.debug('Uploading host file and updating hostname', node)
            ssh.scp('%s/hosts' % instance_dir, '/chef/cookbooks/provision/files/default/hosts')
            ssh.run('sudo cp /chef/cookbooks/provision/files/default/hosts /etc/hosts', expectnooutput=True)
            ssh.run('sudo bash -c "echo %s > /etc/hostname"' % node.hostname, expectnooutput=True)
            ssh.run('sudo /etc/init.d/hostname.sh || sudo /etc/init.d/hostname restart', expectnooutput=True)
        self.check_continue()
        if self.chef:
            log.debug('Uploading topology file', node)
            ssh.scp('%s/topology.rb' % instance_dir, '/chef/cookbooks/provision/attributes/topology.rb')
            log.debug('Copying certificates', node)
            ssh.scp_dir('%s/certs' % instance_dir, '/chef/cookbooks/provision/files/default/')
            log.debug('Copying extra files', node)
            for (src, dst) in self.deployer.extra_files:
                ssh.scp(src, dst)

            self.check_continue()
            log.debug('Running chef', node)
            ssh.run('echo -e "cookbook_path \\"/chef/cookbooks\\"\\nrole_path \\"/chef/roles\\"" > /tmp/chef.conf', expectnooutput=True)
            ssh.run('echo \'{ "run_list": [ %s ], "scratch_dir": "%s", "domain_id": "%s", "node_id": "%s"  }\' > /tmp/chef.json' % ((',').join('"%s"' % r for r in node.run_list), self.config.get('scratch-dir'), domain.id, node.id), expectnooutput=True)
            chef_tries = 3
            while chef_tries > 0:
                rc = ssh.run('sudo -i chef-solo -c /tmp/chef.conf -j /tmp/chef.json', exception_on_error=False)
                if rc != 0:
                    chef_tries -= 1
                    log.debug('chef-solo failed. %i attempts left' % chef_tries, node)
                else:
                    break

            if chef_tries == 0:
                raise DeploymentException, 'Failed to configure node %s' % node.id
            self.check_continue()
        for cmd in self.deployer.run_cmds:
            rc = ssh.run(cmd, exception_on_error=False)
            if rc != 0:
                log.warning('Extra command failed with status %i: %s' % (rc, cmd), node)

        log.info('Configuration done.', node)

    def configure_stop(self, ssh):
        node = self.node
        log.info('Configuring node for shutdown', node)
        ssh.run('sudo cp /etc/hosts.gp-bak /etc/hosts', expectnooutput=True)
        ssh.run('sudo cp /etc/hostname.gp-bak /etc/hostname', expectnooutput=True)
        ssh.run('sudo /etc/init.d/hostname.sh || sudo /etc/init.d/hostname restart', expectnooutput=True)
        ssh.run('sudo bash -c "echo +auto.master > /etc/auto.master"', exception_on_error=False)
        ssh.run('sudo bash -c "echo > /etc/yp.conf"', exception_on_error=False)
        ssh.run('sudo bash -c "echo > /etc/default/nfs-common"', exception_on_error=False)
        ssh.run('sudo update-rc.d -f nis remove', exception_on_error=False)
        log.info('Configuration done.', node)