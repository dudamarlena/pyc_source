# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/virtualmachine/lxc.py
# Compiled at: 2013-08-03 03:24:10
from abstract import AbstractVirtualMachine
from ..exceptions import VMException
import lxc, os.path, shutil, ipaddr

def convert_ip_netmask_to_cidr(ip, netmask):
    return str(ipaddr.IPv4Network('%s/%s' % (ip, netmask)))


def create_lxc_config(configfile, rootfs, name, ip, netmask, hwaddr, bridge='br0', ram=1024):
    cidr = convert_ip_netmask_to_cidr(ip, netmask)
    fd = open(configfile, 'w')
    try:
        fd.write('# auto-generated config for ' + name + '\nlxc.network.type=veth\nlxc.network.link=%(bridge)s\nlxc.network.flags=up\nlxc.network.hwaddr=%(hwaddr)s\nlxc.network.ipv4=%(cidr)s\nlxc.cap.drop = sys_module mac_admin\nlxc.tty = 1\nlxc.pts = 1024\nlxc.rootfs = %(rootfs)s\nlxc.cgroup.memory.limit_in_bytes = %(ram)dM\nlxc.utsname = %(name)s\nlxc.cgroup.devices.deny = a\n# /dev/null and zero\nlxc.cgroup.devices.allow = c 1:3 rwm\nlxc.cgroup.devices.allow = c 1:5 rwm\n# consoles\nlxc.cgroup.devices.allow = c 5:1 rwm\nlxc.cgroup.devices.allow = c 5:0 rwm\nlxc.cgroup.devices.allow = c 4:0 rwm\nlxc.cgroup.devices.allow = c 4:1 rwm\n# /dev/{,u}random\nlxc.cgroup.devices.allow = c 1:9 rwm\nlxc.cgroup.devices.allow = c 1:8 rwm\nlxc.cgroup.devices.allow = c 136:* rwm\nlxc.cgroup.devices.allow = c 5:2 rwm\n# tun\nlxc.cgroup.devices.allow = c 10:200 rwm\n# rtc\nlxc.cgroup.devices.allow = c 254:0 rwm\n\n# mount points\nlxc.mount.entry=proc %(rootfs)s/proc proc nodev,noexec,nosuid 0 0\nlxc.mount.entry=sysfs %(rootfs)s/sys sysfs defaults  0 0\n' % locals())
    finally:
        fd.close()


def unpack_lxc_rootfs(rootfs, name, targz):
    """Called to install the rootfs"""
    if not os.path.isdir(rootfs):
        os.mkdir(rootfs)
    os.system("tar -C '%s' -xzpsSf '%s'" % (rootfs, targz))


def unpack_lxc_overlay(rootfs, name, targz):
    """Called to install another tarball over the first one"""
    if not os.path.exists(targz):
        return
    os.system("tar -C '%s' -xzpsSf '%s'" % (rootfs, targz))


def posix_quote(string):
    return ("\\'").join("'" + p + "'" for p in string.split("'"))


def create_firstboot_config(rootfs, name, ip, netmask, gateway, metadata=None):
    firstboot = os.path.join(rootfs, 'etc/firstboot.config')
    fd = open(firstboot, 'w')
    try:
        fd.write('NAME="%s"\n' % (name,))
        fd.write('IPADDRESS="%s"\n' % (ip,))
        fd.write('NETMASK="%s"\n' % (netmask,))
        fd.write('GATEWAY="%s"\n' % (gateway,))
        if metadata:
            for k, v in metadata.items():
                fd.write('%s=%s\n' % (k, posix_quote(v)))

    finally:
        fd.close()


def cleanup_lxc(config_directory, rootfs):
    """Remove config directory and the .hold lockfile if it exists"""
    if os.path.isdir(config_directory):
        shutil.rmtree(config_directory)
    if os.path.exists(rootfs + '.hold'):
        os.unlink(rootfs + '.hold')


