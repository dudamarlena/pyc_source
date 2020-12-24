# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/containerexecutor.py
# Compiled at: 2020-05-07 05:52:35
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, errno, logging, os, collections, shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

import signal, subprocess, sys, tempfile
from benchexec import __version__
from benchexec import baseexecutor
from benchexec import BenchExecException
from benchexec.cgroups import Cgroup
from benchexec import container
from benchexec import libc
from benchexec import util
from benchexec.container import DIR_MODES, DIR_HIDDEN, DIR_READ_ONLY, DIR_OVERLAY, DIR_FULL_ACCESS, NATIVE_CLONE_CALLBACK_SUPPORTED
sys.dont_write_bytecode = True
_HAS_SIGWAIT = hasattr(signal, b'sigwait')

def add_basic_container_args(argument_parser):
    argument_parser.add_argument(b'--network-access', action=b'store_true', help=b'allow process to use network communication')
    argument_parser.add_argument(b'--no-tmpfs', dest=b'tmpfs', action=b'store_false', help=b'Store temporary files (e.t., tool output files) on the actual file system instead of a tmpfs ("RAM disk") that is included in the memory limit')
    argument_parser.add_argument(b'--keep-system-config', dest=b'container_system_config', action=b'store_false', help=b'do not use a special minimal configuration for local user and host lookups inside the container')
    argument_parser.add_argument(b'--keep-tmp', action=b'store_true', help=b"do not use a private /tmp for process (same as '--full-access-dir /tmp')")
    argument_parser.add_argument(b'--hidden-dir', metavar=b'DIR', action=b'append', default=[], help=b"hide this directory by mounting an empty directory over it (default for '/tmp' and '/run')")
    argument_parser.add_argument(b'--read-only-dir', metavar=b'DIR', action=b'append', default=[], help=b'make this directory visible read-only in the container')
    argument_parser.add_argument(b'--overlay-dir', metavar=b'DIR', action=b'append', default=[], help=b"mount an overlay filesystem over this directory that redirects all write accesses to temporary files (default for '/')")
    argument_parser.add_argument(b'--full-access-dir', metavar=b'DIR', action=b'append', default=[], help=b'give full access (read/write) to this host directory to processes inside container')


def handle_basic_container_args(options, parser=None):
    """Handle the options specified by add_basic_container_args().
    @return: a dict that can be used as kwargs for the ContainerExecutor constructor
    """
    dir_modes = {}
    error_fn = parser.error if parser else sys.exit

    def handle_dir_mode(path, mode):
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            error_fn((b"Cannot specify directory mode for '{}' because it does not exist or is no directory.").format(path))
        if path in dir_modes:
            error_fn((b"Cannot specify multiple directory modes for '{}'.").format(path))
        dir_modes[path] = mode

    for path in options.hidden_dir:
        handle_dir_mode(path, DIR_HIDDEN)

    for path in options.read_only_dir:
        handle_dir_mode(path, DIR_READ_ONLY)

    for path in options.overlay_dir:
        handle_dir_mode(path, DIR_OVERLAY)

    for path in options.full_access_dir:
        handle_dir_mode(path, DIR_FULL_ACCESS)

    if options.keep_tmp:
        if b'/tmp' in dir_modes and not dir_modes[b'/tmp'] == DIR_FULL_ACCESS:
            error_fn(b'Cannot specify both --keep-tmp and --hidden-dir /tmp.')
        dir_modes[b'/tmp'] = DIR_FULL_ACCESS
    elif b'/tmp' not in dir_modes:
        dir_modes[b'/tmp'] = DIR_HIDDEN
    if b'/' not in dir_modes:
        dir_modes[b'/'] = DIR_OVERLAY
    if b'/run' not in dir_modes:
        dir_modes[b'/run'] = DIR_HIDDEN
    if options.container_system_config:
        if options.network_access:
            logging.warning(b'The container configuration disables DNS, host lookups will fail despite --network-access. Consider using --keep-system-config.')
    else:
        if b'/run/resolvconf' not in dir_modes and os.path.isdir(b'/run/resolvconf'):
            dir_modes[b'/run/resolvconf'] = DIR_READ_ONLY
        if b'/run/systemd/resolve' not in dir_modes and os.path.isdir(b'/run/systemd/resolve'):
            dir_modes[b'/run/systemd/resolve'] = DIR_READ_ONLY
    return {b'network_access': options.network_access, b'container_tmpfs': options.tmpfs, 
       b'container_system_config': options.container_system_config, 
       b'dir_modes': dir_modes}


