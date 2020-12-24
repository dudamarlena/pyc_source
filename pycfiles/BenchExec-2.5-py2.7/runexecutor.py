# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/runexecutor.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, collections, errno, logging, multiprocessing, os, signal, subprocess, sys, threading, time, tempfile
sys.dont_write_bytecode = True
from benchexec import __version__
from benchexec import baseexecutor
from benchexec import BenchExecException
from benchexec import containerexecutor
from benchexec.cgroups import *
from benchexec.filehierarchylimit import FileHierarchyLimitThread
from benchexec import intel_cpu_energy
from benchexec import oomhandler
from benchexec import resources
from benchexec import systeminfo
from benchexec import util
_WALLTIME_LIMIT_DEFAULT_OVERHEAD = 30
_BYTE_FACTOR = 1000
_LOG_SHRINK_MARKER = b'\n\n\nWARNING: YOUR LOGFILE WAS TOO LONG, SOME LINES IN THE MIDDLE WERE REMOVED.\n\n\n\n'
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, b'rb')

def main(argv=None):
    """
    A simple command-line interface for the runexecutor module of BenchExec.
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(fromfile_prefix_chars=b'@', description=b"Execute a command with resource limits and measurements.\n           Command-line parameters can additionally be read from a file if file name prefixed with '@' is given as argument.\n           Part of BenchExec: https://github.com/sosy-lab/benchexec/")
    resource_args = parser.add_argument_group(b'optional arguments for resource limits')
    resource_args.add_argument(b'--memlimit', type=util.parse_memory_value, metavar=b'BYTES', help=b'memory limit in bytes')
    resource_args.add_argument(b'--timelimit', type=util.parse_timespan_value, metavar=b'SECONDS', help=b'CPU time limit in seconds')
    resource_args.add_argument(b'--softtimelimit', type=util.parse_timespan_value, metavar=b'SECONDS', help=b'"soft" CPU time limit in seconds (command will be send the TERM signal at this time)')
    resource_args.add_argument(b'--walltimelimit', type=util.parse_timespan_value, metavar=b'SECONDS', help=b'wall time limit in seconds (default is CPU time limit plus a few seconds)')
    resource_args.add_argument(b'--cores', type=util.parse_int_list, metavar=b'N,M-K', help=b'list of CPU cores to use')
    resource_args.add_argument(b'--memoryNodes', type=util.parse_int_list, metavar=b'N,M-K', help=b'list of memory nodes to use')
    io_args = parser.add_argument_group(b'optional arguments for run I/O')
    io_args.add_argument(b'--input', metavar=b'FILE', help=b'name of file used as stdin for command (default: /dev/null; use - for stdin passthrough)')
    io_args.add_argument(b'--output', default=b'output.log', metavar=b'FILE', help=b'name of file where command output (stdout and stderr) is written')
    io_args.add_argument(b'--maxOutputSize', type=util.parse_memory_value, metavar=b'BYTES', help=b'shrink output file to approximately this size if necessary (by removing lines from the middle of the output)')
    io_args.add_argument(b'--filesCountLimit', type=int, metavar=b'COUNT', help=b'maximum number of files the tool may write to (checked periodically, counts only files written in container mode or to temporary directories, only supported with --no-tmpfs)')
    io_args.add_argument(b'--filesSizeLimit', type=util.parse_memory_value, metavar=b'BYTES', help=b'maximum size of files the tool may write (checked periodically, counts only files written in container mode or to temporary directories, only supported with --no-tmpfs)')
    io_args.add_argument(b'--skip-cleanup', action=b'store_false', dest=b'cleanup', help=b'do not delete files created by the tool in temp directory')
    container_args = parser.add_argument_group(b'optional arguments for run container')
    container_on_args = container_args.add_mutually_exclusive_group()
    container_on_args.add_argument(b'--container', action=b'store_true', dest=b'_ignored_container', help=b'force isolation of run in container (default)')
    container_on_args.add_argument(b'--no-container', action=b'store_false', dest=b'container', help=b'disable use of containers for isolation of runs')
    containerexecutor.add_basic_container_args(container_args)
    containerexecutor.add_container_output_args(container_args)
    environment_args = parser.add_argument_group(b'optional arguments for run environment')
    environment_args.add_argument(b'--require-cgroup-subsystem', action=b'append', default=[], metavar=b'SUBSYSTEM', help=b'additional cgroup system that should be enabled for runs (may be specified multiple times)')
    environment_args.add_argument(b'--set-cgroup-value', action=b'append', dest=b'cgroup_values', default=[], metavar=b'SUBSYSTEM.OPTION=VALUE', help=b"additional cgroup values that should be set for runs (e.g., 'cpu.shares=1000')")
    environment_args.add_argument(b'--dir', metavar=b'DIR', help=b'working directory for executing the command (default is current directory)')
    baseexecutor.add_basic_executor_options(parser)
    options = parser.parse_args(argv[1:])
    baseexecutor.handle_basic_executor_options(options, parser)
    logging.debug(b'This is runexec %s.', __version__)
    if options.container:
        container_options = containerexecutor.handle_basic_container_args(options, parser)
        container_output_options = containerexecutor.handle_container_output_args(options, parser)
        if container_options[b'container_tmpfs'] and (options.filesCountLimit or options.filesSizeLimit):
            parser.error(b'Files-count limit and files-size limit are not supported if tmpfs is used in container. Use --no-tmpfs to make these limits work or disable them (typically they are unnecessary if a tmpfs is used).')
    else:
        container_options = {}
        container_output_options = {}
    if options.input == b'-':
        stdin = sys.stdin
    else:
        if options.input is not None:
            if options.input == options.output:
                parser.error(b'Input and output files cannot be the same.')
            try:
                stdin = open(options.input, b'rt')
            except IOError as e:
                parser.error(e)

        else:
            stdin = None
        cgroup_subsystems = set(options.require_cgroup_subsystem)
        cgroup_values = {}
        for arg in options.cgroup_values:
            try:
                key, value = arg.split(b'=', 1)
                subsystem, option = key.split(b'.', 1)
                if not subsystem or not option:
                    raise ValueError()
            except ValueError:
                parser.error((b'Cgroup value "{}" has invalid format, needs to be "subsystem.option=value".').format(arg))

            cgroup_values[(subsystem, option)] = value
            cgroup_subsystems.add(subsystem)

        executor = RunExecutor(cleanup_temp_dir=options.cleanup, additional_cgroup_subsystems=list(cgroup_subsystems), use_namespaces=options.container, **container_options)

        def signal_handler_kill(signum, frame):
            executor.stop()

        signal.signal(signal.SIGTERM, signal_handler_kill)
        signal.signal(signal.SIGQUIT, signal_handler_kill)
        signal.signal(signal.SIGINT, signal_handler_kill)
        formatted_args = (b' ').join(map(util.escape_string_shell, options.args))
        logging.info(b'Starting command %s', formatted_args)
        if options.container and options.output_directory and options.result_files:
            logging.info(b'Writing output to %s and result files to %s', util.escape_string_shell(options.output), util.escape_string_shell(options.output_directory))
        else:
            logging.info(b'Writing output to %s', util.escape_string_shell(options.output))
        try:
            result = executor.execute_run(args=options.args, output_filename=options.output, stdin=stdin, hardtimelimit=options.timelimit, softtimelimit=options.softtimelimit, walltimelimit=options.walltimelimit, cores=options.cores, memlimit=options.memlimit, memory_nodes=options.memoryNodes, cgroupValues=cgroup_values, workingDir=options.dir, maxLogfileSize=options.maxOutputSize, files_count_limit=options.filesCountLimit, files_size_limit=options.filesSizeLimit, **container_output_options)
        finally:
            if stdin:
                stdin.close()

        exit_code = result.pop(b'exitcode', None)

        def print_optional_result(key, unit=b'', format_fn=str):
            if key in result:
                print(key + b'=' + format_fn(result[key]) + unit)

        print_optional_result(b'starttime', unit=b'', format_fn=lambda dt: dt.isoformat())
        print_optional_result(b'terminationreason')
        if exit_code is not None and exit_code.value is not None:
            print(b'returnvalue=' + str(exit_code.value))
        if exit_code is not None and exit_code.signal is not None:
            print(b'exitsignal=' + str(exit_code.signal))
        print_optional_result(b'walltime', b's')
        print_optional_result(b'cputime', b's')
        for key in sorted(result.keys()):
            if key.startswith(b'cputime-'):
                print((b'{}={:.9f}s').format(key, result[key]))

        print_optional_result(b'memory', b'B')
        print_optional_result(b'blkio-read', b'B')
        print_optional_result(b'blkio-write', b'B')
        energy = intel_cpu_energy.format_energy_results(result.get(b'cpuenergy'))
        for energy_key, energy_value in energy.items():
            print((b'{}={}J').format(energy_key, energy_value))

    return


class RunExecutor(containerexecutor.ContainerExecutor):

    def __init__(self, cleanup_temp_dir=True, additional_cgroup_subsystems=[], *args, **kwargs):
        """
        Create an instance of of RunExecutor.
        @param cleanup_temp_dir Whether to remove the temporary directories created for the run.
        @param additional_cgroup_subsystems List of additional cgroup subsystems that should be required and used for runs.
        """
        super(RunExecutor, self).__init__(*args, **kwargs)
        self._termination_reason = None
        self._should_cleanup_temp_dir = cleanup_temp_dir
        self._cgroup_subsystems = additional_cgroup_subsystems
        self._energy_measurement = intel_cpu_energy.EnergyMeasurement.create_if_supported()
        self._init_cgroups()
        return

    def _init_cgroups(self):
        """
        This function initializes the cgroups for the limitations and measurements.
        """
        self.cgroups = find_my_cgroups()
        for subsystem in self._cgroup_subsystems:
            self.cgroups.require_subsystem(subsystem)
            if subsystem not in self.cgroups:
                sys.exit((b'Required cgroup subsystem "{}" is missing.').format(subsystem))

        self.cgroups.require_subsystem(BLKIO, log_method=logging.debug)
        if BLKIO not in self.cgroups:
            logging.debug(b'Cannot measure I/O without blkio cgroup.')
        self.cgroups.require_subsystem(CPUACCT)
        if CPUACCT not in self.cgroups:
            logging.warning(b'Cannot measure CPU time without cpuacct cgroup.')
        self.cgroups.require_subsystem(FREEZER)
        if FREEZER not in self.cgroups and not self._use_namespaces:
            sys.exit(b'Cannot reliably kill sub-processes without freezer cgroup or container mode. Please enable at least one of them.')
        self.cgroups.require_subsystem(MEMORY)
        if MEMORY not in self.cgroups:
            logging.warning(b'Cannot measure memory consumption without memory cgroup.')
        elif systeminfo.has_swap() and not self.cgroups.has_value(MEMORY, b'memsw.max_usage_in_bytes'):
            logging.warning(b'Kernel misses feature for accounting swap memory, but machine has swap. Memory usage may be measured inaccurately. Please set swapaccount=1 on your kernel command line or disable swap with "sudo swapoff -a".')
        self.cgroups.require_subsystem(CPUSET)
        self.cpus = None
        self.memory_nodes = None
        if CPUSET in self.cgroups:
            try:
                self.cpus = util.parse_int_list(self.cgroups.get_value(CPUSET, b'cpus'))
            except ValueError as e:
                logging.warning(b'Could not read available CPU cores from kernel: %s', e.strerror)

            logging.debug(b'List of available CPU cores is %s.', self.cpus)
            try:
                self.memory_nodes = util.parse_int_list(self.cgroups.get_value(CPUSET, b'mems'))
            except ValueError as e:
                logging.warning(b'Could not read available memory nodes from kernel: %s', e.strerror)

            logging.debug(b'List of available memory nodes is %s.', self.memory_nodes)
        return

    def _set_termination_reason(self, reason):
        if not self._termination_reason:
            self._termination_reason = reason

    def _setup_cgroups(self, my_cpus, memlimit, memory_nodes, cgroup_values):
        """
        This method creates the CGroups for the following execution.
        @param my_cpus: None or a list of the CPU cores to use
        @param memlimit: None or memory limit in bytes
        @param memory_nodes: None or a list of memory nodes of a NUMA system to use
        @param cgroup_values: dict of additional values to set
        @return cgroups: a map of all the necessary cgroups for the following execution.
                         Please add the process of the following execution to all those cgroups!
        """
        logging.debug(b'Setting up cgroups for run.')
        subsystems = [
         BLKIO, CPUACCT, FREEZER, MEMORY] + self._cgroup_subsystems
        if my_cpus is not None or memory_nodes is not None:
            subsystems.append(CPUSET)
        subsystems = [ s for s in subsystems if s in self.cgroups ]
        cgroups = self.cgroups.create_fresh_child_cgroup(*subsystems)
        logging.debug(b'Created cgroups %s.', cgroups)
        for (subsystem, option), value in cgroup_values.items():
            try:
                cgroups.set_value(subsystem, option, value)
            except EnvironmentError as e:
                cgroups.remove()
                sys.exit((b'{} for setting cgroup option {}.{} to "{}" (error code {}).').format(e.strerror, subsystem, option, value, e.errno))

            logging.debug(b'Cgroup value %s.%s was set to "%s", new value is now "%s".', subsystem, option, value, cgroups.get_value(subsystem, option))

        if my_cpus is not None:
            my_cpus_str = (b',').join(map(str, my_cpus))
            cgroups.set_value(CPUSET, b'cpus', my_cpus_str)
            my_cpus_str = cgroups.get_value(CPUSET, b'cpus')
            logging.debug(b'Using cpu cores [%s].', my_cpus_str)
        if memory_nodes is not None:
            cgroups.set_value(CPUSET, b'mems', (b',').join(map(str, memory_nodes)))
            memory_nodesStr = cgroups.get_value(CPUSET, b'mems')
            logging.debug(b'Using memory nodes [%s].', memory_nodesStr)
        if memlimit is not None:
            limit = b'limit_in_bytes'
            cgroups.set_value(MEMORY, limit, memlimit)
            swap_limit = b'memsw.limit_in_bytes'
            if not cgroups.has_value(MEMORY, swap_limit):
                if systeminfo.has_swap():
                    sys.exit(b'Kernel misses feature for accounting swap memory, but machine has swap. Please set swapaccount=1 on your kernel command line or disable swap with "sudo swapoff -a".')
            else:
                try:
                    cgroups.set_value(MEMORY, swap_limit, memlimit)
                except IOError as e:
                    if e.errno == errno.ENOTSUP:
                        sys.exit(b'Memory limit specified, but kernel does not allow limiting swap memory. Please set swapaccount=1 on your kernel command line or disable swap with "sudo swapoff -a".')
                    raise e

            memlimit = cgroups.get_value(MEMORY, limit)
            logging.debug(b'Effective memory limit is %s bytes.', memlimit)
        if MEMORY in cgroups:
            try:
                cgroups.set_value(MEMORY, b'swappiness', b'0')
            except IOError as e:
                logging.warning(b'Could not disable swapping for benchmarked process: %s', e)

        return cgroups

    def _cleanup_temp_dir(self, base_dir):
        """Delete given temporary directory and all its contents."""
        if self._should_cleanup_temp_dir:
            logging.debug(b'Cleaning up temporary directory %s.', base_dir)
            util.rmtree(base_dir, onerror=util.log_rmtree_error)
        else:
            logging.info(b'Skipping cleanup of temporary directory %s.', base_dir)

    def _setup_environment(self, environments):
        """Return map with desired environment variables for run."""
        if environments.get(b'keepEnv', None) is not None:
            run_environment = {}
        else:
            run_environment = os.environ.copy()
        for key, value in environments.get(b'keepEnv', {}).items():
            if key in os.environ:
                run_environment[key] = os.environ[key]

        for key, value in environments.get(b'newEnv', {}).items():
            run_environment[key] = value

        for key, value in environments.get(b'additionalEnv', {}).items():
            run_environment[key] = os.environ.get(key, b'') + value

        for key in environments.get(b'clearEnv', {}).items():
            run_environment.pop(key, None)

        logging.debug(b'Using additional environment %s.', environments)
        return run_environment

    def _setup_output_file(self, output_filename, args, write_header=True):
        """Open and prepare output file."""
        try:
            output_file = open(output_filename, b'w')
        except IOError as e:
            sys.exit(e)

        if write_header:
            output_file.write((b' ').join(map(util.escape_string_shell, args)) + b'\n\n\n' + b'-' * 80 + b'\n\n\n')
            output_file.flush()
        return output_file

    def _setup_cgroup_time_limit(self, hardtimelimit, softtimelimit, walltimelimit, cgroups, cores, pid_to_kill):
        """Start time-limit handler.
        @return None or the time-limit handler for calling cancel()
        """
        if any([hardtimelimit, softtimelimit, walltimelimit]):
            timelimitThread = _TimelimitThread(cgroups=cgroups, hardtimelimit=hardtimelimit, softtimelimit=softtimelimit, walltimelimit=walltimelimit, pid_to_kill=pid_to_kill, cores=cores, callbackFn=self._set_termination_reason)
            timelimitThread.start()
            return timelimitThread
        else:
            return

    def _setup_cgroup_memory_limit(self, memlimit, cgroups, pid_to_kill):
        """Start memory-limit handler.
        @return None or the memory-limit handler for calling cancel()
        """
        if memlimit is not None:
            try:
                oomThread = oomhandler.KillProcessOnOomThread(cgroups=cgroups, pid_to_kill=pid_to_kill, callbackFn=self._set_termination_reason)
                oomThread.start()
                return oomThread
            except OSError as e:
                logging.critical(b'OSError %s during setup of OomEventListenerThread: %s.', e.errno, e.strerror)

        return

    def _setup_file_hierarchy_limit(self, files_count_limit, files_size_limit, temp_dir, cgroups, pid_to_kill):
        """Start thread that enforces any file-hiearchy limits."""
        if files_count_limit is not None or files_size_limit is not None:
            file_hierarchy_limit_thread = FileHierarchyLimitThread(self._get_result_files_base(temp_dir), files_count_limit=files_count_limit, files_size_limit=files_size_limit, pid_to_kill=pid_to_kill, callbackFn=self._set_termination_reason)
            file_hierarchy_limit_thread.start()
            return file_hierarchy_limit_thread
        else:
            return

    def execute_run(self, args, output_filename, stdin=None, hardtimelimit=None, softtimelimit=None, walltimelimit=None, cores=None, memlimit=None, memory_nodes=None, environments={}, workingDir=None, maxLogfileSize=None, cgroupValues={}, files_count_limit=None, files_size_limit=None, error_filename=None, write_header=True, **kwargs):
        """
        This function executes a given command with resource limits,
        and writes the output to a file.

        Note that this method does not expect to be interrupted by KeyboardInterrupt
        and does not guarantee proper cleanup if KeyboardInterrupt is raised!
        If this method runs on the main thread of your program,
        make sure to set a signal handler for signal.SIGINT that calls stop() instead.

        @param args: the command line to run
        @param output_filename: the file where the output should be written to
        @param stdin: What to uses as stdin for the process (None: /dev/null, a file descriptor, or a file object)
        @param hardtimelimit: None or the CPU time in seconds after which the tool is forcefully killed.
        @param softtimelimit: None or the CPU time in seconds after which the tool is sent a kill signal.
        @param walltimelimit: None or the wall time in seconds after which the tool is forcefully killed (default: hardtimelimit + a few seconds)
        @param cores: None or a list of the CPU cores to use
        @param memlimit: None or memory limit in bytes
        @param memory_nodes: None or a list of memory nodes in a NUMA system to use
        @param environments: special environments for running the command
        @param workingDir: None or a directory which the execution should use as working directory
        @param maxLogfileSize: None or a number of bytes to which the output of the tool should be truncated approximately if there is too much output.
        @param cgroupValues: dict of additional cgroup values to set (key is tuple of subsystem and option, respective subsystem needs to be enabled in RunExecutor; cannot be used to override values set by BenchExec)
        @param files_count_limit: None or maximum number of files that may be written.
        @param files_size_limit: None or maximum size of files that may be written.
        @param error_filename: the file where the error output should be written to (default: same as output_filename)
        @param write_headers: Write informational headers to the output and the error file if separate (default: True)
        @param **kwargs: further arguments for ContainerExecutor.execute_run()
        @return: dict with result of run (measurement results and process exitcode)
        """
        if stdin == subprocess.PIPE:
            sys.exit(b'Illegal value subprocess.PIPE for stdin')
        else:
            if stdin is None:
                stdin = DEVNULL
            if hardtimelimit is not None:
                if hardtimelimit <= 0:
                    sys.exit((b'Invalid time limit {0}.').format(hardtimelimit))
                if CPUACCT not in self.cgroups:
                    sys.exit(b'Time limit cannot be specified without cpuacct cgroup.')
            if softtimelimit is not None:
                if softtimelimit <= 0:
                    sys.exit((b'Invalid soft time limit {0}.').format(softtimelimit))
                if hardtimelimit and softtimelimit > hardtimelimit:
                    sys.exit(b'Soft time limit cannot be larger than the hard time limit.')
                if CPUACCT not in self.cgroups:
                    sys.exit(b'Soft time limit cannot be specified without cpuacct cgroup.')
            if walltimelimit is None:
                if hardtimelimit is not None:
                    walltimelimit = hardtimelimit + _WALLTIME_LIMIT_DEFAULT_OVERHEAD
                elif softtimelimit is not None:
                    walltimelimit = softtimelimit + _WALLTIME_LIMIT_DEFAULT_OVERHEAD
            else:
                if walltimelimit <= 0:
                    sys.exit((b'Invalid wall time limit {0}.').format(walltimelimit))
                if cores is not None:
                    if self.cpus is None:
                        sys.exit(b'Cannot limit CPU cores without cpuset cgroup.')
                    if not cores:
                        sys.exit(b'Cannot execute run without any CPU core.')
                    if not set(cores).issubset(self.cpus):
                        sys.exit((b'Cores {0} are not allowed to be used').format(list(set(cores).difference(self.cpus))))
                if memlimit is not None:
                    if memlimit <= 0:
                        sys.exit((b'Invalid memory limit {0}.').format(memlimit))
                    if MEMORY not in self.cgroups:
                        sys.exit(b'Memory limit specified, but cannot be implemented without cgroup support.')
                if memory_nodes is not None:
                    if self.memory_nodes is None:
                        sys.exit(b'Cannot restrict memory nodes without cpuset cgroup.')
                    if len(memory_nodes) == 0:
                        sys.exit(b'Cannot execute run without any memory node.')
                    if not set(memory_nodes).issubset(self.memory_nodes):
                        sys.exit((b'Memory nodes {0} are not allowed to be used').format(list(set(memory_nodes).difference(self.memory_nodes))))
                if workingDir:
                    if not os.path.exists(workingDir):
                        sys.exit((b'Working directory {0} does not exist.').format(workingDir))
                    if not os.path.isdir(workingDir):
                        sys.exit((b'Working directory {0} is not a directory.').format(workingDir))
                    if not os.access(workingDir, os.X_OK):
                        sys.exit((b'Permission denied for working directory {0}.').format(workingDir))
                for (subsystem, option), _ in cgroupValues.items():
                    if subsystem not in self._cgroup_subsystems:
                        sys.exit((b'Cannot set option "{option}" for subsystem "{subsystem}" that is not enabled. Please specify "--require-cgroup-subsystem {subsystem}".').format(option=option, subsystem=subsystem))
                    if not self.cgroups.has_value(subsystem, option):
                        sys.exit((b'Cannot set option "{option}" for subsystem "{subsystem}", it does not exist.').format(option=option, subsystem=subsystem))

            if files_count_limit is not None:
                if files_count_limit < 0:
                    sys.exit((b'Invalid files-count limit {0}.').format(files_count_limit))
            if files_size_limit is not None:
                if files_size_limit < 0:
                    sys.exit((b'Invalid files-size limit {0}.').format(files_size_limit))
            try:
                return self._execute(args, output_filename, error_filename, stdin, write_header, hardtimelimit, softtimelimit, walltimelimit, memlimit, cores, memory_nodes, cgroupValues, environments, workingDir, maxLogfileSize, files_count_limit, files_size_limit, **kwargs)
            except BenchExecException as e:
                logging.critical(b"Cannot execute '%s': %s.", util.escape_string_shell(args[0]), e)
                return {b'terminationreason': b'failed'}
            except OSError as e:
                logging.critical(b"OSError %s while starting '%s' in '%s': %s.", e.errno, util.escape_string_shell(args[0]), workingDir or b'.', e.strerror)
                return {b'terminationreason': b'failed'}

        return

    def _execute(self, args, output_filename, error_filename, stdin, write_header, hardtimelimit, softtimelimit, walltimelimit, memlimit, cores, memory_nodes, cgroup_values, environments, workingDir, max_output_size, files_count_limit, files_size_limit, **kwargs):
        """
        This method executes the command line and waits for the termination of it,
        handling all setup and cleanup, but does not check whether arguments are valid.
        """
        timelimitThread = None
        oomThread = None
        file_hierarchy_limit_thread = None
        if self._energy_measurement is not None:
            if cores is None:
                packages = True
            else:
                all_siblings = set(util.flatten(resources.get_cores_of_same_package_as(core) for core in cores))
                if all_siblings == set(cores):
                    packages = {resources.get_cpu_package_for_core(core) for core in cores}
                else:
                    packages = None

        def preParent():
            """Setup that is executed in the parent process immediately before the actual tool is started."""
            if self._energy_measurement is not None and packages:
                self._energy_measurement.start()
            try:
                starttime = util.read_local_time()
            except AttributeError:
                starttime = None

            walltime_before = util.read_monotonic_time()
            return (starttime, walltime_before)

        def postParent(preParent_result, exit_code, base_path):
            """Cleanup that is executed in the parent process immediately after the actual tool terminated."""
            starttime, walltime_before = preParent_result
            walltime = util.read_monotonic_time() - walltime_before
            energy = self._energy_measurement.stop() if self._energy_measurement else None
            if FREEZER in cgroups:
                cgroups.kill_all_tasks()
            if timelimitThread:
                timelimitThread.cancel()
            if oomThread:
                oomThread.cancel()
            if file_hierarchy_limit_thread:
                file_hierarchy_limit_thread.cancel()
            if exit_code.value not in (0, 1):
                _get_debug_output_after_crash(output_filename, base_path)
            return (starttime, walltime, energy)

        def preSubprocess():
            """Setup that is executed in the forked process before the actual tool is started."""
            os.setpgrp()

        cgroups = self._setup_cgroups(cores, memlimit, memory_nodes, cgroup_values)
        temp_dir = tempfile.mkdtemp(prefix=b'BenchExec_run_')
        run_environment = self._setup_environment(environments)
        outputFile = self._setup_output_file(output_filename, args, write_header=write_header)
        if error_filename is None:
            errorFile = outputFile
        else:
            errorFile = self._setup_output_file(error_filename, args, write_header=write_header)
        pid = None
        returnvalue = 0
        ru_child = None
        self._termination_reason = None
        result = collections.OrderedDict()
        throttle_check = systeminfo.CPUThrottleCheck(cores)
        swap_check = systeminfo.SwapCheck()
        logging.debug(b'Starting process.')
        try:
            pid, result_fn = self._start_execution(args=args, stdin=stdin, stdout=outputFile, stderr=errorFile, env=run_environment, cwd=workingDir, temp_dir=temp_dir, memlimit=memlimit, memory_nodes=memory_nodes, cgroups=cgroups, parent_setup_fn=preParent, child_setup_fn=preSubprocess, parent_cleanup_fn=postParent, **kwargs)
            with self.SUB_PROCESS_PIDS_LOCK:
                self.SUB_PROCESS_PIDS.add(pid)
            timelimitThread = self._setup_cgroup_time_limit(hardtimelimit, softtimelimit, walltimelimit, cgroups, cores, pid)
            oomThread = self._setup_cgroup_memory_limit(memlimit, cgroups, pid)
            file_hierarchy_limit_thread = self._setup_file_hierarchy_limit(files_count_limit, files_size_limit, temp_dir, cgroups, pid)
            returnvalue, ru_child, (starttime, walltime, energy) = result_fn()
            if starttime:
                result[b'starttime'] = starttime
            result[b'walltime'] = walltime
        finally:
            logging.debug(b'Process terminated, exit code %s.', returnvalue)
            with self.SUB_PROCESS_PIDS_LOCK:
                self.SUB_PROCESS_PIDS.discard(pid)
            if timelimitThread:
                timelimitThread.cancel()
            if oomThread:
                oomThread.cancel()
            if file_hierarchy_limit_thread:
                file_hierarchy_limit_thread.cancel()
            cgroups.kill_all_tasks()
            outputFile.close()
            if errorFile is not outputFile:
                errorFile.close()
            self._get_cgroup_measurements(cgroups, ru_child, result)
            logging.debug(b'Cleaning up cgroups.')
            cgroups.remove()
            self._cleanup_temp_dir(temp_dir)
            if timelimitThread:
                _try_join_cancelled_thread(timelimitThread)
            if oomThread:
                _try_join_cancelled_thread(oomThread)
            if file_hierarchy_limit_thread:
                _try_join_cancelled_thread(file_hierarchy_limit_thread)
            if self._energy_measurement:
                self._energy_measurement.stop()

        if throttle_check.has_throttled():
            logging.warning(b'CPU throttled itself during benchmarking due to overheating. Benchmark results are unreliable!')
        if swap_check.has_swapped():
            logging.warning(b'System has swapped during benchmarking. Benchmark results are unreliable!')
        if error_filename is not None:
            _reduce_file_size_if_necessary(error_filename, max_output_size)
        _reduce_file_size_if_necessary(output_filename, max_output_size)
        result[b'exitcode'] = util.ProcessExitCode.from_raw(returnvalue)
        if energy:
            if packages == True:
                result[b'cpuenergy'] = energy
            else:
                result[b'cpuenergy'] = {pkg:energy[pkg] for pkg in energy if pkg in packages}
        if self._termination_reason:
            result[b'terminationreason'] = self._termination_reason
        elif memlimit and b'memory' in result and result[b'memory'] >= memlimit:
            result[b'terminationreason'] = b'memory'
        return result

    def _get_cgroup_measurements(self, cgroups, ru_child, result):
        """
        This method calculates the exact results for time and memory measurements.
        It is not important to call this method as soon as possible after the run.
        """
        logging.debug(b'Getting cgroup measurements.')
        cputime_wait = ru_child.ru_utime + ru_child.ru_stime if ru_child else 0
        cputime_cgroups = None
        if CPUACCT in cgroups:
            tmp = cgroups.read_cputime()
            tmp2 = None
            while tmp != tmp2:
                time.sleep(0.1)
                tmp2 = tmp
                tmp = cgroups.read_cputime()

            cputime_cgroups = tmp
            if cputime_wait > 0.5 and cputime_wait * 0.95 > cputime_cgroups:
                logging.warning(b'Cputime measured by wait was %s, cputime measured by cgroup was only %s, perhaps measurement is flawed.', cputime_wait, cputime_cgroups)
                result[b'cputime'] = cputime_wait
            else:
                result[b'cputime'] = cputime_cgroups
            for core, coretime in enumerate(cgroups.get_value(CPUACCT, b'usage_percpu').split(b' ')):
                try:
                    coretime = int(coretime)
                    if coretime != 0:
                        result[b'cputime-cpu' + str(core)] = coretime / 1000000000
                except (OSError, ValueError) as e:
                    logging.debug(b'Could not read CPU time for core %s from kernel: %s', core, e)

        if MEMORY in cgroups:
            memUsageFile = b'memsw.max_usage_in_bytes'
            if not cgroups.has_value(MEMORY, memUsageFile):
                memUsageFile = b'max_usage_in_bytes'
            if not cgroups.has_value(MEMORY, memUsageFile):
                logging.warning(b'Memory-usage is not available due to missing files.')
            else:
                try:
                    result[b'memory'] = int(cgroups.get_value(MEMORY, memUsageFile))
                except IOError as e:
                    if e.errno == errno.ENOTSUP:
                        logging.critical(b'Kernel does not track swap memory usage, cannot measure memory usage. Please set swapaccount=1 on your kernel command line.')
                    else:
                        raise e

        if BLKIO in cgroups:
            blkio_bytes_file = b'throttle.io_service_bytes'
            if cgroups.has_value(BLKIO, blkio_bytes_file):
                bytes_read = 0
                bytes_written = 0
                for blkio_line in cgroups.get_file_lines(BLKIO, blkio_bytes_file):
                    try:
                        dev_no, io_type, bytes_amount = blkio_line.split(b' ')
                        if io_type == b'Read':
                            bytes_read += int(bytes_amount)
                        elif io_type == b'Write':
                            bytes_written += int(bytes_amount)
                    except ValueError:
                        pass

                result[b'blkio-read'] = bytes_read
                result[b'blkio-write'] = bytes_written
        logging.debug(b'Resource usage of run: walltime=%s, cputime=%s, cgroup-cputime=%s, memory=%s', result.get(b'walltime'), cputime_wait, cputime_cgroups, result.get(b'memory', None))
        return

    def stop(self):
        self._set_termination_reason(b'killed')
        super(RunExecutor, self).stop()


def _reduce_file_size_if_necessary(fileName, maxSize):
    """
    This function shrinks a file.
    We remove only the middle part of a file,
    the file-start and the file-end remain unchanged.
    """
    fileSize = os.path.getsize(fileName)
    if maxSize is None:
        logging.debug(b"Size of logfile '%s' is %s bytes, size limit disabled.", fileName, fileSize)
        return
    else:
        if fileSize < maxSize + 500:
            logging.debug(b"Size of logfile '%s' is %s bytes, nothing to do.", fileName, fileSize)
            return
        logging.warning(b"Logfile '%s' is too big (size %s bytes). Removing lines.", fileName, fileSize)
        util.shrink_text_file(fileName, maxSize, _LOG_SHRINK_MARKER)
        return


def _get_debug_output_after_crash(output_filename, base_path):
    """
    Segmentation faults and some memory failures reference a file
    with more information (hs_err_pid_*). We append this file to the log.
    The format that we expect is a line
    "# An error report file with more information is saved as:"
    and the file name of the dump file on the next line.
    @param output_filename name of log file with tool output
    @param base_path string that needs to be preprended to paths for lookup of files
    """
    logging.debug(b'Analysing output for crash info.')
    foundDumpFile = False
    try:
        with open(output_filename, b'r+b') as (outputFile):
            for line in outputFile:
                if foundDumpFile:
                    dumpFileName = base_path.encode() + line.strip(b' #\n')
                    outputFile.seek(0, os.SEEK_END)
                    try:
                        with open(dumpFileName, b'rb') as (dumpFile):
                            util.copy_all_lines_from_to(dumpFile, outputFile)
                        os.remove(dumpFileName)
                    except IOError as e:
                        logging.warning(b'Could not append additional segmentation fault information from %s (%s)', dumpFileName, e.strerror)

                    break
                try:
                    if line.startswith(b'# An error report file with more information is saved as:'):
                        logging.debug(b'Going to append error report file')
                        foundDumpFile = True
                except UnicodeDecodeError:
                    pass

    except IOError as e:
        logging.warning(b'Could not analyze tool output for crash information (%s)', e.strerror)


def _try_join_cancelled_thread(thread):
    """Join a thread, but if the thread doesn't terminate for some time, ignore it
    instead of waiting infinitely."""
    thread.join(10)
    if thread.is_alive():
        logging.warning(b'Thread %s did not terminate within grace period after cancellation', thread.name)


class _TimelimitThread(threading.Thread):
    """
    Thread that periodically checks whether the given process has already
    reached its timelimit. After this happens, the process is terminated.
    """

    def __init__(self, cgroups, hardtimelimit, softtimelimit, walltimelimit, pid_to_kill, cores, callbackFn=lambda reason: None):
        super(_TimelimitThread, self).__init__()
        self.name = b'TimelimitThread-' + self.name
        assert (hardtimelimit or softtimelimit) and CPUACCT in cgroups
        assert walltimelimit is not None
        if cores:
            self.cpuCount = len(cores)
        else:
            try:
                self.cpuCount = multiprocessing.cpu_count()
            except NotImplementedError:
                self.cpuCount = 1

        self.cgroups = cgroups
        self.timelimit = hardtimelimit or 3153600000
        self.softtimelimit = softtimelimit or 3153600000
        self.latestKillTime = util.read_monotonic_time() + walltimelimit
        self.pid_to_kill = pid_to_kill
        self.callback = callbackFn
        self.finished = threading.Event()
        return

    def read_cputime(self):
        while True:
            try:
                return self.cgroups.read_cputime()
            except ValueError:
                time.sleep(1)

    def run(self):
        while not self.finished.is_set():
            usedCpuTime = self.read_cputime() if CPUACCT in self.cgroups else 0
            remainingCpuTime = self.timelimit - usedCpuTime
            remainingSoftCpuTime = self.softtimelimit - usedCpuTime
            remainingWallTime = self.latestKillTime - util.read_monotonic_time()
            logging.debug(b'TimelimitThread for process %s: used CPU time: %s, remaining CPU time: %s, remaining soft CPU time: %s, remaining wall time: %s.', self.pid_to_kill, usedCpuTime, remainingCpuTime, remainingSoftCpuTime, remainingWallTime)
            if remainingCpuTime <= 0:
                self.callback(b'cputime')
                logging.debug(b'Killing process %s due to CPU time timeout.', self.pid_to_kill)
                util.kill_process(self.pid_to_kill)
                self.finished.set()
                return
            if remainingWallTime <= 0:
                self.callback(b'walltime')
                logging.warning(b'Killing process %s due to wall time timeout.', self.pid_to_kill)
                util.kill_process(self.pid_to_kill)
                self.finished.set()
                return
            if remainingSoftCpuTime <= 0:
                self.callback(b'cputime-soft')
                util.kill_process(self.pid_to_kill, signal.SIGTERM)
                self.softtimelimit = self.timelimit
            remainingTime = min(remainingCpuTime / self.cpuCount, remainingSoftCpuTime / self.cpuCount, remainingWallTime)
            self.finished.wait(remainingTime + 1)

    def cancel(self):
        self.finished.set()


if __name__ == b'__main__':
    main()