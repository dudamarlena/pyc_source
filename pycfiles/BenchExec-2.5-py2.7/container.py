# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/container.py
# Compiled at: 2019-11-28 13:06:28
"""Utility functions for implementing a container using Linux namespaces
and for appropriately configuring such a container."""
from __future__ import absolute_import, division, print_function, unicode_literals
import contextlib, ctypes, errno, fcntl, logging, os, resource, signal, socket, struct
from benchexec import libc
from benchexec import seccomp
from benchexec import util
__all__ = [
 b'execute_in_namespace',
 b'setup_user_mapping',
 b'activate_network_interface',
 b'duplicate_mount_hierarchy',
 b'determine_directory_mode',
 b'get_mount_points',
 b'remount_with_additional_flags',
 b'make_overlay_mount',
 b'mount_proc',
 b'make_bind_mount',
 b'get_my_pid_from_procfs',
 b'drop_capabilities',
 b'forward_all_signals_async',
 b'wait_for_child_and_forward_signals',
 b'setup_container_system_config',
 b'CONTAINER_UID',
 b'CONTAINER_GID',
 b'CONTAINER_HOME',
 b'CONTAINER_HOSTNAME']
DEFAULT_STACK_SIZE = 1048576
GUARD_PAGE_SIZE = libc.sysconf(libc.SC_PAGESIZE)
CONTAINER_UID = 1000
CONTAINER_GID = 1000
CONTAINER_HOME = b'/home/benchexec'
CONTAINER_HOSTNAME = b'benchexec'
CONTAINER_ETC_NSSWITCH_CONF = b'\npasswd: files\ngroup: files\nshadow: files\nhosts: files\nnetworks: files\n\nprotocols:      db files\nservices:       db files\nethers:         db files\nrpc:            db files\n\nnetgroup:       files\nautomount:      files\n'
CONTAINER_ETC_PASSWD = (b'\nroot:x:0:0:root:/root:/bin/bash\nbenchexec:x:{uid}:{gid}:benchexec:{home}:/bin/bash\nnobody:x:65534:65534:nobody:/:/bin/false\n').format(uid=CONTAINER_UID, gid=CONTAINER_GID, home=CONTAINER_HOME)
CONTAINER_ETC_GROUP = (b'\nroot:x:0:\nbenchexec:x:{gid}:\nnogroup:x:65534:\n').format(uid=CONTAINER_UID, gid=CONTAINER_GID, home=CONTAINER_HOME)
CONTAINER_ETC_HOSTS = (b'\n127.0.0.1       localhost {host}\n# The following lines are desirable for IPv6 capable hosts\n::1     localhost ip6-localhost ip6-loopback\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\n').format(host=CONTAINER_HOSTNAME)
CONTAINER_ETC_FILE_OVERRIDE = {b'nsswitch.conf': CONTAINER_ETC_NSSWITCH_CONF, 
   b'passwd': CONTAINER_ETC_PASSWD, 
   b'group': CONTAINER_ETC_GROUP, 
   b'hostname': CONTAINER_HOSTNAME + b'\n', 
   b'hosts': CONTAINER_ETC_HOSTS}
DIR_HIDDEN = b'hidden'
DIR_READ_ONLY = b'read-only'
DIR_OVERLAY = b'overlay'
DIR_FULL_ACCESS = b'full-access'
DIR_MODES = [DIR_HIDDEN, DIR_READ_ONLY, DIR_OVERLAY, DIR_FULL_ACCESS]
LXCFS_PROC_DIR = b'/var/lib/lxcfs/proc'
if not hasattr(ctypes.pythonapi, b'PyOS_BeforeFork'):
    ctypes.pythonapi.PyOS_BeforeFork = lambda : None
if not hasattr(ctypes.pythonapi, b'PyOS_AfterFork_Parent'):
    ctypes.pythonapi.PyOS_AfterFork_Parent = lambda : None
if not hasattr(ctypes.pythonapi, b'PyOS_AfterFork_Child'):
    ctypes.pythonapi.PyOS_AfterFork_Child = ctypes.pythonapi.PyOS_AfterFork
