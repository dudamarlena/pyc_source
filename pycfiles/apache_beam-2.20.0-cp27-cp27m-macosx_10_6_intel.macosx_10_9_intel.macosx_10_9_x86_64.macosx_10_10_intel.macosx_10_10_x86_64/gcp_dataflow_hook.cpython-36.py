# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_dataflow_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11907 bytes
import json, re, select, subprocess, time, uuid
from googleapiclient.discovery import build
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook
from airflow.utils.log.logging_mixin import LoggingMixin
DEFAULT_DATAFLOW_LOCATION = 'us-central1'

class _DataflowJob(LoggingMixin):

    def __init__(self, dataflow, project_number, name, location, poll_sleep=10, job_id=None, num_retries=None):
        self._dataflow = dataflow
        self._project_number = project_number
        self._job_name = name
        self._job_location = location
        self._job_id = job_id
        self._num_retries = num_retries
        self._job = self._get_job()
        self._poll_sleep = poll_sleep

    def _get_job_id_from_name(self):
        jobs = self._dataflow.projects().locations().jobs().list(projectId=(self._project_number),
          location=(self._job_location)).execute(num_retries=(self._num_retries))
        for job in jobs['jobs']:
            if job['name'].lower() == self._job_name.lower():
                self._job_id = job['id']
                return job

    def _get_job(self):
        if self._job_id:
            job = self._dataflow.projects().locations().jobs().get(projectId=(self._project_number),
              location=(self._job_location),
              jobId=(self._job_id)).execute(num_retries=(self._num_retries))
        else:
            if self._job_name:
                job = self._get_job_id_from_name()
            else:
                raise Exception('Missing both dataflow job ID and name.')
            if job:
                if 'currentState' in job:
                    self.log.info('Google Cloud DataFlow job %s is %s', job['name'], job['currentState'])
            if job:
                self.log.info('Google Cloud DataFlow with job_id %s has name %s', self._job_id, job['name'])
            else:
                self.log.info('Google Cloud DataFlow job not available yet..')
        return job

    def wait_for_done(self):
        while self._job:
            if 'currentState' in self._job:
                if 'JOB_STATE_DONE' == self._job['currentState']:
                    return True
                elif 'JOB_STATE_RUNNING' == self._job['currentState']:
                    if 'JOB_TYPE_STREAMING' == self._job['type']:
                        return True
                else:
                    if 'JOB_STATE_FAILED' == self._job['currentState']:
                        raise Exception('Google Cloud Dataflow job {} has failed.'.format(self._job['name']))
                    else:
                        if 'JOB_STATE_CANCELLED' == self._job['currentState']:
                            raise Exception('Google Cloud Dataflow job {} was cancelled.'.format(self._job['name']))
                        else:
                            if 'JOB_STATE_RUNNING' == self._job['currentState']:
                                time.sleep(self._poll_sleep)
                            else:
                                if 'JOB_STATE_PENDING' == self._job['currentState']:
                                    time.sleep(15)
                                else:
                                    self.log.debug(str(self._job))
                                    raise Exception('Google Cloud Dataflow job {} was unknown state: {}'.format(self._job['name'], self._job['currentState']))
            else:
                time.sleep(15)
            self._job = self._get_job()

    def get(self):
        return self._job


class _Dataflow(LoggingMixin):

    def __init__(self, cmd):
        self.log.info('Running command: %s', ' '.join(cmd))
        self._proc = subprocess.Popen(cmd,
          shell=False,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          close_fds=True)

    def _line(self, fd):
        if fd == self._proc.stderr.fileno():
            line = ''.join(self._proc.stderr.readlines())
            if line:
                self.log.warning(line[:-1])
            return line
        if fd == self._proc.stdout.fileno():
            line = ''.join(self._proc.stdout.readlines())
            if line:
                self.log.info(line[:-1])
            return line

    @staticmethod
    def _extract_job(line):
        job_id_pattern = re.compile('.*console.cloud.google.com/dataflow.*/jobs/([a-z|0-9|A-Z|\\-|\\_]+).*')
        matched_job = job_id_pattern.search(line or '')
        if matched_job:
            return matched_job.group(1).decode()

    def wait_for_done(self):
        reads = [self._proc.stderr.fileno(), self._proc.stdout.fileno()]
        self.log.info('Start waiting for DataFlow process to complete.')
        job_id = None
        process_ends = False
        while 1:
            ret = select.select(reads, [], [], 5)
            if ret is not None:
                for fd in ret[0]:
                    line = self._line(fd)
                    if line:
                        job_id = job_id or self._extract_job(line)

            else:
                self.log.info('Waiting for DataFlow process to complete.')
            if process_ends:
                break
            if self._proc.poll() is not None:
                process_ends = True

        if self._proc.returncode != 0:
            raise Exception('DataFlow failed with return code {}'.format(self._proc.returncode))
        return job_id


