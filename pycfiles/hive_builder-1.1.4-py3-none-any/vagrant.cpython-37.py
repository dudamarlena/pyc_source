# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mitsuru/Projects/hive/hive/lib/vagrant.py
# Compiled at: 2019-06-17 10:31:26
# Size of source mod 2**32: 16969 bytes
import vagrant
DOCUMENTATION = '\n---\nmodule: vagrant\nshort_description: create a local instance via vagrant\ndescription:\n     - creates VM instances via vagrant and optionally waits for it to be \'running\'. This module has a dependency on python-vagrant.\nversion_added: "100.0"\noptions:\n  state:\n    description: Should the VMs be "present" or "absent."\n  cmd:\n    description:\n      - vagrant subcommand to execute. Can be "up," "status," "config," "ssh," "halt," "destroy" or "clear."\n    required: false\n    default: null\n    aliases: [\'command\']\n  box_name:\n    description:\n      - vagrant boxed image to start\n    required: false\n    default: null\n    aliases: [\'image\']\n  box_path:\n    description:\n      - path to vagrant boxed image to start\n    required: false\n    default: null\n    aliases: []\n  instaces:\n    description:\n      - list of instance definition dict has inventory_hostname, private_ip\n    required: True\n  forward_ports:\n    description:\n      - comma separated list of ports to forward to the host\n    required: False\n    aliases: []\n  vagrant_dir:\n    description:\n      - directory where vagrant command is executed\n    required: True\n\nexamples:\n   - code: \'local_action: vagrant cmd=up box_name=lucid32 vm_name=webserver\'\n     description:\nrequirements: [ "vagrant" ]\nauthor: Rob Parrott\n'
VAGRANT_FILE = './Vagrantfile'
VAGRANT_DICT_FILE = './Vagrantfile.json'
VAGRANT_LOCKFILE = './.vagrant-lock'
VAGRANT_FILE_HEAD = 'Vagrant::Config.run do |config|\n'
VAGRANT_FILE_BOX_NAME = '  config.vm.box = "%s"\n'
VAGRANT_FILE_VM_STANZA_HEAD = '\n  config.vm.define :%s do |%s_config|\n    %s_config.vm.network :hostonly, "%s"\n    %s_config.vm.box = "%s"\n'
VAGRANT_FILE_HOSTNAME_LINE = '    %s_config.vm.host_name = "%s"\n'
VAGRANT_FILE_PORT_FORWARD_LINE = '    %s_config.vm.forward_port %s, %s\n'
VAGRANT_FILE_VM_STANZA_TAIL = '  end\n'
VAGRANT_FILE_TAIL = '\nend\n'
VAGRANT_INT_IP = '192.168.179.%s'
DEFAULT_VM_NAME = 'ansible'
from ansible.module_utils.basic import AnsibleModule
import sys, subprocess, os.path, json
try:
    import lockfile
except ModuleNotFoundError:
    print('Python module lockfile is not installed. Falling back to using flock(), which will fail on Windows.')

try:
    import vagrant
except ModuleNotFoundError:
    print("failed=True msg='python-vagrant required for this module'")
    sys.exit(1)