_CLONE_NESTED_CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int)
NATIVE_CLONE_CALLBACK_SUPPORTED = os.uname()[0] == b'Linux' and os.uname()[4] == b'x86_64'

@contextlib.contextmanager
def allocate_stack(size=DEFAULT_STACK_SIZE):
    """Allocate some memory that can be used as a stack.
    @return: a ctypes void pointer to the *top* of the stack.
    """
    base = libc.mmap_anonymous(size + GUARD_PAGE_SIZE, libc.PROT_READ | libc.PROT_WRITE, libc.MAP_GROWSDOWN | libc.MAP_STACK)
    try:
        libc.mprotect(base, GUARD_PAGE_SIZE, libc.PROT_NONE)
        yield ctypes.c_void_p(base + size + GUARD_PAGE_SIZE)
    finally:
        libc.munmap(base, size + GUARD_PAGE_SIZE)


def execute_in_namespace(func, use_network_ns=True):
    """Execute a function in a child process in separate namespaces.
    @param func: a parameter-less function returning an int
        (which will be the process' exit value)
    @return: the PID of the created child process
    """
    flags = signal.SIGCHLD | libc.CLONE_NEWNS | libc.CLONE_NEWUTS | libc.CLONE_NEWIPC | libc.CLONE_NEWUSER | libc.CLONE_NEWPID
    if use_network_ns:
        flags |= libc.CLONE_NEWNET
    func_p = _CLONE_NESTED_CALLBACK(func)
    with allocate_stack() as (stack):
        try:
            ctypes.pythonapi.PyOS_BeforeFork()
            pid = libc.clone(_clone_child_callback, stack, flags, func_p)
        finally:
            ctypes.pythonapi.PyOS_AfterFork_Parent()

    return pid


@libc.CLONE_CALLBACK
def _python_clone_child_callback(func_p):
    """Used as callback for clone, calls the passed function pointer."""
    ctypes.pythonapi.PyOS_AfterFork_Child()
    return _CLONE_NESTED_CALLBACK(func_p)()


def _generate_native_clone_child_callback():
    """Generate Linux x86_64 machine code
    that does the same as _python_clone_child_callback"""
    page_size = libc.sysconf(libc.SC_PAGESIZE)
    mem = libc.mmap_anonymous(page_size, libc.PROT_READ | libc.PROT_WRITE)
    afterfork_address = struct.pack(b'Q', ctypes.cast(ctypes.pythonapi.PyOS_AfterFork_Child, ctypes.c_void_p).value)
    movabsq_address_rdx = b'H\xba' + afterfork_address
    subq_0x18_rsp = b'H\x83\xec\x18'
    xorl_eax_eax = b'2\xc0'
    movq_rdi_stack = b'H\x89|$\x08'
    callq_rdx = b'\xff\xd2'
    movq_stack_rdi = b'H\x8b|$\x08'
    addq_0x18_rsp = b'H\x83\xc4\x18'
    jmpq_rdi = b'\xff\xe7'
    code = movabsq_address_rdx + subq_0x18_rsp + xorl_eax_eax + movq_rdi_stack + callq_rdx + movq_stack_rdi + xorl_eax_eax + addq_0x18_rsp + jmpq_rdi
    ctypes.memmove(mem, code, len(code))
    libc.mprotect(mem, page_size, libc.PROT_READ | libc.PROT_EXEC)
    return libc.CLONE_CALLBACK(mem)


if NATIVE_CLONE_CALLBACK_SUPPORTED:
    _clone_child_callback = _generate_native_clone_child_callback()
else:
    _clone_child_callback = _python_clone_child_callback