class LXCVirtualMachine(AbstractVirtualMachine):

    def _get_config_directory(self):
        """Directory for the config file for this LXC container"""
        config_directory_prefix = self.config.get('config_directory_prefix', '/var/lib/lxc')
        return os.path.join(config_directory_prefix, self.get_name())

    def _get_rootfs_directory(self):
        """Directory for the rootfs of this LXC container"""
        default_rootfs_prefix = self.config.get('default_rootfs_prefix', None)
        rootfs = None
        if self.storage_volumes and len(self.storage_volumes) > 0:
            storage = self.storage_volumes[0]
            rootfs = storage.get_directory()
        if rootfs is None and default_rootfs_prefix:
            rootfs = os.path.join(default_rootfs_prefix, self.get_name(), 'rootfs')
        if rootfs is None:
            raise VMException("storage plugin doesn't support get_directory(), and vms.${vm_type}.default_rootfs_prefix was not set in configuration file")
        return rootfs

    def _define(self):
        name = self.get_name()
        template_path = self.config.get('template_path', '/var/lib/lxc/templates')
        template = self.definition['template']
        targz = os.path.join('%s/%s.tar.gz' % (template_path, template))
        overlay_targz = os.path.join('%s/overlay/%s.tar.gz' % (template_path, template))
        try:
            network = self.definition.get('network')
            eth0 = network[0]
            ip = eth0['ipaddr']
            netmask = eth0['netmask']
            gateway = eth0['gateway']
            hwaddr = eth0['hwaddr']
            bridge = eth0['bridge']
        except KeyError as IndexError:
            raise VMException('Missing or incomplete network definition')

        ram = self.definition.get('ram', 1024)
        rootfs = self._get_rootfs_directory()
        config_directory_prefix = self.config.get('config_directory_prefix', '/var/lib/lxc')
        confdir = os.path.join(config_directory_prefix, self.get_name())
        conffile = os.path.join(confdir, 'config')
        if not os.path.exists(confdir):
            os.mkdir(confdir)
        create_lxc_config(conffile, rootfs, name, ip, netmask, hwaddr, ram=ram, bridge=bridge)
        hostnamefile = os.path.join(rootfs, 'etc/hostname')
        if not os.path.exists(hostnamefile):
            unpack_lxc_rootfs(rootfs, name, targz)
            unpack_lxc_overlay(rootfs, name, overlay_targz)
            create_firstboot_config(rootfs, name, ip, '255.255.255.0', '192.168.1.1', metadata=self.definition.get('metadata', None))
        fd = open(hostnamefile, 'w')
        try:
            fd.write(name + '\n')
        finally:
            fd.close()

        return

    def _lxc_bin_path(self):
        return self.config.get('lxc_bin_path', '/usr/bin')

    def _cgroup_path(self):
        return self.config.get('cgroup_path', '/cgroup')

    def _start(self):
        os.system('%s/lxc-start -d -n %s' % (self._lxc_bin_path(), self.name))

    def _stop(self):
        os.system('%s/lxc-stop -n %s' % (self._lxc_bin_path(), self.name))

    def _shutdown(self):
        os.system('%s/lxc-stop -n %s' % (self._lxc_bin_path(), self.name))

    def _undefine(self):
        transient = self.definition.get('transient', False)
        config_directory = self._get_config_directory()
        rootfs = self._get_rootfs_directory()
        if transient:
            if os.path.exists(rootfs):
                shutil.rmtree(rootfs)
        cleanup_lxc(config_directory, rootfs)

    def deprovision(self):
        self.undefine()
        with self._lock:
            rootfs = self._get_rootfs_directory()
            if os.path.exists(rootfs):
                shutil.rmtree(rootfs)

    def get_substate(self):
        return getattr(self, 'substate', None)

    def get_state(self):
        if os.path.exists(os.path.join(self._cgroup_path(), 'cpu.shares')) and os.path.isdir(os.path.join(self._cgroup_path(), self.name)):
            return (
             'running', self.get_substate() or 'running')
        if os.path.isdir(os.path.join(self._cgroup_path(), 'cpu/lxc', self.name)):
            return (
             'running', self.get_substate() or 'running')
        return ('stopped', self.get_substate() or 'stopped')

    def get_cpu_usage(self):
        return 1

    def get_memory_usage(self):
        fmemusage = os.path.join(self._cgroup_path(), 'memory/lxc', self.get_name(), 'memory.usage_in_bytes')
        if os.path.exists(fmemusage):
            with open(fmemusage, 'rb') as (fd):
                return int(int(fd.read()) / 1024.0 / 1024.0)
        return -1

    def get_primary_ip(self):
        """Used by command line vmctl client"""
        if 'network' not in self.definition:
            return
        else:
            network = self.definition['network']
            if type(network) != list or len(network) < 1:
                return
            if network[0].get('name', None) != 'eth0':
                return
            return network[0].get('ipaddr', None)

    def get_console_command(self):
        """Used by command line vmctl client"""
        return ('lxc-console --name {0}').format(self.get_name())

    def is_locked(self):
        lockfile = self._get_rootfs_directory() + '.locked'
        return os.path.exists(lockfile)

    def lock(self):
        lockfile = self._get_rootfs_directory() + '.locked'
        if not os.path.exists(lockfile):
            with open(lockfile, 'w') as (fd):
                fd.write('VM has been marked as locked down.\n')

    def unlock(self):
        lockfile = self._get_rootfs_directory() + '.locked'
        if os.path.exists(lockfile):
            os.unlink(lockfile)