class VagrantWrapper(object):

    def __init__(self):
        """
        Wrapper around the python-vagrant module for use with ansible.
        Note that Vagrant itself is non-thread safe, as is the python-vagrant lib, so we need to lock on basically all operations ...
        """
        self.lock = None
        try:
            self.lock = lockfile.FileLock(VAGRANT_LOCKFILE)
            self.lock.acquire()
        except:
            try:
                import fcntl
                self.lock = open(VAGRANT_LOCKFILE, 'w')
                fcntl.flock(self.lock, fcntl.LOCK_EX)
            except:
                print('failed=True msg=\'Could not get a lock for using vagrant. Install python module "lockfile" to use vagrant on non-POSIX filesytems.\'')
                sys.exit(1)

        self.vg = vagrant.Vagrant()
        self._deserialize()
        self._serialize()

    def __del__(self):
        """Clean up file locks"""
        try:
            self.lock.release()
        except:
            os.close(self.lock)
            os.unlink(self.lock)

    def prepare_box(self, box_name, box_path):
        """
        Given a specified name and URL, import a Vagrant "box" for use.
        """
        changed = False
        if box_name == None:
            raise Exception('You must specify a box_name with a box_path for vagrant.')
        boxes = self.vg.box_list()
        if box_name not in boxes:
            self.vg.box_add(box_name, box_path)
            changed = True
        return changed

    def up(self, box_name, instances, box_path=None, ports=[]):
        """
        Fire up a given VM and name it, using vagrant's multi-VM mode.
        """
        changed = False
        if box_name == None:
            raise Exception('You must specify a box name for Vagrant.')
        if box_path != None:
            changed = self.prepare_box(box_name, box_path)
        for instance in instances:
            self._deserialize()
            d = self._get_instance(instance['inventory_hostname'], instance['private_ip'])
            if not d.has_key('box_name'):
                d['box_name'] = box_name
            d['forward_ports'] = ports
            self._instances()[vm_name] = d
            self._serialize()
            vgn = d['vagrant_name']
            status = self.vg.status(vgn)
            if status != 'running':
                self.vg.up(False, d['vagrant_name'])
                changed = True

        ad = self._build_instance_array_for_ansible(vm_name)
        return (changed, ad)

    def status(self, vm_name=None):
        """
        Return the run status of the VM instance. If no instance N is given, returns first instance.
        """
        vm_names = []
        if vm_name != None:
            vm_names = [
             vm_name]
        else:
            vm_names = self._instances().keys()
        statuses = {}
        for vmn in vm_names:
            stat_array = []
            inst = self.vg_data['instances'][vmn]
            vgn = inst['vagrant_name']
            stat_array.append(self.vg.status(vgn))
            statuses[vmn] = stat_array

        return (False, statuses)

    def config(self, vm_name):
        """
        Return info on SSH for the running instance.
        """
        vm_names = []
        if vm_name != None:
            vm_names = [
             vm_name]
        else:
            vm_names = self._instances().keys()
        configs = {}
        for vmn in vm_names:
            inst = self.vg_data['instances'][vmn]
            cnf = self.vg.conf(None, inst['vagrant_name'])
            configs[vmn] = cnf

        return (False, configs)

    def halt(self, vm_name=None):
        """
        Shuts down a vm_name or all VMs.
        """
        changed = False
        vm_names = []
        if vm_name != None:
            vm_names = [
             vm_name]
        else:
            vm_names = self._instances().keys()
        statuses = {}
        for vmn in vm_names:
            inst = self.vg_data['instances'][vmn]
            vgn = inst['vagrant_name']
            if self.vg.status(vgn) == 'running':
                self.vg.halt(vgn)
                changed = True
            statuses[vmn] = self.vg.status(vgn)

        return (changed, statuses)

    def destroy(self, vm_name=None):
        """
        Halt and remove data for a VM, or all VMs.
        """
        self._deserialize()
        changed, stats = self.halt(vm_name, n)
        self.vg.destroy(vm_name)
        if vm_name != None:
            self._instances().pop(vm_name)
        else:
            self.vg_data['instances'] = {}
        self._serialize()
        changed = True
        return changed

    def clear(self, vm_name=None):
        """
        Halt and remove data for a VM, or all VMs. Also clear all state data
        """
        changed = self.vg.destroy(vm_name)
        if os.path.isfile(VAGRANT_FILE):
            os.remove(VAGRANT_FILE)
            changed = True
        if os.path.isfile(VAGRANT_DICT_FILE):
            os.remove(VAGRANT_DICT_FILE)
            changed = True
        return changed

    def _instances(self):
        return self.vg_data['instances']

    def _get_instance(self, vm_name, ip):
        instances = self._instances()
        if instances.has_key(vm_name):
            return instances[vm_name]
        d = dict()
        N = self.vg_data['num_inst'] + 1
        d['N'] = N
        d['name'] = vm_name
        d['vagrant_name'] = vm_name.replace('-', '_')
        d['internal_ip'] = ip
        d['forward_ports'] = []
        self.vg_data['num_inst'] = N
        self._instances()[vm_name] = d
        return d

    def _serialize(self):
        self._save_state()
        self._write_vagrantfile()

    def _deserialize(self):
        self._load_state()

    def _load_state(self):
        self.vg_data = dict(num_inst=0, instances={})
        if os.path.isfile(VAGRANT_DICT_FILE):
            json_file = open(VAGRANT_DICT_FILE)
            self.vg_data = json.load(json_file)
            json_file.close()

    def _state_as_string(self, d):
        from StringIO import StringIO
        io = StringIO()
        json.dump(self.vg_data, io)
        return io.getvalue()

    def _save_state(self):
        json_file = open(VAGRANT_DICT_FILE, 'w')
        json.dump((self.vg_data), json_file, sort_keys=True, indent=4, separators=(',',
                                                                                   ': '))
        json_file.close()

    def _write_vagrantfile(self):
        vfile = open(VAGRANT_FILE, 'w')
        vfile.write(VAGRANT_FILE_HEAD)
        instances = self._instances()
        for vm_name in instances.keys():
            d = instances[vm_name]
            name = d['vagrant_name']
            ip = d['internal_ip']
            box_name = d['box_name']
            vfile.write(VAGRANT_FILE_VM_STANZA_HEAD % (
             name, name, name, ip, name, box_name))
            vfile.write(VAGRANT_FILE_HOSTNAME_LINE % (name, name.replace('_', '-')))
            if d.has_key('forward_ports'):
                for p in d['forward_ports']:
                    vfile.write(VAGRANT_FILE_PORT_FORWARD_LINE % (name, p, p))

            vfile.write(VAGRANT_FILE_VM_STANZA_TAIL)

        vfile.write(VAGRANT_FILE_TAIL)
        vfile.close()

    def _build_instance_array_for_ansible(self, vmname=None):
        vm_names = []
        instances = self._instances()
        if vmname != None:
            vm_names = [
             vmname]
        else:
            vm_names = instances.keys()
        ans_instances = []
        for vm_name in vm_names:
            for inst in instances[vm_name]:
                vagrant_name = inst['vagrant_name']
                cnf = self.vg.conf(None, vagrant_name)
                vg_data = instances[vm_name]
                if cnf != None:
                    d = {'name':vm_name,  'vagrant_name':vagrant_name, 
                     'id':cnf['Host'], 
                     'public_ip':cnf['HostName'], 
                     'internal_ip':inst['internal_ip'], 
                     'public_dns_name':cnf['HostName'], 
                     'port':cnf['Port'], 
                     'username':cnf['User'], 
                     'key':cnf['IdentityFile'], 
                     'status':self.vg.status(vagrant_name)}
                    ans_instances.append(d)

        return ans_instances