def setup_user_mapping(pid, uid=os.getuid(), gid=os.getgid(), parent_uid=os.getuid(), parent_gid=os.getgid()):
    """Write uid_map and gid_map in /proc to create a user mapping
    that maps our user from outside the container to the same user inside the container
    (and no other users are mapped).
    @see: http://man7.org/linux/man-pages/man7/user_namespaces.7.html
    @param pid: The PID of the process in the container.
    @param uid: The UID that shall be used in the container.
    @param gid: The GID that shall be used in the container.
    @param parent_uid: The UID that is used in the parent namespace.
    @param parent_gid: The GID that is used in the parent namespace.
    """
    proc_child = os.path.join(b'/proc', str(pid))
    try:
        uid_map = (b'{0} {1} 1').format(uid, parent_uid)
        util.write_file(uid_map, proc_child, b'uid_map')
    except IOError as e:
        logging.warning(b'Creating UID mapping into container failed: %s', e)

    try:
        util.write_file(b'deny', proc_child, b'setgroups')
    except IOError as e:
        if e.errno != errno.ENOENT:
            logging.warning(b'Could not write to setgroups file in /proc: %s', e)

    try:
        gid_map = (b'{0} {1} 1').format(gid, parent_gid)
        util.write_file(gid_map, proc_child, b'gid_map')
    except IOError as e:
        logging.warning(b'Creating GID mapping into container failed: %s', e)


_SIOCGIFFLAGS = 35091
_SIOCSIFFLAGS = 35092
_IFF_UP = 1
_STRUCT_IFREQ_LAYOUT_IFADDR_SAFAMILY = b'16sH14s'
_STRUCT_IFREQ_LAYOUT_IFFLAGS = b'16sH14s'

def activate_network_interface(iface):
    """Bring up the given network interface.
    @raise OSError: if interface does not exist or permissions are missing
    """
    iface = iface.encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
    try:
        ifreq = struct.pack(_STRUCT_IFREQ_LAYOUT_IFADDR_SAFAMILY, iface, socket.AF_INET, b'00000000000000')
        ifreq = fcntl.ioctl(sock, _SIOCGIFFLAGS, ifreq)
        if_flags = struct.unpack(_STRUCT_IFREQ_LAYOUT_IFFLAGS, ifreq)[1]
        ifreq = struct.pack(_STRUCT_IFREQ_LAYOUT_IFFLAGS, iface, if_flags | _IFF_UP, b'00000000000000')
        fcntl.ioctl(sock, _SIOCSIFFLAGS, ifreq)
    finally:
        sock.close()


