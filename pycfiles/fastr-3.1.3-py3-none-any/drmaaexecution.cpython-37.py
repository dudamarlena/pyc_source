# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/drmaaexecution.py
# Compiled at: 2019-10-16 09:10:20
# Size of source mod 2**32: 26237 bytes
import os, queue, sys, threading, time
from bidict import bidict
import fastr
from fastr import exceptions
from fastr.abc.baseplugin import PluginState
try:
    import drmaa
    load_drmaa = True
except (ImportError, RuntimeError, OSError):
    load_drmaa = False

from fastr.execution.job import JobState
from fastr.plugins.executionplugin import ExecutionPlugin
import fastr.helpers.classproperty as classproperty

class FastrDRMAANotFoundError(exceptions.FastrImportError):
    __doc__ = '\n    Indicate the DRMAA module was not found on the system.\n    '


class FastrDRMAANotFunctionalError(exceptions.FastrError):
    __doc__ = '\n    Indicate DRMAA is found but creating a session did not work\n    '


class DRMAAExecution(ExecutionPlugin):
    __doc__ = '\n    A DRMAA execution plugin to execute Jobs on a Grid Engine cluster. It uses\n    a configuration option for selecting the queue to submit to. It uses the\n    python ``drmaa`` package.\n\n    .. note::\n\n        To use this plugin, make sure the ``drmaa`` package is installed and\n        that the execution is started on an SGE submit host with DRMAA\n        libraries installed.\n\n    .. note::\n\n        This plugin is at the moment tailored to SGE, but it should be fairly\n        easy to make different subclasses for different DRMAA supporting\n        systems.\n    '
    if not load_drmaa:
        _status = (
         PluginState.failed, 'Could not load DRMAA module required for cluster communication')
    SUPPORTS_CANCEL = True
    SUPPORTS_DEPENDENCY = True
    SUPPORTS_HOLD_RELEASE = True
    CANCELS_DEPENDENCIES = False
    GE_NATIVE_SPEC = {'CWD':'-cwd', 
     'QUEUE':'-q {queue}', 
     'WALLTIME':'-l h_rt={walltime}', 
     'MEMORY':'-l h_vmem={memory}', 
     'NCORES':'-pe smp {ncores:d}', 
     'OUTPUTLOG':'-o {outputlog}', 
     'ERRORLOG':'-e {errorlog}', 
     'DEPENDS':'-hold_jid {hold_list}', 
     'DEPENDS_SEP':',', 
     'HOLD':'-h'}
    TORQUE_NATIVE_SPEC = {'CWD':'', 
     'QUEUE':'-q {queue}', 
     'WALLTIME':'-l walltime={walltime}', 
     'MEMORY':'-l mem={memory}', 
     'NCORES':'-l procs={ncores:d}', 
     'OUTPUTLOG':'-o {outputlog}', 
     'ERRORLOG':'-e {errorlog}', 
     'DEPENDS':'-W depend=afterok:{hold_list}', 
     'DEPENDS_SEP':':', 
     'HOLD':'-h'}
    NATIVE_SPEC = {'grid_engine':GE_NATIVE_SPEC, 
     'torque':TORQUE_NATIVE_SPEC}

    def __init__(self, finished_callback=None, cancelled_callback=None):
        super(DRMAAExecution, self).__init__(finished_callback, cancelled_callback)
        self.default_queue = fastr.config.drmaa_queue
        self.max_jobs = fastr.config.drmaa_max_jobs
        self.engine = fastr.config.drmaa_engine
        self.regression_check_interval = fastr.config.drmaa_job_check_interval
        self.num_undetermined_to_fail = fastr.config.drmaa_num_undetermined_to_fail
        try:
            self.session = drmaa.Session()
            self.session.initialize()
        except drmaa.errors.DrmaaException as exception:
            try:
                raise FastrDRMAANotFunctionalError('Encountered an error when creating DRMAA session: [{}] {}'.format(exception.__class__, str(exception)))
            finally:
                exception = None
                del exception

        fastr.log.debug('A DRMAA session was started successfully')
        response = self.session.contact
        fastr.log.debug('session contact returns: ' + response)
        self.job_lookup_fastr_drmaa = bidict()
        self.job_lookup_lock = threading.Lock()
        self.undetermined_jobs = {}
        self.submit_queue = queue.Queue()
        self.finished_queue = queue.Queue()
        self.last_thread_check = time.time()
        self.thread_check_lock = threading.Lock()
        self.collector_thread = None
        self.callback_thread = None
        self.submitter_thread = None
        self.checker_thread = None
        self.ensure_threads()

    def check_threads(self):
        """
        Check if the threads are still alive, but make sure it is only done once per minute
        """
        with self.thread_check_lock:
            if time.time() - self.last_thread_check < 60:
                return
            self.last_thread_check = time.time()
            self.ensure_threads()

    def ensure_threads(self):
        """
        Start thread if not defined, or restart if they somehow died accidentallyy
        """
        if not self.running:
            return
            if not (self.collector_thread is None or self.collector_thread.is_alive()):
                fastr.log.debug('Creating job collector')
                self.collector_thread = threading.Thread(name='DRMAAJobCollector-0', target=(self.collect_jobs), args=())
                self.collector_thread.daemon = True
                fastr.log.debug('Starting job collector')
                self.collector_thread.start()
            self.callback_thread is None or self.callback_thread.is_alive() or fastr.log.debug('Creating job callback processor')
            self.callback_thread = threading.Thread(name='DRMAAJobCallback-0', target=(self.dispatch_callbacks), args=())
            self.callback_thread.daemon = True
            fastr.log.debug('Starting job callback processor')
            self.callback_thread.start()
        else:
            if not (self.submitter_thread is None or self.submitter_thread.is_alive()):
                fastr.log.debug('Creating job submitter')
                self.submitter_thread = threading.Thread(name='DRMAAJobSubmitter-0', target=(self.submit_jobs), args=())
                self.submitter_thread.daemon = True
                fastr.log.debug('Starting job submitter')
                self.submitter_thread.start()
            self.checker_thread is None or self.checker_thread.is_alive() or fastr.log.debug('Creating job regression checker')
            self.checker_thread = threading.Thread(name='DRMAAJobChecker-0', target=(self.regression_check), args=())
            self.checker_thread.daemon = True
            fastr.log.debug('Starting job regression checker')
            self.checker_thread.start()

    @classproperty
    def configuration_fields(cls):
        return {'drmaa_queue':(
          str, 'week', 'The default queue to use for jobs send to the scheduler'), 
         'drmaa_max_jobs':(
          int, 0, 'The maximum jobs that can be send to the scheduler at the same time (0 for no limit)'), 
         'drmaa_engine':(
          str, 'grid_engine', 'The engine to use (options: grid_engine, torque'), 
         'drmaa_job_check_interval':(
          int, 900, 'The interval in which the job checker will start to check for stale jobs'), 
         'drmaa_num_undetermined_to_fail':(
          int, 3, 'Number of consecutive times a job state has be undetermined to be considered to have failed')}

    @classmethod
    def test(cls):
        if not load_drmaa:
            raise FastrDRMAANotFoundError('Could not import the required drmaa for this plugin')

    @property
    def spec_fields(self):
        return self.NATIVE_SPEC[self.engine]

    @property
    def n_current_jobs(self):
        return len(self.job_lookup_fastr_drmaa)

    def cleanup(self):
        super(DRMAAExecution, self).cleanup()
        while self.n_current_jobs > 0:
            with self.job_lookup_lock:
                fastr_job_id, drmaa_job_id = self.job_lookup_fastr_drmaa.popitem()
            fastr.log.info('Terminating left-over job {}'.format(drmaa_job_id))
            self._terminate_job(drmaa_job_id, retry=0)

        fastr.log.debug('Stopping DRMAA executor')
        try:
            self.session.exit()
            fastr.log.debug('Exiting DRMAA session')
        except drmaa.NoActiveSessionException:
            pass

        if self.collector_thread.is_alive():
            fastr.log.debug('Terminating job collector thread')
            self.collector_thread.join()
        if self.submitter_thread.is_alive():
            fastr.log.debug('Terminating job submitter thread')
            self.submitter_thread.join()
        if self.checker_thread.is_alive():
            fastr.log.debug('Terminating job checker thread')
            self.checker_thread.join()
        if self.callback_thread.is_alive():
            fastr.log.debug('Terminating job callback thread')
            self.callback_thread.join()
        fastr.log.debug('DRMAA executor stopped!')

    def _queue_job(self, job):
        self.submit_queue.put(job, block=True)

    def _terminate_job(self, drmaa_job_id: int, retry=1):
        try:
            self.session.control(drmaa_job_id, drmaa.JobControlAction.TERMINATE)
        except (drmaa.InvalidJobException, drmaa.InternalException) as exception:
            try:
                new_status = self._get_job_state(drmaa_job_id)
                if new_status not in [drmaa.JobState.UNDETERMINED,
                 drmaa.JobState.DONE,
                 drmaa.JobState.FAILED]:
                    if retry > 0:
                        self._terminate_job(drmaa_job_id, retry=(retry - 1))
                        return
                    fastr.log.warning(f"Encountered a DRMAA exception: [{type(exception).__name__}] {exception}")
            finally:
                exception = None
                del exception

        except Exception as exception:
            try:
                fastr.log.error(f"Encountered an exception during cancellation of job {drmaa_job_id}: [{type(exception).__name__}] {exception}")
            finally:
                exception = None
                del exception

    def _cancel_job(self, job, retry=True):
        with self.job_lookup_lock:
            drmaa_job_id = self.job_lookup_fastr_drmaa.pop(job.id, None)
        if drmaa_job_id is None:
            fastr.log.info('Job {} not found in DRMAA lookup, no longer exists?'.format(job.id))
            return
        fastr.log.debug('Cancelling job {}'.format(drmaa_job_id))
        self._terminate_job(drmaa_job_id)
        self.job_finished(job, errors=[exceptions.FastrError('job cancelled by fastr DRMAA plugin').excerpt()])

    def _hold_job(self, job):
        drmaa_job_id = self.job_lookup_fastr_drmaa.get(job.id, None)
        if drmaa_job_id:
            try:
                self.session.control(drmaa_job_id, drmaa.JobControlAction.HOLD)
            except Exception as exception:
                try:
                    fastr.log.error(f"Encountered an exception during setting job {drmaa_job_id} to hold: [{type(exception).__name__}] {exception}")
                finally:
                    exception = None
                    del exception

        else:
            fastr.log.error('Cannot hold job {}, cannot find the drmaa id!'.format(job.id))

    def _release_job(self, job):
        drmaa_job_id = self.job_lookup_fastr_drmaa.get(job.id, None)
        if drmaa_job_id:
            try:
                self.session.control(drmaa_job_id, drmaa.JobControlAction.RELEASE)
            except Exception as exception:
                try:
                    fastr.log.error(f"Encountered an exception during releasing job {drmaa_job_id}: [{type(exception).__name__}] {exception}")
                finally:
                    exception = None
                    del exception

        else:
            fastr.log.error('Cannot release job {}, cannot find the drmaa id!'.format(job.id))

    def _job_finished(self, result):
        pass

    def create_native_spec(self, queue, walltime, memory, ncores, outputLog, errorLog, hold_job, hold):
        """
        Create the native spec for the DRMAA scheduler. Needs to be implemented
        in the subclasses

        :param str queue: the queue to submit to
        :param str walltime: walltime specified
        :param str memory: memory requested
        :param int ncores: number of cores requested
        :param str outputLog: the location of the stdout log
        :param str errorLog: the location of stderr log
        :param list hold_job: list of jobs to depend on
        :param bool hold: flag if job should be submitted in hold mode
        :return:
        """
        native_spec = []
        native_spec.append(self.spec_fields['CWD'].format(os.path.abspath(os.curdir)))
        native_spec.append(self.spec_fields['QUEUE'].format(queue=queue))
        if walltime is not None:
            native_spec.append(self.spec_fields['WALLTIME'].format(walltime=walltime))
        if memory is not None:
            native_spec.append(self.spec_fields['MEMORY'].format(memory=memory))
        elif ncores is not None:
            if ncores > 1:
                native_spec.append(self.spec_fields['NCORES'].format(ncores=ncores))
        elif outputLog is not None:
            native_spec.append(self.spec_fields['OUTPUTLOG'].format(outputlog=outputLog))
        else:
            if errorLog is not None:
                native_spec.append(self.spec_fields['ERRORLOG'].format(errorlog=errorLog))
            if hold_job is not None:
                if isinstance(hold_job, int):
                    native_spec.append(self.spec_fields['DEPENDS'].format(hold_list=hold_job))
                else:
                    if isinstance(hold_job, list) or isinstance(hold_job, tuple):
                        if len(hold_job) > 0:
                            jid_list = self.spec_fields['DEPENDS_SEP'].join([str(x) for x in hold_job])
                            native_spec.append(self.spec_fields['DEPENDS'].format(hold_list=jid_list))
                    else:
                        fastr.log.error('Incorrect hold_job type!')
        if hold:
            native_spec.append(self.spec_fields['HOLD'])
        return ' '.join(native_spec)

    def send_job(self, command, arguments, queue=None, resources=None, job_name=None, joinLogFiles=False, outputLog=None, errorLog=None, hold_job=None, hold=False):
        jt = self.session.createJobTemplate()
        jt.remoteCommand = command
        jt.args = arguments
        jt.joinFiles = joinLogFiles
        env = os.environ
        env.pop('BASH_FUNC_module()', None)
        env['PBS_O_INITDIR'] = os.path.abspath(os.curdir)
        jt.jobEnvironment = env
        if queue is None:
            queue = self.default_queue
        else:
            if resources.time:
                hours = resources.time // 3600
                minutes = resources.time % 3600 // 60
                seconds = resources.time % 60
                walltime = '{}:{:02d}:{:02d}'.format(hours, minutes, seconds)
            else:
                walltime = None
            if resources.memory:
                memory = '{}M'.format(resources.memory)
            else:
                memory = None
        native_spec = self.create_native_spec(queue=queue,
          walltime=walltime,
          memory=memory,
          ncores=(resources.cores),
          outputLog=outputLog,
          errorLog=errorLog,
          hold_job=hold_job,
          hold=hold)
        fastr.log.debug('Setting native spec to: {}'.format(native_spec))
        jt.nativeSpecification = native_spec
        if job_name is None:
            job_name = command
            job_name = job_name.replace(' ', '_')
            job_name = job_name.replace('"', '')
            if len(job_name) > 32:
                job_name = job_name[0:32]
        jt.jobName = job_name
        job_id = self.session.runJob(jt)
        self.session.deleteJobTemplate(jt)
        return job_id

    def submit_jobs(self):
        while self.running:
            try:
                self.check_threads()
                if 0 < self.max_jobs <= self.n_current_jobs:
                    time.sleep(1)
                    continue
                job = self.submit_queue.get(block=True, timeout=2)
                command = [
                 sys.executable,
                 os.path.join(fastr.config.executionscript),
                 job.commandfile]
                fastr.log.debug('Command to queue: {}'.format(command))
                if not self.running:
                    break
                fastr.log.debug('Queueing {} [{}] via DRMAA'.format(job.id, job.status))
                cl_job_id = self.send_job((command[0]), (command[1:]), job_name=('fastr_{}'.format(job.id)),
                  resources=(job.resources),
                  outputLog=(job.stdoutfile),
                  errorLog=(job.stderrfile),
                  hold_job=[self.job_lookup_fastr_drmaa[x] for x in job.hold_jobs if x in self.job_lookup_fastr_drmaa],
                  hold=(job.status == JobState.hold))
                with self.job_lookup_lock:
                    self.job_lookup_fastr_drmaa[job.id] = cl_job_id
                self.submit_queue.task_done()
                fastr.log.info('Job {} queued via DRMAA as {}'.format(job.id, cl_job_id))
            except queue.Empty:
                pass

        fastr.log.info('DRMAA submission thread ended!')

    def collect_jobs(self):
        while self.running:
            try:
                self.check_threads()
                info = self.session.wait(drmaa.Session.JOB_IDS_SESSION_ANY, 2)
            except drmaa.ExitTimeoutException:
                pass
            except drmaa.InvalidJobException:
                fastr.log.debug('No jobs left (session queue appears to be empty)')
                time.sleep(2)
            except drmaa.NoActiveSessionException:
                self.running = False
                if not self.running:
                    fastr.log.debug('DRMAA session no longer active, quiting collector...')
                else:
                    fastr.log.critical('DRMAA session no longer active, but DRMAA executor not stopped properly! Quitting')
            except drmaa.errors.DrmaaException as exception:
                try:
                    fastr.log.warning('Encountered unexpected DRMAA exception: {}'.format(exception))
                finally:
                    exception = None
                    del exception

            except Exception as exception:
                try:
                    if exceptions.get_message(exception).startswith('code 24:'):
                        fastr.log.warning('Encountered (probably harmless) DRMAA exception: {}'.format(exception))
                    else:
                        fastr.log.error('Encountered unexpected exception: {}'.format(exception))
                finally:
                    exception = None
                    del exception

            else:
                self.finished_queue.put(info, block=True)

        fastr.log.info('DRMAA collect jobs thread ended!')

    def dispatch_callbacks(self):
        while self.running:
            try:
                self.check_threads()
                info = self.finished_queue.get(block=True, timeout=2)
                if not self.running:
                    break
                else:
                    fastr.log.debug('Cluster DRMAA job {} finished'.format(info.jobId))
                    errors = []
                    with self.job_lookup_lock:
                        job_id = self.job_lookup_fastr_drmaa.inv.pop(info.jobId, None)
                    job = self.job_dict.get(job_id, None)
                    if info.hasSignal:
                        errors.append(exceptions.FastrError('Job exited because of a signal, this might indicate it got killed because it attempted to use too much memory (or other resources)').excerpt())
                    self.finished_queue.task_done()
                    if job is not None:
                        self.job_finished(job, errors=errors)
                    else:
                        fastr.log.warning('Job {} no longer available (got cancelled/processed already?)'.format(info.jobId))
            except queue.Empty:
                pass

        fastr.log.info('DRMAA dispatch callback thread ended!')

    def _get_job_state(self, drmaa_job_id: int) -> 'drmaa.JobState':
        try:
            return self.session.jobStatus(drmaa_job_id)
        except drmaa.errors.InvalidJobException:
            return drmaa.JobState.UNDETERMINED
        except Exception as exception:
            try:
                fastr.log.error(f"Encountered an exception during getting state for job {drmaa_job_id}: [{type(exception).__name__}] {exception}")
                return drmaa.JobState.UNDETERMINED
            finally:
                exception = None
                del exception

    def regression_check--- This code section failed: ---

 L. 569         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'last_update'

 L. 571         8  SETUP_LOOP          264  'to 264'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                running
            14_16  POP_JUMP_IF_FALSE   262  'to 262'

 L. 572        18  LOAD_FAST                'self'
               20  LOAD_METHOD              check_threads
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  POP_TOP          

 L. 573        26  LOAD_GLOBAL              time
               28  LOAD_METHOD              time
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  LOAD_FAST                'last_update'
               34  BINARY_SUBTRACT  
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                regression_check_interval
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE   110  'to 110'

 L. 576        44  LOAD_FAST                'self'
               46  LOAD_ATTR                undetermined_jobs
               48  POP_JUMP_IF_FALSE    98  'to 98'

 L. 577        50  LOAD_GLOBAL              list
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                undetermined_jobs
               56  LOAD_METHOD              keys
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  STORE_FAST               'undetermined_jobs'

 L. 579        64  SETUP_LOOP          108  'to 108'
               66  LOAD_FAST                'undetermined_jobs'
               68  GET_ITER         
               70  FOR_ITER             94  'to 94'
               72  STORE_FAST               'drmaa_job_id'

 L. 580        74  LOAD_FAST                'self'
               76  LOAD_ATTR                running
               78  POP_JUMP_IF_TRUE     82  'to 82'

 L. 581        80  BREAK_LOOP       
             82_0  COME_FROM            78  '78'

 L. 583        82  LOAD_FAST                'self'
               84  LOAD_METHOD              _job_regression_check
               86  LOAD_FAST                'drmaa_job_id'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          
               92  JUMP_BACK            70  'to 70'
               94  POP_BLOCK        
               96  JUMP_BACK            10  'to 10'
             98_0  COME_FROM            48  '48'

 L. 585        98  LOAD_GLOBAL              time
              100  LOAD_METHOD              sleep
              102  LOAD_CONST               1
              104  CALL_METHOD_1         1  '1 positional argument'
              106  POP_TOP          
            108_0  COME_FROM_LOOP       64  '64'

 L. 586       108  CONTINUE             10  'to 10'
            110_0  COME_FROM            42  '42'

 L. 588       110  LOAD_GLOBAL              time
              112  LOAD_METHOD              time
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  STORE_FAST               'last_update'

 L. 590       118  LOAD_GLOBAL              list
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                job_lookup_fastr_drmaa
              124  LOAD_METHOD              values
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  STORE_FAST               'jobs_to_check'

 L. 591       132  LOAD_GLOBAL              fastr
              134  LOAD_ATTR                log
              136  LOAD_METHOD              info
              138  LOAD_STR                 'Running job regression check, '
              140  LOAD_GLOBAL              len
              142  LOAD_FAST                'jobs_to_check'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  FORMAT_VALUE          0  ''
              148  LOAD_STR                 ' job(s) to be checked'
              150  BUILD_STRING_3        3 
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          

 L. 592       156  LOAD_GLOBAL              fastr
              158  LOAD_ATTR                log
              160  LOAD_METHOD              info
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                submit_queue
              166  LOAD_METHOD              qsize
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  FORMAT_VALUE          0  ''
              172  LOAD_STR                 ' waiting to be submitted'
              174  BUILD_STRING_2        2 
              176  CALL_METHOD_1         1  '1 positional argument'
              178  POP_TOP          

 L. 593       180  LOAD_GLOBAL              fastr
              182  LOAD_ATTR                log
              184  LOAD_METHOD              info
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                finished_queue
              190  LOAD_METHOD              qsize
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  FORMAT_VALUE          0  ''
              196  LOAD_STR                 ' waiting finished and waiting to be processed'
              198  BUILD_STRING_2        2 
              200  CALL_METHOD_1         1  '1 positional argument'
              202  POP_TOP          

 L. 594       204  LOAD_GLOBAL              fastr
              206  LOAD_ATTR                log
              208  LOAD_METHOD              info
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                callback_queue
              214  LOAD_METHOD              qsize
              216  CALL_METHOD_0         0  '0 positional arguments'
              218  FORMAT_VALUE          0  ''
              220  LOAD_STR                 ' waiting waiting for the final callback processing'
              222  BUILD_STRING_2        2 
              224  CALL_METHOD_1         1  '1 positional argument'
              226  POP_TOP          

 L. 596       228  SETUP_LOOP          260  'to 260'
              230  LOAD_FAST                'jobs_to_check'
              232  GET_ITER         
              234  FOR_ITER            258  'to 258'
              236  STORE_FAST               'drmaa_job_id'

 L. 597       238  LOAD_FAST                'self'
              240  LOAD_ATTR                running
              242  POP_JUMP_IF_TRUE    246  'to 246'

 L. 598       244  BREAK_LOOP       
            246_0  COME_FROM           242  '242'

 L. 600       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _job_regression_check
              250  LOAD_FAST                'drmaa_job_id'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          
              256  JUMP_BACK           234  'to 234'
              258  POP_BLOCK        
            260_0  COME_FROM_LOOP      228  '228'
              260  JUMP_BACK            10  'to 10'
            262_0  COME_FROM            14  '14'
              262  POP_BLOCK        
            264_0  COME_FROM_LOOP        8  '8'