def main():
    module = AnsibleModule(argument_spec=dict(state=(dict()),
      cmd=dict(required=False, aliases=['command']),
      box_name=dict(required=False, aliases=['image']),
      box_path=(dict()),
      instances=dict(required=True, type='list', elements='dict'),
      forward_ports=(dict()),
      vagrant_dir=dict(required=True)))
    state = module.params.get('state')
    cmd = module.params.get('cmd')
    box_name = module.params.get('box_name')
    box_path = module.params.get('box_path')
    forward_ports = module.params.get('forward_ports')
    vagrant_dir = module.params.get('vagrant_dir')
    if forward_ports != None:
        forward_ports = forward_ports.split(',')
    if forward_ports == None:
        forward_ports = []
    instances = module.params.get('instances')
    vgw = VagrantWrapper()
    try:
        os.chdir(vagrant_dir)
        if state != None:
            if state != 'present':
                if state != 'absent':
                    module.fail_json(msg='State must be "present" or "absent" in vagrant module.')
            if state == 'present':
                changd, insts = vgw.up(box_name, instances, box_path, forward_ports)
                module.exit_json(changed=changd, instances=insts)
            if state == 'absent':
                changd = vgw.halt(vm_name)
                module.exit_json(changed=changd, status=(vgw.status(vm_name)))
        elif cmd == 'up':
            changd, insts = vgw.up(box_name, instances, box_path, forward_ports)
            module.exit_json(changed=changd, instances=insts)
        else:
            if cmd == 'status':
                changd, result = vgw.status(vm_name)
                module.exit_json(changed=changd, status=result)
            else:
                if cmd == 'config' or cmd == 'conf':
                    if vm_name == None:
                        module.fail_json(msg='Error: you must specify a vm_name when calling config.')
                    changd, cnf = vgw.config(vm_name)
                    module.exit_json(changed=changd, config=cnf)
                else:
                    if cmd == 'ssh':
                        if vm_name == None:
                            module.fail_json(msg='Error: you must specify a vm_name when calling ssh.')
                        changd, cnf = vgw.config(vm_name)
                        sshcmd = 'ssh -i %s -p %s %s@%s' % (cnf['IdentityFile'], cnf['Port'], cnf['User'], cnf['HostName'])
                        sshmsg = 'Execute the command "vagrant ssh %s"' % vm_name
                        module.exit_json(changed=changd, msg=sshmsg, SshCommand=sshcmd)
                    else:
                        if cmd == 'halt':
                            changd, stats = vgw.halt(vm_name)
                            module.exit_json(changed=changd, status=stats)
                        else:
                            if cmd == 'destroy':
                                changd = vgw.destroy(vm_name)
                                module.exit_json(changed=changd, status=(vgw.status(vm_name)))
                            else:
                                if cmd == 'clear':
                                    changd = vgw.clear()
                                    module.exit_json(changed=changd)
                                else:
                                    module.fail_json(msg=('Unknown vagrant subcommand: "%s".' % cmd))
    except subprocess.CalledProcessError as e:
        try:
            module.fail_json(msg=('Vagrant command failed: %s.' % e))
        finally:
            e = None
            del e

    module.exit_json(status='success')