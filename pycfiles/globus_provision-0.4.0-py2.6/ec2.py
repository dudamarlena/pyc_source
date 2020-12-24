# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/cli/ec2.py
# Compiled at: 2012-03-02 22:17:19
"""
Commands related to the EC2 deployer, but which do not require access to the API
"""
import sys, os.path
from globus.provision.cli import Command
from globus.provision.deploy.ec2.images import EC2AMICreator, EC2AMIUpdater
from globus.provision.common import defaults
from globus.provision.core.config import GPConfig
from globus.provision.common.utils import parse_extra_files_files

def gp_ec2_create_ami_func():
    return gp_ec2_create_ami(sys.argv).run()


class gp_ec2_create_ami(Command):
    """
    Creates a Globus Provision AMI with Chef files pre-deployed, and
    some software pre-installed.            
    """
    name = 'gp-ec2-create-ami'

    def __init__(self, argv):
        Command.__init__(self, argv)
        self.optparser.add_option('-s', '--chef-directory', action='store', type='string', dest='chef_dir', help='Location of Chef files.')
        self.optparser.add_option('-c', '--conf', action='store', type='string', dest='conf', default=defaults.CONFIG_FILE, help='Configuration file. Must include an [ec2] section.')
        self.optparser.add_option('-a', '--ami', action='store', type='string', dest='ami', help='AMI to base the new AMI on.')
        self.optparser.add_option('-n', '--name', action='store', type='string', dest='aminame', help='Name of AMI to create')
        self.optparser.add_option('-t', '--instance-type', action='store', type='string', dest='instance_type', help='EC2 instance type to use')
        self.optparser.add_option('-g', '--security-groups', action='store', type='string', dest='security_groups', help='EC2 security groups to use (comma separated)')

    def run(self):
        self.parse_options()
        config = GPConfig(os.path.expanduser(self.opt.conf))
        chef_dir = os.path.expanduser(self.opt.chef_dir)
        if self.opt.security_groups == None:
            sg = None
        else:
            sg = self.opt.security_groups.split(',')
        c = EC2AMICreator(chef_dir, self.opt.ami, self.opt.aminame, self.opt.instance_type, sg, config)
        c.run()
        return


def gp_ec2_update_ami_func():
    return gp_ec2_update_ami(sys.argv).run()


class gp_ec2_update_ami(Command):
    """
    Takes an existing AMI, adds files to it, and creates a new AMI.
    """
    name = 'gp-ec2-update-ami'

    def __init__(self, argv):
        Command.__init__(self, argv)
        self.optparser.add_option('-a', '--ami', action='store', type='string', dest='ami', help='AMI to update.')
        self.optparser.add_option('-n', '--name', action='store', type='string', dest='aminame', help='Name of new AMI.')
        self.optparser.add_option('-c', '--conf', action='store', type='string', dest='conf', default=defaults.CONFIG_FILE, help='Configuration file. Must include an [ec2] section.')
        self.optparser.add_option('-f', '--files', action='store', type='string', dest='files', help='Files to add to AMI')

    def run(self):
        self.parse_options()
        files = parse_extra_files_files(self.opt.files)
        config = GPConfig(os.path.expanduser(self.opt.conf))
        c = EC2AMIUpdater(self.opt.ami, self.opt.aminame, files, config)
        c.run()