def duplicate_mount_hierarchy(mount_base, temp_base, work_base, dir_modes):
    """
    Setup a copy of the system's mount hierarchy below a specified directory,
    and apply all specified directory modes (e.g., read-only access or hidden)
    in that new hierarchy.
    Afterwards, the new mount hierarchy can be chroot'ed into.
    @param mount_base: the base directory of the new mount hierarchy
    @param temp_base: the base directory for all temporary files
    @param work_base: the base directory for all overlayfs work files
    @param dir_modes: the directory modes to apply (without mount_base prefix)
    """
    make_bind_mount(b'/', mount_base, recursive=True, private=True)
    for special_dir in dir_modes.keys():
        mount_path = mount_base + special_dir
        temp_path = temp_base + special_dir
        try:
            make_bind_mount(mount_path, mount_path)
        except OSError as e:
            if e.errno == errno.EINVAL:
                try:
                    make_bind_mount(mount_path, mount_path, recursive=True)
                except OSError as e2:
                    logging.debug(b'Failed to make %s a (recursive) bind mount: %s', mount_path, e2)

            else:
                logging.debug(b'Failed to make %s a bind mount: %s', mount_path, e)

        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

    for unused_source, full_mountpoint, fstype, options in list(get_mount_points()):
        if not util.path_is_below(full_mountpoint, mount_base):
            continue
        mountpoint = full_mountpoint[len(mount_base):] or b'/'
        mode = determine_directory_mode(dir_modes, mountpoint, fstype)
        if not mode:
            continue
        if not os.access(os.path.dirname(mountpoint), os.X_OK):
            original_mountpoint = mountpoint
            parent = os.path.dirname(mountpoint)
            while not os.access(parent, os.X_OK):
                mountpoint = parent
                parent = os.path.dirname(mountpoint)

            mode = DIR_HIDDEN
            logging.debug(b"Marking inaccessible directory '%s' as hidden because it contains a mountpoint at '%s'", mountpoint.decode(), original_mountpoint.decode())
        else:
            logging.debug(b"Mounting '%s' as %s", mountpoint.decode(), mode)
        mount_path = mount_base + mountpoint
        temp_path = temp_base + mountpoint
        work_path = work_base + mountpoint
        if mode == DIR_OVERLAY:
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)
            if not os.path.exists(work_path):
                os.makedirs(work_path)
            try:
                libc.umount(mount_path)
            except OSError as e:
                logging.debug(e)

            try:
                make_overlay_mount(mount_path, mountpoint, temp_path, work_path)
            except OSError as e:
                mp = mountpoint.decode()
                raise OSError(e.errno, (b"Creating overlay mount for '{}' failed: {}. Please use other directory modes, for example '--read-only-dir {}'.").format(mp, os.strerror(e.errno), util.escape_string_shell(mp)))

        elif mode == DIR_HIDDEN:
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)
            try:
                libc.umount(mount_path)
            except OSError as e:
                logging.debug(e)

            make_bind_mount(temp_path, mount_path)
        elif mode == DIR_READ_ONLY:
            try:
                remount_with_additional_flags(mount_path, options, libc.MS_RDONLY)
            except OSError as e:
                if e.errno == errno.EACCES:
                    logging.warning(b"Cannot mount '%s', directory may be missing from container.", mountpoint.decode())
                else:
                    make_bind_mount(mountpoint, mount_path, recursive=True, private=True)
                    remount_with_additional_flags(mount_path, options, libc.MS_RDONLY)

        elif mode == DIR_FULL_ACCESS:
            try:
                remount_with_additional_flags(mount_path, options, 0)
            except OSError as e:
                if e.errno == errno.EACCES:
                    logging.warning(b"Cannot mount '%s', directory may be missing from container.", mountpoint.decode())
                else:
                    make_bind_mount(mountpoint, mount_path, recursive=True, private=True)

        elif not False:
            raise AssertionError


def determine_directory_mode(dir_modes, path, fstype=None):
    """
    From a high-level mapping of desired directory modes, determine the actual mode
    for a given directory.
    """
    if fstype == b'proc':
        return DIR_READ_ONLY
    else:
        if util.path_is_below(path, b'/proc'):
            return
        parent_mode = None
        result_mode = None
        for special_dir, mode in dir_modes.items():
            if util.path_is_below(path, special_dir):
                if path != special_dir:
                    parent_mode = mode
                result_mode = mode

        assert result_mode is not None
        if result_mode == DIR_OVERLAY and (util.path_is_below(path, b'/dev') or util.path_is_below(path, b'/sys') or fstype == b'fuse.lxcfs' or fstype == b'cgroup'):
            return DIR_READ_ONLY
        if result_mode == DIR_OVERLAY and fstype and (fstype.startswith(b'fuse.') or fstype == b'autofs' or fstype == b'vfat' or fstype == b'ntfs'):
            logging.debug(b'Cannot use overlay mode for %s because it has file system %s. Using read-only mode instead. You can override this by specifying a different directory mode.', path.decode(), fstype.decode())
            return DIR_READ_ONLY
        if result_mode == DIR_HIDDEN and parent_mode == DIR_HIDDEN:
            return
        return result_mode


def get_mount_points():
    """Get all current mount points of the system.
    Changes to the mount points during iteration may be reflected in the result.
    @return a generator of (source, target, fstype, options),
    where options is a list of bytes instances, and the others are bytes instances
    (this avoids encoding problems with mount points with problematic characters).
    """

    def decode_path(path):
        return path.replace(b'\\011', b'\t').replace(b'\\040', b' ').replace(b'\\012', b'\n').replace(b'\\134', b'\\')

    with open(b'/proc/self/mounts', b'rb') as (mounts):
        for mount in mounts:
            source, target, fstype, options, unused1, unused2 = mount.split(b' ')
            options = set(options.split(b','))
            yield (decode_path(source), decode_path(target), fstype, options)