class DataFlowHook(GoogleCloudBaseHook):

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None, poll_sleep=10):
        self.poll_sleep = poll_sleep
        super(DataFlowHook, self).__init__(gcp_conn_id, delegate_to)

    def get_conn(self):
        """
        Returns a Google Cloud Dataflow service object.
        """
        http_authorized = self._authorize()
        return build('dataflow',
          'v1b3', http=http_authorized, cache_discovery=False)

    @GoogleCloudBaseHook._Decorators.provide_gcp_credential_file
    def _start_dataflow(self, variables, name, command_prefix, label_formatter):
        variables = self._set_variables(variables)
        cmd = command_prefix + self._build_cmd(variables, label_formatter)
        job_id = _Dataflow(cmd).wait_for_done()
        _DataflowJob(self.get_conn(), variables['project'], name, variables['region'], self.poll_sleep, job_id, self.num_retries).wait_for_done()

    @staticmethod
    def _set_variables(variables):
        if variables['project'] is None:
            raise Exception('Project not specified')
        if 'region' not in variables.keys():
            variables['region'] = DEFAULT_DATAFLOW_LOCATION
        return variables

    def start_java_dataflow(self, job_name, variables, dataflow, job_class=None, append_job_name=True):
        name = self._build_dataflow_job_name(job_name, append_job_name)
        variables['jobName'] = name

        def label_formatter(labels_dict):
            return [
             '--labels={}'.format(json.dumps(labels_dict).replace(' ', ''))]

        command_prefix = ['java', '-cp', dataflow, job_class] if job_class else [
         'java', '-jar', dataflow]
        self._start_dataflow(variables, name, command_prefix, label_formatter)

    def start_template_dataflow(self, job_name, variables, parameters, dataflow_template, append_job_name=True):
        variables = self._set_variables(variables)
        name = self._build_dataflow_job_name(job_name, append_job_name)
        self._start_template_dataflow(name, variables, parameters, dataflow_template)

    def start_python_dataflow(self, job_name, variables, dataflow, py_options, append_job_name=True):
        name = self._build_dataflow_job_name(job_name, append_job_name)
        variables['job_name'] = name

        def label_formatter(labels_dict):
            return ['--labels={}={}'.format(key, value) for key, value in labels_dict.items()]

        self._start_dataflow(variables, name, ['python2'] + py_options + [dataflow], label_formatter)

    @staticmethod
    def _build_dataflow_job_name(job_name, append_job_name=True):
        base_job_name = str(job_name).replace('_', '-')
        if not re.match('^[a-z]([-a-z0-9]*[a-z0-9])?$', base_job_name):
            raise ValueError('Invalid job_name ({}); the name must consist ofonly the characters [-a-z0-9], starting with a letter and ending with a letter or number '.format(base_job_name))
        else:
            if append_job_name:
                safe_job_name = base_job_name + '-' + str(uuid.uuid4())[:8]
            else:
                safe_job_name = base_job_name
        return safe_job_name

    @staticmethod
    def _build_cmd(variables, label_formatter):
        command = ['--runner=DataflowRunner']
        if variables is not None:
            for attr, value in variables.items():
                if attr == 'labels':
                    command += label_formatter(value)
                else:
                    if value is None or value.__len__() < 1:
                        command.append('--' + attr)
                    else:
                        command.append('--' + attr + '=' + value)

        return command

    def _start_template_dataflow(self, name, variables, parameters, dataflow_template):
        environment = {}
        for key in ('numWorkers', 'maxWorkers', 'zone', 'serviceAccountEmail', 'tempLocation',
                    'bypassTempDirValidation', 'machineType', 'additionalExperiments',
                    'network', 'subnetwork', 'additionalUserLabels'):
            if key in variables:
                environment.update({key: variables[key]})

        body = {'jobName':name, 
         'parameters':parameters, 
         'environment':environment}
        service = self.get_conn()
        request = service.projects().locations().templates().launch(projectId=(variables['project']),
          location=(variables['region']),
          gcsPath=dataflow_template,
          body=body)
        response = request.execute(num_retries=(self.num_retries))
        variables = self._set_variables(variables)
        _DataflowJob((self.get_conn()), (variables['project']), name, (variables['region']), (self.poll_sleep),
          num_retries=(self.num_retries)).wait_for_done()
        return response