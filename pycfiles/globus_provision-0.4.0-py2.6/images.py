# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/deploy/ec2/images.py
# Compiled at: 2012-03-02 22:17:19
from boto.exception import EC2ResponseError
from globus.provision.core.deploy import DeploymentException
from globus.provision.common.utils import create_ec2_connection
from globus.provision.common.ssh import SSH
from globus.provision.common import log
import time

class EC2AMICreator(object):
    """
    Used to create a Globus Provision AMI.
    """

    def __init__(self, chef_dir, base_ami, ami_name, instance_type, security_groups, config):
        self.chef_dir = chef_dir
        self.base_ami = base_ami
        self.ami_name = ami_name
        self.instance_type = instance_type
        self.security_groups = security_groups
        self.config = config
        self.keypair = config.get('ec2-keypair')
        self.keyfile = config.get('ec2-keyfile')
        self.hostname = config.get('ec2-server-hostname')
        self.port = config.get('ec2-server-port')
        self.path = config.get('ec2-server-path')
        self.username = config.get('ec2-username')
        self.scratch_dir = config.get('scratch-dir')

    def run(self):
        log.init_logging(2)
        conn = create_ec2_connection(hostname=self.hostname, path=self.path, port=self.port)
        if conn == None:
            raise DeploymentException, 'AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are not set.'
        print 'Creating instance'
        reservation = conn.run_instances(self.base_ami, min_count=1, max_count=1, instance_type=self.instance_type, security_groups=self.security_groups, key_name=self.keypair)
        instance = reservation.instances[0]
        print 'Instance %s created. Waiting for it to start...' % instance.id
        while True:
            try:
                newstate = instance.update()
                if newstate == 'running':
                    break
                time.sleep(2)
            except EC2ResponseError, ec2err:
                if ec2err.error_code == 'InvalidInstanceID.NotFound':
                    pass
                else:
                    raise ec2err

        print 'Instance running'
        print self.username, instance.public_dns_name, self.keyfile
        ssh = SSH(self.username, instance.public_dns_name, self.keyfile, None, None)
        try:
            ssh.open()
        except Exception, e:
            print e.message
            exit(1)

        print 'Copying Chef files'
        ssh.run('sudo mkdir /chef')
        ssh.run('sudo chown -R %s /chef' % self.username)
        ssh.scp_dir('%s' % self.chef_dir, '/chef')
        ssh.run('echo "%s `hostname`" | sudo tee -a /etc/hosts' % instance.private_ip_address)
        ssh.run('sudo apt-get install lsb-release wget')
        ssh.run('echo "deb http://apt.opscode.com/ `lsb_release -cs` main" | sudo tee /etc/apt/sources.list.d/opscode.list')
        ssh.run('wget -qO - http://apt.opscode.com/packages@opscode.com.gpg.key | sudo apt-key add -')
        ssh.run('sudo apt-get update')
        ssh.run("echo 'chef chef/chef_server_url string http://127.0.0.1:4000' | sudo debconf-set-selections")
        ssh.run('sudo apt-get -q=2 install chef')
        ssh.run('sudo apt-get dist-upgrade -uy')
        ssh.run('echo -e "cookbook_path \\"/chef/cookbooks\\"\\nrole_path \\"/chef/roles\\"" > /tmp/chef.conf')
        ssh.run('echo \'{ "run_list": "recipe[provision::ec2]", "scratch_dir": "%s" }\' > /tmp/chef.json' % self.scratch_dir)
        ssh.run('sudo chef-solo -c /tmp/chef.conf -j /tmp/chef.json')
        ssh.run('sudo update-rc.d -f chef-client remove')
        print 'Removing private data and authorized keys'
        ssh.run('sudo find /root/.*history /home/*/.*history -exec rm -f {} \\;', exception_on_error=False)
        ssh.run('sudo find / -name authorized_keys -exec rm -f {} \\;', exception_on_error=False)
        print 'Stopping instance'
        conn.stop_instances([instance.id])
        while instance.update() != 'stopped':
            time.sleep(2)

        print 'Instance stopped'
        print 'Creating AMI'
        ami = conn.create_image(instance.id, self.ami_name, description=self.ami_name)
        print 'Cleaning up'
        print 'Terminating instance'
        print 'Instance terminated'
        return


class EC2AMIUpdater(object):
    """
    Used to update a Globus Provision AMI.
    """

    def __init__(self, base_ami, ami_name, files, config):
        self.base_ami = base_ami
        self.ami_name = ami_name
        self.files = files
        self.config = config
        self.keypair = config.get('ec2-keypair')
        self.keyfile = config.get('ec2-keyfile')
        self.hostname = config.get('ec2-server-hostname')
        self.port = config.get('ec2-server-port')
        self.path = config.get('ec2-server-path')
        self.username = config.get('ec2-username')

    def run(self):
        log.init_logging(2)
        conn = create_ec2_connection(hostname=self.hostname, path=self.path, port=self.port)
        print 'Creating instance'
        reservation = conn.run_instances(self.base_ami, min_count=1, max_count=1, instance_type='m1.small', key_name=self.keypair)
        instance = reservation.instances[0]
        print 'Instance %s created. Waiting for it to start...' % instance.id
        while instance.update() != 'running':
            time.sleep(2)

        print 'Instance running.'
        print 'Opening SSH connection.'
        ssh = SSH(self.username, instance.public_dns_name, self.keyfile)
        ssh.open()
        print 'Copying files'
        for (src, dst) in self.files:
            ssh.scp(src, dst)

        print 'Removing private data and authorized keys'
        ssh.run('sudo find /root/.*history /home/*/.*history -exec rm -f {} \\;', exception_on_error=False)
        ssh.run('sudo find / -name authorized_keys -exec rm -f {} \\;', exception_on_error=False)
        print 'Stopping instance'
        conn.stop_instances([instance.id])
        while instance.update() != 'stopped':
            time.sleep(2)

        print 'Instance stopped'
        print 'Creating AMI'
        ami = conn.create_image(instance.id, self.ami_name, description=self.ami_name)
        if ami != None:
            print ami
        print 'Cleaning up'
        print 'Terminating instance'
        conn.terminate_instances([instance.id])
        while instance.update() != 'terminated':
            time.sleep(2)

        print 'Instance terminated'
        return