def remount_with_additional_flags(mountpoint, existing_options, mountflags):
    """Remount an existing mount point with additional flags.
    @param mountpoint: the mount point as bytes
    @param existing_options: dict with current mount existing_options as bytes
    @param mountflags: int with additional mount existing_options
        (cf. libc.MS_* constants)
    """
    mountflags |= libc.MS_REMOUNT | libc.MS_BIND
    for option, flag in libc.MOUNT_FLAGS.items():
        if option in existing_options:
            mountflags |= flag

    libc.mount(None, mountpoint, None, mountflags, None)
    return


def make_overlay_mount(mount, lower, upper, work):
    logging.debug(b'Creating overlay mount: target=%s, lower=%s, upper=%s, work=%s', mount, lower, upper, work)
    libc.mount(b'none', mount, b'overlay', 0, b'lowerdir=' + lower + b',upperdir=' + upper + b',workdir=' + work)


def mount_proc(container_system_config):
    """Mount the /proc filesystem.
    @param container_system_config: Whether to mount container-specific files in /proc
    """
    libc.mount(b'proc', b'/proc', b'proc', 0, None)
    if container_system_config and os.access(LXCFS_PROC_DIR, os.R_OK):
        for f in os.listdir(LXCFS_PROC_DIR):
            make_bind_mount(os.path.join(LXCFS_PROC_DIR, f), os.path.join(b'/proc', f), private=True)

        libc.mount(b'proc', b'/proc/1/ns', b'proc', 0, None)
    return


def make_bind_mount(source, target, recursive=False, private=False, read_only=False):
    """Make a bind mount.
    @param source: the source directory as bytes
    @param target: the target directory as bytes
    @param recursive: whether to also recursively bind mount all mounts below source
    @param private: whether to mark the bind as private,
        i.e., changes to the existing mounts won't propagate and vice-versa
        (changes to files/dirs will still be visible).
    """
    flags = libc.MS_BIND
    if recursive:
        flags |= libc.MS_REC
    if private:
        flags |= libc.MS_PRIVATE
    if read_only:
        flags |= libc.MS_RDONLY
    libc.mount(source, target, None, flags, None)
    return


def chroot(target):
    """
    Chroot into a target directory. This also affects the working directory, make sure
    to call os.chdir() afterwards.
    """
    os.chdir(target)
    libc.pivot_root(b'.', b'.')
    libc.umount2(b'/', libc.MNT_DETACH)


def get_my_pid_from_procfs():
    """
    Get the PID of this process by reading from /proc (this is the PID of this process
    in the namespace in which that /proc instance has originally been mounted),
    which may be different from our PID according to os.getpid().
    """
    return int(os.readlink(b'/proc/self'))


def drop_capabilities(keep=[]):
    """
    Drop all capabilities this process has.
    @param keep: list of capabilities to not drop
    """
    capdata = (libc.CapData * 2)()
    for cap in keep:
        capdata[0].effective |= 1 << cap
        capdata[0].permitted |= 1 << cap

    libc.capset(ctypes.byref(libc.CapHeader(version=libc.LINUX_CAPABILITY_VERSION_3, pid=0)), ctypes.byref(capdata))


_FORBIDDEN_SYSCALLS = [
 b'add_key',
 b'request_key',
 b'keyctl',
 b'userfaultfd']

def setup_seccomp_filter():
    if not seccomp.is_available():
        return
    try:
        with seccomp.SeccompFilter() as (s):
            for syscall in _FORBIDDEN_SYSCALLS:
                s.add_rule(seccomp.SCMP_ACT_ENOSYS, syscall)

            s.activate()
    except OSError as e:
        logging.info(b'Could not enable seccomp filter for container isolation: %s', e)


try:
    _ALL_SIGNALS = signal.valid_signals()
except AttributeError:
    _ALL_SIGNALS = range(1, signal.NSIG)

_FORWARDABLE_SIGNALS = set(range(1, 32)).difference([
 signal.SIGKILL, signal.SIGSTOP, signal.SIGCHLD])
_HAS_SIGWAIT = hasattr(signal, b'sigwait')

