# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/cli/globusonline.py
# Compiled at: 2011-09-13 11:00:44
"""
Commands related to Globus Online endpoint management, but which do not require access to the API
"""
import sys, os.path, paramiko
from globus.provision.common.ssh import SSH
from globus.provision.cli import Command
from globus.provision.core.instance import InstanceStore
from globus.provision.common.go_transfer import GlobusOnlineHelper

def gp_go_register_endpoints_func():
    return gp_go_register_endpoints(sys.argv).run()


class gp_go_register_endpoints(Command):
    """
    Creates the Globus Online endpoints specified in an instance's topology.
    
    The instance identifier must be specified after all other parameters. For example::
    
        gp-go-register-endpoints --public gpi-12345678    
    """
    name = 'gp-go-register-endpoints'

    def __init__(self, argv):
        Command.__init__(self, argv)
        self.optparser.add_option('-m', '--domain', action='store', type='string', dest='domain', help='Register only the endpoints in this domain')
        self.optparser.add_option('-r', '--replace', action='store_true', dest='replace', help='If an endpoint already exists, replace it')

    def run(self):
        self.parse_options()
        inst_id = self.args[1]
        istore = InstanceStore(self.opt.dir)
        inst = istore.get_instance(inst_id)
        go_helper = GlobusOnlineHelper.from_instance(inst)
        for (domain_name, domain) in inst.topology.domains.items():
            for ep in domain.go_endpoints:
                go_helper.connect(ep.user)
                if not ep.has_property('globus_connect_cert') or ep.has_property('globus_connect_cert') and not ep.globus_connect_cert:
                    go_helper.create_endpoint(ep, self.opt.replace)
                go_helper.disconnect()
                print "Created endpoint '%s#%s' for domain '%s'" % (ep.user, ep.name, domain_name)