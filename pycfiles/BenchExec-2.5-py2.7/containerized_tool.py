# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/containerized_tool.py
# Compiled at: 2019-11-28 13:06:28
import collections, contextlib, errno, functools, inspect, logging, multiprocessing, os, signal, tempfile
from benchexec import BenchExecException, container, containerexecutor, libc, util
import benchexec.tools.template

class ContainerizedTool(benchexec.tools.template.BaseTool):
    """Wrapper for an instance of any subclass of benchexec.tools.template.BaseTool.
    The module and the subclass instance will be loaded in a subprocess that has been
    put into a container. This means, for example, that the code of this module cannot
    make network connections and that any changes made to files on disk have no effect.
    """

    def __init__(self, tool_module, config):
        """Load tool-info module in subprocess.
        @param tool_module: The name of the module to load.
            Needs to define class named Tool.
        @param config: A config object suitable for
            benchexec.containerexecutor.handle_basic_container_args()
        """
        self._pool = multiprocessing.Pool(1, _init_worker_process)
        container_options = containerexecutor.handle_basic_container_args(config)
        temp_dir = tempfile.mkdtemp(prefix='Benchexec_tool_info_container_')
        try:
            try:
                self.__doc__ = self._pool.apply(_init_container_and_load_tool, [
                 tool_module, temp_dir], container_options)
            except BaseException as e:
                self._pool.terminate()
                raise e

        finally:
            with contextlib.suppress(OSError):
                os.rmdir(temp_dir)

    def close(self):
        self._pool.close()

    def _forward_call(self, method_name, args, kwargs):
        """Call given method indirectly on the tool instance in the container."""
        return self._pool.apply(_call_tool_func, [method_name, list(args), kwargs])

    @classmethod
    def _add_proxy_function(cls, method_name, method):
        """Add function to given class that calls the specified method indirectly."""

        @functools.wraps(method)
        def proxy_function(self, *args, **kwargs):
            return self._forward_call(method_name, args, kwargs)

        setattr(cls, member_name, proxy_function)


for member_name, member in inspect.getmembers(ContainerizedTool, inspect.isfunction):
    if member_name[0] == '_' or member_name == 'close':
        continue
    ContainerizedTool._add_proxy_function(member_name, member)

def _init_worker_process():
    """Initial setup of worker process from multiprocessing module."""
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def _init_container_and_load_tool(tool_module, *args, **kwargs):
    """Initialize container for the current process and load given tool-info module."""
    try:
        _init_container(*args, **kwargs)
    except EnvironmentError as e:
        raise BenchExecException('Failed to configure container: ' + str(e))

    return _load_tool(tool_module)


def _init_container(temp_dir, network_access, dir_modes, container_system_config, container_tmpfs):
    """
    Create a fork of this process in a container. This method only returns in the fork,
    so calling it seems like moving the current process into a container.
    """
    if container_system_config:
        dir_modes.setdefault(container.CONTAINER_HOME, container.DIR_HIDDEN)
        os.environ['HOME'] = container.CONTAINER_HOME
    temp_dir = temp_dir.encode()
    dir_modes = collections.OrderedDict(sorted(((path.encode(), kind) for path, kind in dir_modes.items()), key=lambda tupl: len(tupl[0])))
    uid = container.CONTAINER_UID if container_system_config else os.getuid()
    gid = container.CONTAINER_GID if container_system_config else os.getgid()
    flags = libc.CLONE_NEWNS | libc.CLONE_NEWUTS | libc.CLONE_NEWIPC | libc.CLONE_NEWUSER | libc.CLONE_NEWPID
    if not network_access:
        flags |= libc.CLONE_NEWNET
    try:
        libc.unshare(flags)
    except OSError as e:
        if e.errno == errno.EPERM and util.try_read_file('/proc/sys/kernel/unprivileged_userns_clone') == '0':
            raise BenchExecException("Unprivileged user namespaces forbidden on this system, please enable them with 'sysctl kernel.unprivileged_userns_clone=1' or disable container mode")
        else:
            raise BenchExecException('Creating namespace for container mode failed: ' + os.strerror(e.errno))

    container.setup_user_mapping(os.getpid(), uid, gid)
    _setup_container_filesystem(temp_dir, dir_modes, container_system_config)
    if container_system_config:
        libc.sethostname(container.CONTAINER_HOSTNAME)
    if not network_access:
        container.activate_network_interface('lo')
    pid = os.fork()
    if pid:
        container.drop_capabilities()
        os.waitpid(pid, 0)
        os._exit(0)
    container.mount_proc(container_system_config)
    container.drop_capabilities()
    libc.prctl(libc.PR_SET_DUMPABLE, libc.SUID_DUMP_DISABLE, 0, 0, 0)
    container.setup_seccomp_filter()


def _load_tool(tool_module):
    global tool
    logging.debug('Loading tool-info module %s in container', tool_module)
    tool = __import__(tool_module, fromlist=['Tool']).Tool()
    return tool.__doc__


def _setup_container_filesystem(temp_dir, dir_modes, container_system_config):
    libc.mount(None, temp_dir, 'tmpfs', 0, 'size=100%')
    mount_base = os.path.join(temp_dir, 'mount')
    temp_base = os.path.join(temp_dir, 'temp')
    work_base = os.path.join(temp_dir, 'overlayfs')
    os.mkdir(mount_base)
    os.mkdir(temp_base)
    os.mkdir(work_base)
    container.duplicate_mount_hierarchy(mount_base, temp_base, work_base, dir_modes)

    def make_tmpfs_dir(path):
        """Ensure that a tmpfs is mounted on path, if the path exists"""
        if path in dir_modes:
            return
        mount_tmpfs = mount_base + path
        if os.path.isdir(mount_tmpfs):
            temp_tmpfs = temp_base + path
            util.makedirs(temp_tmpfs, exist_ok=True)
            container.make_bind_mount(temp_tmpfs, mount_tmpfs)

    make_tmpfs_dir('/dev/shm')
    make_tmpfs_dir('/run/shm')
    if container_system_config:
        container.setup_container_system_config(temp_base, mount_base, dir_modes)
    cwd = os.getcwd()
    container.chroot(mount_base)
    os.chdir(cwd)
    return


def _call_tool_func(name, args, kwargs):
    """Call a method on the tool instance.
    @param name: The method name to call.
    @param args: List of arguments to be passed as positional arguments.
    @param kwargs: Dict of arguments to be passed as keyword arguments.
    """
    try:
        return getattr(tool, name)(*args, **kwargs)
    except SystemExit as e:
        raise BenchExecException(str(e.code))