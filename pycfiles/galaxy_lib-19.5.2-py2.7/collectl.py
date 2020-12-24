# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/jobs/metrics/instrumenters/collectl.py
# Compiled at: 2018-09-15 08:40:24
"""The module describes the ``collectl`` job metrics plugin."""
import logging, os, shutil
from galaxy import util
from . import InstrumentPlugin
from .. import formatting
from ..collectl import cli, processes, subsystems
log = logging.getLogger(__name__)
DEFAULT_PROCFILT_ON = 'username'
DEFAULT_SUBSYSTEMS = 'process'
DEFAULT_FLUSH_INTERVAL = '0'
FORMATTED_RESOURCE_TITLES = {'PCT': 'Percent CPU Usage', 
   'RSYS': 'Disk Reads', 
   'WSYS': 'Disk Writes'}
EMPTY_COLLECTL_FILE_MESSAGE = 'Skipping process summary due to empty file... job probably did not run long enough for collectl to gather data.'

class CollectlFormatter(formatting.JobMetricFormatter):

    def format(self, key, value):
        if key == 'pid':
            return ('Process ID', int(value))
        else:
            if key == 'raw_log_path':
                return ('Relative Path of Full Collectl Log', value)
            if key == 'process_max_AccumT':
                return ('Job Runtime (System+User)', formatting.seconds_to_str(float(value)))
            _, stat_type, resource_type = key.split('_', 2)
            if resource_type.startswith('Vm'):
                value_str = '%s KB' % int(value)
            elif resource_type in ('RSYS', 'WSYS') and stat_type in ('count', 'max',
                                                                     'sum'):
                value_str = '%d (# system calls)' % int(value)
            else:
                value_str = str(value)
            resource_title = FORMATTED_RESOURCE_TITLES.get(resource_type, resource_type)
            return ('%s (%s)' % (resource_title, stat_type), value_str)


class CollectlPlugin(InstrumentPlugin):
    """ Run collectl along with job to capture system and/or process data
    according to specified collectl subsystems.
    """
    plugin_type = 'collectl'
    formatter = CollectlFormatter()

    def __init__(self, **kwargs):
        self.__configure_paths(kwargs)
        self.__configure_subsystems(kwargs)
        saved_logs_path = kwargs.get('saved_logs_path', '')
        if 'app' in kwargs:
            log.debug('Found path for saved logs: %s' % saved_logs_path)
            saved_logs_path = kwargs['app'].config.resolve_path(saved_logs_path)
        self.saved_logs_path = saved_logs_path
        self.__configure_collectl_recorder_args(kwargs)
        self.summarize_process_data = util.asbool(kwargs.get('summarize_process_data', True))
        self.log_collectl_program_output = util.asbool(kwargs.get('log_collectl_program_output', False))
        if self.summarize_process_data:
            if subsystems.get_subsystem('process') not in self.subsystems:
                raise Exception('Collectl plugin misconfigured - cannot summarize_process_data without process subsystem being enabled.')
            process_statistics = kwargs.get('process_statistics', None)
            self.process_statistics = processes.parse_process_statistics(process_statistics)
        return

    def pre_execute_instrument(self, job_directory):
        commands = []
        commands.append('echo "$$" > \'%s\' ' % self.__pid_file(job_directory))
        commands.append(self.__collectl_record_command(job_directory))
        return commands

    def post_execute_instrument(self, job_directory):
        commands = []
        return commands

    def job_properties(self, job_id, job_directory):
        pid = open(self.__pid_file(job_directory), 'r').read().strip()
        contents = os.listdir(job_directory)
        try:
            rel_path = filter(self._is_instrumented_collectl_log, contents)[0]
            path = os.path.join(job_directory, rel_path)
        except IndexError:
            message = 'Failed to find collectl log in directory %s, files were %s' % (job_directory, contents)
            raise Exception(message)

        properties = dict(pid=int(pid))
        if self.saved_logs_path:
            destination_rel_dir = os.path.join(*util.directory_hash_id(job_id))
            destination_rel_path = os.path.join(destination_rel_dir, rel_path)
            destination_path = os.path.join(self.saved_logs_path, destination_rel_path)
            destination_dir = os.path.dirname(destination_path)
            if not os.path.isdir(destination_dir):
                os.makedirs(destination_dir)
            shutil.copyfile(path, destination_path)
            properties['raw_log_path'] = destination_rel_path
        if self.summarize_process_data:
            summary_statistics = self.__summarize_process_data(pid, path)
            for statistic, value in summary_statistics:
                properties['process_%s' % ('_').join(statistic)] = value

        return properties

    def __configure_paths(self, kwargs):
        collectl_path = kwargs.get('collectl_path', 'collectl')
        self.remote_collectl_path = kwargs.get('remote_collectl_path', collectl_path)
        self.local_collectl_path = kwargs.get('local_collectl_path', collectl_path)

    def __configure_subsystems(self, kwargs):
        raw_subsystems_str = kwargs.get('subsystems', DEFAULT_SUBSYSTEMS)
        raw_subsystems = util.listify(raw_subsystems_str, do_strip=True)
        self.subsystems = [ subsystems.get_subsystem(_) for _ in raw_subsystems ]

    def __configure_collectl_recorder_args(self, kwargs):
        collectl_recorder_args = kwargs.copy()
        if 'interval' in kwargs and 'interval2' not in kwargs:
            collectl_recorder_args['interval2'] = kwargs['interval']
        if 'flush' not in kwargs:
            collectl_recorder_args['flush'] = DEFAULT_FLUSH_INTERVAL
        procfilt_on = kwargs.get('procfilt_on', DEFAULT_PROCFILT_ON).lower()
        explicit_args = dict(collectl_path=self.remote_collectl_path, procfilt=procfilt_argument(procfilt_on), subsystems=self.subsystems)
        collectl_recorder_args.update(explicit_args)
        self.collectl_recorder_args = collectl_recorder_args

    def __summarize_process_data(self, pid, collectl_log_path):
        playback_cli_args = dict(collectl_path=self.local_collectl_path, playback_path=collectl_log_path, sep='9')
        if not os.stat(collectl_log_path).st_size:
            log.debug(EMPTY_COLLECTL_FILE_MESSAGE)
            return []
        playback_cli = cli.CollectlCli(**playback_cli_args)
        return processes.generate_process_statistics(playback_cli, pid, self.process_statistics)

    def __collectl_recorder_cli(self, job_directory):
        cli_args = self.collectl_recorder_args.copy()
        cli_args['destination_path'] = self._instrument_file_path(job_directory, 'log')
        return cli.CollectlCli(**cli_args)

    def __collectl_record_command(self, job_directory):
        collectl_cli = self.__collectl_recorder_cli(job_directory)
        if self.log_collectl_program_output:
            redirect_to = self._instrument_file_path(job_directory, 'program_output')
        else:
            redirect_to = '/dev/null'
        return '%s > %s 2>&1 &' % (
         collectl_cli.build_command_line(),
         redirect_to)

    def __pid_file(self, job_directory):
        return self._instrument_file_path(job_directory, 'pid')

    def _is_instrumented_collectl_log(self, filename):
        prefix = self._instrument_file_name('log')
        return filename.startswith(prefix) and filename.endswith('.raw.gz')


def procfilt_argument(procfilt_on):
    if procfilt_on == 'username':
        return 'U$USER'
    else:
        if procfilt_on == 'uid':
            return 'u$UID'
        if procfilt_on or procfilt_on.lower() != 'none':
            raise Exception('Invalid procfilt_on argument encountered')
        return ''


__all__ = ('CollectlPlugin', )