def block_all_signals():
    """Block asynchronous delivery of all signals to this process."""
    if _HAS_SIGWAIT:
        signal.pthread_sigmask(signal.SIG_BLOCK, _ALL_SIGNALS)


def _forward_signal(signum, target_pid, process_name):
    logging.debug(b'Forwarding signal %d to process %s.', signum, process_name)
    try:
        os.kill(target_pid, signum)
    except OSError as e:
        logging.debug(b'Could not forward signal %d to process %s: %s', signum, process_name, e)


def forward_all_signals_async(target_pid, process_name):
    """Install all signal handler that forwards all signals to the given process."""

    def forwarding_signal_handler(signum):
        _forward_signal(signum, forwarding_signal_handler.target_pid, process_name)

    forwarding_signal_handler.target_pid = target_pid
    for signum in _FORWARDABLE_SIGNALS:
        libc.signal(signum, forwarding_signal_handler)

    reset_signal_handling()


def wait_for_child_and_forward_signals(child_pid, process_name):
    """Wait for a child to terminate and in the meantime forward all signals
    that the current process receives to this child.
    @return a tuple of exit code and resource usage of the child as given by os.waitpid
    """
    assert _HAS_SIGWAIT
    block_all_signals()
    while True:
        logging.debug(b'Waiting for signals')
        signum = signal.sigwait(_ALL_SIGNALS)
        if signum == signal.SIGCHLD:
            pid, exitcode, ru_child = os.wait4(-1, os.WNOHANG)
            while pid != 0:
                if pid == child_pid:
                    return (exitcode, ru_child)
                logging.debug(b'Received unexpected SIGCHLD for PID %s', pid)
                pid, exitcode, ru_child = os.wait4(-1, os.WNOHANG)

        else:
            _forward_signal(signum, child_pid, process_name)


def reset_signal_handling():
    if _HAS_SIGWAIT:
        signal.pthread_sigmask(signal.SIG_SETMASK, {})


def close_open_fds(keep_files=[]):
    """Close all open file descriptors except those in a given set.
    @param keep_files: an iterable of file descriptors or file-like objects.
    """
    keep_fds = set()
    for file in keep_files:
        if isinstance(file, int):
            keep_fds.add(file)
        else:
            try:
                keep_fds.add(file.fileno())
            except Exception:
                pass

    for fd in os.listdir(b'/proc/self/fd'):
        fd = int(fd)
        if fd not in keep_fds:
            try:
                os.close(fd)
            except OSError:
                pass


def setup_container_system_config(basedir, mountdir, dir_modes):
    """Create a minimal system configuration for use in a container.
    @param basedir: The directory where the configuration files should be placed (bytes)
    @param mountdir: The base directory of the mount hierarchy in the container (bytes).
    @param dir_modes: All directory modes in the container.
    """
    symlinks_required = determine_directory_mode(dir_modes, b'/etc') != DIR_OVERLAY
    etc = os.path.join(basedir, b'etc')
    if not os.path.exists(etc):
        os.mkdir(etc)
    for file, content in CONTAINER_ETC_FILE_OVERRIDE.items():
        util.write_file(content, etc, file)
        if symlinks_required:
            make_bind_mount(os.path.join(etc, file), os.path.join(mountdir, b'etc', file), private=True)

    os.symlink(b'/proc/self/mounts', os.path.join(etc, b'mtab'))
    if not os.path.isdir(mountdir.decode() + CONTAINER_HOME):
        logging.warning(b"Home directory in container should be %(h)s but this directory cannot be created due to directory mode of parent directory. It is recommended to use '--overlay-dir %(p)s' or '--hidden-dir %(p)s' and overwrite directory modes for subdirectories where necessary.", {b'h': CONTAINER_HOME, b'p': os.path.dirname(CONTAINER_HOME)})


def is_container_system_config_file(file):
    """Determine whether a given file is one of the files created by
    setup_container_system_config().
    @param file: Absolute file path as string.
    """
    if not file.startswith(b'/etc/'):
        return False
    return file in [ os.path.join(b'/etc', f.decode()) for f in CONTAINER_ETC_FILE_OVERRIDE ]