def add_container_output_args(argument_parser):
    """Define command-line arguments for output of a container (result files).
    @param argument_parser: an argparse parser instance
    """
    argument_parser.add_argument(b'--output-directory', metavar=b'DIR', default=b'output.files', help=b"target directory for result files (default: './output.files')")
    argument_parser.add_argument(b'--result-files', metavar=b'PATTERN', action=b'append', default=[], help=b"pattern for specifying which result files should be copied to the output directory (default: '.')")


def handle_container_output_args(options, parser):
    """Handle the options specified by add_container_output_args().
    @return: a dict that can be used as kwargs for the ContainerExecutor.execute_run()
    """
    if options.result_files:
        result_files_patterns = [ os.path.normpath(p) for p in options.result_files if p ]
        for pattern in result_files_patterns:
            if pattern.startswith(b'..'):
                parser.error((b"Invalid relative result-files pattern '{}'.").format(pattern))

    else:
        result_files_patterns = [
         b'.']
    output_dir = options.output_directory
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        parser.error((b"Output directory '{}' must not refer to an existing file.").format(output_dir))
    return {b'output_dir': output_dir, b'result_files_patterns': result_files_patterns}


def main(argv=None):
    """
    A simple command-line interface for the containerexecutor module of BenchExec.
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(fromfile_prefix_chars=b'@', description=b"Execute a command inside a simple container, i.e., partially\n            isolated from the host. Command-line parameters can additionally be read\n            from a file if file name prefixed with '@' is given as argument.\n            Part of BenchExec: https://github.com/sosy-lab/benchexec/")
    parser.add_argument(b'--dir', metavar=b'DIR', help=b'working directory for executing the command (default is current directory)')
    parser.add_argument(b'--root', action=b'store_true', help=b'Use UID 0 and GID 0 (i.e., fake root account) within container. This is mostly safe, but processes can use this to circumvent some file system restrictions of the container and access otherwise hidden directories.')
    parser.add_argument(b'--uid', metavar=b'UID', type=int, default=None, help=b'use given UID within container (default: current UID)')
    parser.add_argument(b'--gid', metavar=b'GID', type=int, default=None, help=b'use given GID within container (default: current UID)')
    add_basic_container_args(parser)
    add_container_output_args(parser)
    baseexecutor.add_basic_executor_options(parser)
    options = parser.parse_args(argv[1:])
    baseexecutor.handle_basic_executor_options(options, parser)
    logging.debug(b'This is containerexec %s.', __version__)
    container_options = handle_basic_container_args(options, parser)
    container_output_options = handle_container_output_args(options, parser)
    if options.root:
        if options.uid is not None or options.gid is not None:
            parser.error(b'Cannot combine option --root with --uid/--gid')
        options.uid = 0
        options.gid = 0
    formatted_args = (b' ').join(map(util.escape_string_shell, options.args))
    logging.info(b'Starting command %s', formatted_args)
    executor = ContainerExecutor(uid=options.uid, gid=options.gid, **container_options)

    def signal_handler_kill(signum, frame):
        executor.stop()

    signal.signal(signal.SIGTERM, signal_handler_kill)
    signal.signal(signal.SIGQUIT, signal_handler_kill)
    signal.signal(signal.SIGINT, signal_handler_kill)
    try:
        result = executor.execute_run(options.args, workingDir=options.dir, **container_output_options)
    except (BenchExecException, OSError) as e:
        if options.debug:
            logging.exception(e)
        sys.exit((b'Cannot execute {0}: {1}.').format(util.escape_string_shell(options.args[0]), e))

    return result.signal or result.value


class ContainerExecutor(baseexecutor.BaseExecutor):
    """Extended executor that allows to start the processes inside containers
    using Linux namespaces."""

    def __init__(self, use_namespaces=True, uid=None, gid=None, network_access=False, dir_modes={b'/': DIR_OVERLAY, b'/run': DIR_HIDDEN, b'/tmp': DIR_HIDDEN}, container_system_config=True, container_tmpfs=True, *args, **kwargs):
        """Create instance.
        @param use_namespaces: If False, disable all container features of this class
            and ignore all other parameters.
        @param uid: Which UID to use inside container.
        @param gid: Which GID to use inside container.
        @param network_access:
            Whether to allow processes in the contain to access the network.
        @param dir_modes: Dict that specifies which directories should be accessible
            and how in the container.
        @param container_system_config: Whether to use a special system configuration in
            the container that disables all remote host and user lookups, sets a custom
            hostname, etc.
        """
        super(ContainerExecutor, self).__init__(*args, **kwargs)
        self._use_namespaces = use_namespaces
        if not use_namespaces:
            return
        else:
            self._container_tmpfs = container_tmpfs
            self._container_system_config = container_system_config
            self._uid = uid if uid is not None else container.CONTAINER_UID if container_system_config else os.getuid()
            self._gid = gid if gid is not None else container.CONTAINER_GID if container_system_config else os.getgid()
            self._allow_network = network_access
            self._env_override = {}
            if container_system_config:
                self._env_override[b'HOME'] = container.CONTAINER_HOME
                if container.CONTAINER_HOME not in dir_modes:
                    dir_modes[container.CONTAINER_HOME] = DIR_HIDDEN
            if b'/' not in dir_modes:
                raise ValueError(b"Need directory mode for '/'.")
            for path, kind in dir_modes.items():
                if kind not in DIR_MODES:
                    raise ValueError((b"Invalid value '{}' for directory '{}'.").format(kind, path))
                if not os.path.isabs(path):
                    raise ValueError((b"Invalid non-absolute directory '{}'.").format(path))
                if path == b'/proc':
                    raise ValueError(b'Cannot specify directory mode for /proc.')

            sorted_special_dirs = sorted(((path.encode(), kind) for path, kind in dir_modes.items()), key=lambda tupl: len(tupl[0]))
            self._dir_modes = collections.OrderedDict(sorted_special_dirs)

            def is_accessible(path):
                mode = container.determine_directory_mode(self._dir_modes, path)
                return os.access(path, os.R_OK) and mode not in [None, container.DIR_HIDDEN]

            if not is_accessible(container.LXCFS_PROC_DIR):
                logging.info(b'LXCFS is not available, some host information like the uptime leaks into the container.')
            if not NATIVE_CLONE_CALLBACK_SUPPORTED:
                logging.debug(b'Using a non-robust fallback for clone callback. If you have many threads please read https://github.com/sosy-lab/benchexec/issues/435')
            return

    def _get_result_files_base(self, temp_dir):
        """Given the temp directory that is created for each run, return the path to the
        directory where files created by the tool are stored."""
        if not self._use_namespaces:
            return super(ContainerExecutor, self)._get_result_files_base(temp_dir)
        else:
            return os.path.join(temp_dir, b'temp')

    def execute_run(self, args, workingDir=None, output_dir=None, result_files_patterns=[], rootDir=None, environ=os.environ.copy()):
        """
        This method executes the command line and waits for the termination of it,
        handling all setup and cleanup.

        Note that this method does not expect to be interrupted by KeyboardInterrupt
        and does not guarantee proper cleanup if KeyboardInterrupt is raised!
        If this method runs on the main thread of your program,
        make sure to set a signal handler for signal.SIGINT that calls stop() instead.

        @param args: the command line to run
        @param rootDir: None or a root directory that contains all relevant files
            for starting a new process
        @param workingDir:
            None or a directory which the execution should use as working directory
        @param output_dir: the directory where to write result files
            (required if result_files_pattern)
        @param result_files_patterns:
            a list of patterns of files to retrieve as result files
        """
        temp_dir = None
        if rootDir is None:
            temp_dir = tempfile.mkdtemp(prefix=b'BenchExec_run_')
        pid = None
        returnvalue = 0
        logging.debug(b'Starting process.')
        try:
            pid, result_fn = self._start_execution(args=args, stdin=None, stdout=None, stderr=None, env=environ, root_dir=rootDir, cwd=workingDir, temp_dir=temp_dir, cgroups=Cgroup({}), output_dir=output_dir, result_files_patterns=result_files_patterns, child_setup_fn=util.dummy_fn, parent_setup_fn=util.dummy_fn, parent_cleanup_fn=util.dummy_fn)
            with self.SUB_PROCESS_PIDS_LOCK:
                self.SUB_PROCESS_PIDS.add(pid)
            returnvalue, unused_ru_child, unused = result_fn()
        finally:
            logging.debug(b'Process terminated, exit code %s.', returnvalue)
            with self.SUB_PROCESS_PIDS_LOCK:
                self.SUB_PROCESS_PIDS.discard(pid)
            if temp_dir is not None:
                logging.debug(b'Cleaning up temporary directory.')
                util.rmtree(temp_dir, onerror=util.log_rmtree_error)

        return util.ProcessExitCode.from_raw(returnvalue)

    def _start_execution(self, root_dir=None, output_dir=None, result_files_patterns=[], memlimit=None, memory_nodes=None, *args, **kwargs):
        if not self._use_namespaces:
            return super(ContainerExecutor, self)._start_execution(*args, **kwargs)
        else:
            if result_files_patterns:
                if not output_dir:
                    raise ValueError(b'Output directory needed for retaining result files.')
                for pattern in result_files_patterns:
                    if not pattern:
                        raise ValueError((b'Invalid empty result-files pattern in {}').format(result_files_patterns))
                    pattern = os.path.normpath(pattern)
                    if pattern.startswith(b'..'):
                        raise ValueError((b"Invalid relative result-files pattern '{}'.").format(pattern))

            return self._start_execution_in_container(root_dir=root_dir, output_dir=output_dir, memlimit=memlimit, memory_nodes=memory_nodes, result_files_patterns=result_files_patterns, *args, **kwargs)

    def _start_execution_in_container(self, args, stdin, stdout, stderr, env, root_dir, cwd, temp_dir, memlimit, memory_nodes, cgroups, output_dir, result_files_patterns, parent_setup_fn, child_setup_fn, parent_cleanup_fn):
        """Execute the given command and measure its resource usage similarly to
        super()._start_execution(), but inside a container implemented using Linux
        namespaces.  The command has no network access (only loopback),
        a fresh directory as /tmp and no write access outside of this,
        and it does not see other processes except itself.
        """
        assert self._use_namespaces
        if root_dir is None:
            env.update(self._env_override)
        CHILD_OSERROR = 128
        CHILD_UNKNOWN_ERROR = 129
        from_parent, to_grandchild = os.pipe()
        from_grandchild, to_parent = os.pipe()
        MARKER_USER_MAPPING_COMPLETED = b'A'
        MARKER_PARENT_COMPLETED = b'B'
        MARKER_PARENT_POST_RUN_COMPLETED = b'C'
        if root_dir is None:
            cwd = os.path.abspath(cwd or os.curdir)
        else:
            root_dir = os.path.abspath(root_dir)
            cwd = os.path.abspath(cwd)

        def grandchild():
            """Setup everything inside the process that finally exec()s the tool."""
            try:
                my_outer_pid = container.get_my_pid_from_procfs()
                container.mount_proc(self._container_system_config)
                container.drop_capabilities()
                container.reset_signal_handling()
                child_setup_fn()
                os.write(to_parent, str(my_outer_pid).encode())
                received = os.read(from_parent, 1)
                assert received == MARKER_PARENT_COMPLETED, received
            finally:
                os.close(from_parent)
                os.close(to_parent)

        def child():
            """Setup everything inside the container,
            start the tool, and wait for result."""
            try:
                logging.debug(b'Child: child process of RunExecutor with PID %d started', container.get_my_pid_from_procfs())
                container.block_all_signals()
                necessary_fds = {
                 sys.stdin,
                 sys.stdout,
                 sys.stderr,
                 to_parent,
                 from_parent,
                 stdin,
                 stdout,
                 stderr} - {
                 None}
                container.close_open_fds(keep_files=necessary_fds)
                try:
                    if self._container_system_config:
                        libc.sethostname(container.CONTAINER_HOSTNAME)
                    if not self._allow_network:
                        container.activate_network_interface(b'lo')
                    received = os.read(from_parent, len(MARKER_USER_MAPPING_COMPLETED))
                    assert received == MARKER_USER_MAPPING_COMPLETED, received
                    if root_dir is not None:
                        self._setup_root_filesystem(root_dir)
                    else:
                        self._setup_container_filesystem(temp_dir, output_dir if result_files_patterns else None, memlimit, memory_nodes)
                    libc.prctl(libc.PR_SET_DUMPABLE, libc.SUID_DUMP_DISABLE, 0, 0, 0)
                except EnvironmentError as e:
                    logging.critical(b'Failed to configure container: %s', e)
                    return CHILD_OSERROR

                try:
                    os.chdir(cwd)
                except EnvironmentError as e:
                    logging.critical(b'Cannot change into working directory inside container: %s', e)
                    return CHILD_OSERROR

                container.setup_seccomp_filter()
                try:
                    grandchild_proc = subprocess.Popen(args, stdin=stdin, stdout=stdout, stderr=stderr, env=env, close_fds=False, preexec_fn=grandchild)
                except (EnvironmentError, RuntimeError) as e:
                    logging.critical(b'Cannot start process: %s', e)
                    return CHILD_OSERROR

                necessary_capabilities = [libc.CAP_SYS_ADMIN] if result_files_patterns else []
                container.drop_capabilities(keep=necessary_capabilities)
                container.close_open_fds(keep_files={
                 sys.stdout, sys.stderr, to_parent, from_parent})
                if _HAS_SIGWAIT:
                    grandchild_result = container.wait_for_child_and_forward_signals(grandchild_proc.pid, args[0])
                else:
                    container.forward_all_signals_async(grandchild_proc.pid, args[0])
                    grandchild_result = self._wait_for_process(grandchild_proc.pid, args[0])
                logging.debug(b'Child: process %s terminated with exit code %d.', args[0], grandchild_result[0])
                if result_files_patterns:
                    libc.umount(temp_dir.encode())
                libc.prctl(libc.PR_SET_DUMPABLE, libc.SUID_DUMP_USER, 0, 0, 0)
                os.write(to_parent, pickle.dumps(grandchild_result))
                os.close(to_parent)
                assert os.read(from_parent, 1) == MARKER_PARENT_POST_RUN_COMPLETED
                os.close(from_parent)
                return 0
            except EnvironmentError:
                logging.exception(b'Error in child process of RunExecutor')
                return CHILD_OSERROR
            except:
                logging.exception(b'Error in child process of RunExecutor')
                return CHILD_UNKNOWN_ERROR

            return

        try:
            try:
                child_pid = container.execute_in_namespace(child, use_network_ns=not self._allow_network)
            except OSError as e:
                if e.errno == errno.EPERM and util.try_read_file(b'/proc/sys/kernel/unprivileged_userns_clone') == b'0':
                    raise BenchExecException(b"Unprivileged user namespaces forbidden on this system, please enable them with 'sysctl kernel.unprivileged_userns_clone=1' or disable container mode")
                else:
                    raise BenchExecException(b'Creating namespace for container mode failed: ' + os.strerror(e.errno))

            logging.debug(b'Parent: child process of RunExecutor with PID %d started.', child_pid)

            def check_child_exit_code():
                """Check if the child process terminated cleanly
                and raise an error otherwise."""
                child_exitcode, unused_child_rusage = self._wait_for_process(child_pid, args[0])
                child_exitcode = util.ProcessExitCode.from_raw(child_exitcode)
                logging.debug(b'Parent: child process of RunExecutor with PID %d terminated with %s.', child_pid, child_exitcode)
                if child_exitcode:
                    if child_exitcode.value:
                        if child_exitcode.value == CHILD_OSERROR:
                            raise BenchExecException(b'execution in container failed, check log for details')
                        elif child_exitcode.value == CHILD_UNKNOWN_ERROR:
                            raise BenchExecException(b'unexpected error in container')
                        raise OSError(child_exitcode.value, os.strerror(child_exitcode.value))
                    raise OSError(0, b'Child process of RunExecutor terminated with ' + str(child_exitcode))

            os.close(from_parent)
            os.close(to_parent)
            container.setup_user_mapping(child_pid, uid=self._uid, gid=self._gid)
            os.write(to_grandchild, MARKER_USER_MAPPING_COMPLETED)
            try:
                grandchild_pid = int(os.read(from_grandchild, 10))
            except ValueError:
                check_child_exit_code()
                assert False, b'Child process of RunExecutor terminated cleanly but did not send expected data.'

            logging.debug(b'Parent: executing %s in grand child with PID %d via child with PID %d.', args[0], grandchild_pid, child_pid)
            cgroups.add_task(grandchild_pid)
            parent_setup = parent_setup_fn()
            os.write(to_grandchild, MARKER_PARENT_COMPLETED)
            from_grandchild_copy = os.dup(from_grandchild)
            to_grandchild_copy = os.dup(to_grandchild)
        finally:
            os.close(from_grandchild)
            os.close(to_grandchild)

        def wait_for_grandchild():
            try:
                received = os.read(from_grandchild_copy, 1024)
            except OSError as e:
                if self.PROCESS_KILLED and e.errno == errno.EINTR:
                    received = os.read(from_grandchild_copy, 1024)
                else:
                    raise e

            received or os.close(from_grandchild_copy)
            os.close(to_grandchild_copy)
            check_child_exit_code()
            assert False, b'Child process terminated cleanly without sending result'
            exitcode, ru_child = pickle.loads(received)
            base_path = (b'/proc/{}/root').format(child_pid)
            parent_cleanup = parent_cleanup_fn(parent_setup, util.ProcessExitCode.from_raw(exitcode), base_path)
            if result_files_patterns:
                self._transfer_output_files(base_path + temp_dir, cwd, output_dir, result_files_patterns)
            os.close(from_grandchild_copy)
            os.write(to_grandchild_copy, MARKER_PARENT_POST_RUN_COMPLETED)
            os.close(to_grandchild_copy)
            check_child_exit_code()
            return (
             exitcode, ru_child, parent_cleanup)

        return (
         grandchild_pid, wait_for_grandchild)

    def _setup_container_filesystem(self, temp_dir, output_dir, memlimit, memory_nodes):
        """Setup the filesystem layout in the container.
        As first step, we create a copy of all existing mountpoints in mount_base,
        recursively, and as "private" mounts
        (i.e., changes to existing mountpoints afterwards won't propagate to our copy).
        Then we iterate over all mountpoints and change them according to the mode
        the user has specified (hidden, read-only, overlay, or full-access).
        This has do be done for each mountpoint because overlays are not recursive.
        Then we chroot into the new mount hierarchy.

        The new filesystem layout still has a view of the host's /proc. We do not mount
        a fresh /proc here because the grandchild still needs the old /proc.

        We do simply iterate over all existing mount points and set them to
        read-only/overlay them, because it is easier to create a new hierarchy and
        chroot into it. First, we still have access to the original mountpoints while
        doing so, and second, we avoid race conditions if someone else changes the
        existing mountpoints.

        @param temp_dir:
            The base directory under which all our directories should be created.
        """
        temp_base = self._get_result_files_base(temp_dir).encode()
        temp_dir = temp_dir.encode()
        tmpfs_opts = [
         b'size=' + str(memlimit or b'100%')]
        if memory_nodes:
            tmpfs_opts.append(b'mpol=bind:' + (b',').join(map(str, memory_nodes)))
        tmpfs_opts = (b',').join(tmpfs_opts).encode()
        if self._container_tmpfs:
            libc.mount(None, temp_dir, b'tmpfs', 0, tmpfs_opts)
        mount_base = os.path.join(temp_dir, b'mount')
        os.mkdir(mount_base)
        os.mkdir(temp_base)
        work_base = os.path.join(temp_dir, b'overlayfs')
        os.mkdir(work_base)
        container.duplicate_mount_hierarchy(mount_base, temp_base, work_base, self._dir_modes)

        def make_tmpfs_dir(path):
            """Ensure that a tmpfs is mounted on path, if the path exists"""
            if path in self._dir_modes:
                return
            else:
                mount_tmpfs = mount_base + path
                temp_tmpfs = temp_base + path
                util.makedirs(temp_tmpfs, exist_ok=True)
                if os.path.isdir(mount_tmpfs):
                    if self._container_tmpfs:
                        container.make_bind_mount(temp_tmpfs, mount_tmpfs)
                    else:
                        libc.mount(None, mount_tmpfs, b'tmpfs', 0, tmpfs_opts)
                return

        make_tmpfs_dir(b'/dev/shm')
        make_tmpfs_dir(b'/run/shm')
        if self._container_system_config:
            container.setup_container_system_config(temp_base, mount_base, self._dir_modes)
        if output_dir:
            util.makedirs(mount_base + temp_dir, exist_ok=True)
            container.make_bind_mount(temp_base, mount_base + temp_dir, read_only=True)
        if os.path.exists(mount_base + temp_dir):
            util.makedirs(temp_base + temp_dir, exist_ok=True)
            container.make_bind_mount(temp_base + temp_dir, mount_base + temp_dir)
        container.chroot(mount_base)
        return

    def _setup_root_filesystem(self, root_dir):
        """Setup the filesystem layout in the given root directory.
        Create a copy of the existing proc- and dev-mountpoints in the specified root
        directory. Afterwards we chroot into it.

        @param root_dir:
            The path of the root directory that is used to execute the process.
        """
        root_dir = root_dir.encode()
        proc_base = os.path.join(root_dir, b'proc')
        util.makedirs(proc_base, exist_ok=True)
        dev_base = os.path.join(root_dir, b'dev')
        util.makedirs(dev_base, exist_ok=True)
        container.make_bind_mount(b'/dev/', dev_base, recursive=True, private=True)
        container.make_bind_mount(b'/proc/', proc_base, recursive=True, private=True)
        os.chroot(root_dir)

    def _transfer_output_files(self, tool_output_dir, working_dir, output_dir, patterns):
        """Transfer files created by the tool in the container to the output directory.
        @param tool_output_dir:
            The directory under which all tool output files are created.
        @param working_dir: The absolute working directory of the tool in the container.
        @param output_dir: the directory where to write result files
        @param patterns: a list of patterns of files to retrieve as result files
        """
        assert output_dir
        assert patterns
        if any(os.path.isabs(pattern) for pattern in patterns):
            base_dir = tool_output_dir
        else:
            base_dir = tool_output_dir + working_dir

        def transfer_file(abs_file):
            assert abs_file.startswith(base_dir)
            file = os.path.join(b'/', os.path.relpath(abs_file, base_dir))
            if os.path.isfile(abs_file) and not os.path.islink(abs_file) and not container.is_container_system_config_file(file):
                target = output_dir + file
                logging.debug(b'Transferring output file %s to %s', abs_file, target)
                try:
                    os.makedirs(os.path.dirname(target))
                except EnvironmentError:
                    pass

                try:
                    shutil.move(abs_file, target)
                except EnvironmentError as e:
                    logging.warning(b"Could not retrieve output file '%s': %s", file, e)

        for pattern in patterns:
            if os.path.isabs(pattern):
                pattern = tool_output_dir + pattern
            else:
                pattern = tool_output_dir + os.path.join(working_dir, pattern)
            for abs_file in util.maybe_recursive_iglob(os.path.normpath(pattern), recursive=True):
                if os.path.isdir(abs_file):
                    for root, unused_dirs, files in os.walk(abs_file):
                        for file in files:
                            transfer_file(os.path.join(root, file))

                else:
                    transfer_file(abs_file)


if __name__ == b'__main__':
    main()