Parse error at or near `CONTINUE' instruction at offset 108

    def _job_regression_check(self, drmaa_job_id: int):
        status = self._get_job_state(drmaa_job_id)
        if status == drmaa.JobState.UNDETERMINED:
            undetermined_count = self.undetermined_jobs.get(drmaa_job_id, 0) + 1
            if undetermined_count < self.num_undetermined_to_fail:
                self.undetermined_jobs[drmaa_job_id] = undetermined_count
                fastr.log.info(f"Job {drmaa_job_id} status could not determined {undetermined_count} times")
                return
        self.undetermined_jobs.pop(drmaa_job_id, 0)
        if status not in [drmaa.JobState.DONE,
         drmaa.JobState.FAILED,
         drmaa.JobState.UNDETERMINED]:
            return
        fastr.log.info(f"Job {drmaa_job_id} is {status}, calling finished callback")
        with self.job_lookup_lock:
            job_id = self.job_lookup_fastr_drmaa.inv.pop(drmaa_job_id, None)
        job = self.job_dict.get(job_id, None)
        if job is None:
            fastr.log.warning(f"Could not find connected fastr job for {drmaa_job_id}")
            return
        self.job_finished(job,
          errors=[
         exceptions.FastrError('Job collected by the job status checking rather then getting a callback from DRMAA.').excerpt()])