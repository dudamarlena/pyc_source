# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/kubernetes.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 49010 bytes
"""
Batch system for running Toil workflows on Kubernetes.

Ony useful with network-based job stores, like AWSJobStore.

Within non-priveleged Kubernetes containers, additional Docker containers
cannot yet be launched. That functionality will need to wait for user-mode
Docker
"""
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
import base64, datetime, getpass, kubernetes, logging, os, pickle, pytz, string, subprocess, sys, tempfile, time, uuid, urllib3
from kubernetes.client.rest import ApiException
from six.moves.queue import Empty, Queue
from toil import applianceSelf, customDockerInitCmd
from toil.batchSystems.abstractBatchSystem import AbstractBatchSystem, BatchSystemSupport, BatchSystemLocalSupport, EXIT_STATUS_UNAVAILABLE_VALUE, UpdatedBatchJobInfo
from toil.common import Toil
from toil.lib.humanize import human2bytes
from toil.lib.threading import LastProcessStandingArena
from toil.resource import Resource
from toil.lib.retry import retry
logger = logging.getLogger(__name__)

def retryable_kubernetes_errors(e):
    """
    A function that determins whether or not Toil should retry or stop given 
    exceptions thrown by Kubernetes. 
    """
    if isinstance(e, urllib3.exceptions.MaxRetryError) or isinstance(e, ApiException):
        return True
    else:
        return False


def retry_kubernetes(retry_while=retryable_kubernetes_errors):
    """
    A wrapper that sends retryable Kubernetes predicates into a context-manager which will allow 
    Kubernetes to keep retrying until a False or an executable method is seen.  
    """
    return retry(predicate=retry_while)


def slow_down(seconds):
    """
    Toil jobs that have completed are not allowed to have taken 0 seconds, but
    Kubernetes timestamps things to the second. It is possible in Kubernetes for
    a pod to have identical start and end timestamps.

    This function takes a possibly 0 job length in seconds an enforces a minimum length to satisfy Toil.

    :param float seconds: Kubernetes timestamp difference

    :return: seconds, or a small positive number if seconds is 0
    :rtype: float
    """
    return max(seconds, sys.float_info.epsilon)


def utc_now():
    """
    Return a datetime in the UTC timezone corresponding to right now.
    """
    return datetime.datetime.utcnow().replace(tzinfo=(pytz.UTC))


class KubernetesBatchSystem(BatchSystemLocalSupport):

    @classmethod
    def supportsAutoDeployment(cls):
        return True

    @classmethod
    def supportsWorkerCleanup(cls):
        return True

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(KubernetesBatchSystem, self).__init__(config, maxCores, maxMemory, maxDisk)
        logging.getLogger('kubernetes').setLevel(logging.ERROR)
        logging.getLogger('requests_oauthlib').setLevel(logging.ERROR)
        self.credential_time = None
        self._apis = {}
        self.namespace = self._api('namespace')
        self.host_path = config.kubernetesHostPath
        if self.host_path is None:
            if os.environ.get('TOIL_KUBERNETES_HOST_PATH', None) is not None:
                self.host_path = os.environ.get('TOIL_KUBERNETES_HOST_PATH')
        else:
            acceptableChars = set(string.ascii_lowercase + string.digits + '-.')
            if os.environ.get('TOIL_KUBERNETES_OWNER', None) is not None:
                username = os.environ.get('TOIL_KUBERNETES_OWNER')
            else:
                username = ''.join([c for c in getpass.getuser().lower() if c in acceptableChars])[:100]
        self.jobPrefix = '{}-toil-{}-'.format(username, uuid.uuid4())
        self.userScript = None
        self.dockerImage = applianceSelf()
        self.workerWorkDir = Toil.getToilWorkDir(config.workDir)
        if config.workDir is None:
            if os.getenv('TOIL_WORKDIR') is None:
                if self.workerWorkDir == tempfile.gettempdir():
                    self.workerWorkDir = '/var/lib/toil'
        self.awsSecretName = os.environ.get('TOIL_AWS_SECRET_NAME', None)
        self.enableWatching = True
        self.jobIds = set()

    def _api(self, kind, max_age_seconds=300):
        """
        The Kubernetes module isn't clever enough to renew its credentials when
        they are about to expire. See
        https://github.com/kubernetes-client/python/issues/741.
        
        We work around this by making sure that every time we are about to talk
        to Kubernetes, we have fresh credentials. And we do that by reloading
        the config and replacing our Kubernetes API objects before we do any
        Kubernetes things.
        
        TODO: We can still get in trouble if a single watch or listing loop
        goes on longer than our credentials last, though.
        
        This method is the Right Way to get any Kubernetes API. You call it
        with the API you want ('batch', 'core', or 'customObjects') and it
        returns an API object with guaranteed fresh credentials.
        
        It also recognizes 'namespace' and returns our namespace as a string.
        
        max_age_seconds needs to be << your cluster's credential expiry time.
        """
        now = utc_now()
        if self.credential_time is None or (now - self.credential_time).total_seconds() > max_age_seconds:
            try:
                kubernetes.config.load_kube_config()
                config_source = 'kube'
            except TypeError:
                try:
                    kubernetes.config.load_incluster_config()
                    config_source = 'in_cluster'
                except kubernetes.config.ConfigException:
                    raise RuntimeError('Could not load Kubernetes configuration from ~/.kube/config, $KUBECONFIG, or current pod.')

            self._apis['batch'] = kubernetes.client.BatchV1Api()
            self._apis['core'] = kubernetes.client.CoreV1Api()
            self._apis['customObjects'] = kubernetes.client.CustomObjectsApi()
            self.credential_time = now
            if kind == 'namespace':
                if config_source == 'in_cluster':
                    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as (fh):
                        return fh.read().strip()
                else:
                    contexts, activeContext = kubernetes.config.list_kube_config_contexts()
                    if not contexts:
                        raise RuntimeError('No Kubernetes contexts available in ~/.kube/config or $KUBECONFIG')
            else:
                return activeContext.get('context', {}).get('namespace', 'default')
        else:
            try:
                return self._apis[kind]
            except KeyError:
                raise RuntimeError('Unknown Kubernetes API type: {}'.format(kind))

    def _try_kubernetes(self, method, *args, **kwargs):
        """
        Kubernetes API can end abruptly and fail when it could dynamically backoff and retry.

        For example, calling self._api('batch').create_namespaced_job(self.namespace, job),
        Kubernetes can behave inconsistently and fail given a large job. See 
        https://github.com/DataBiosphere/toil/issues/2884 .
        
        This function gives Kubernetes more time to try an executable api.  
        """
        for attempt in retry_kubernetes():
            with attempt:
                return method(*args, **kwargs)

    def setUserScript(self, userScript):
        logger.info('Setting user script for deployment: {}'.format(userScript))
        self.userScript = userScript

    def issueBatchJob(self, jobNode):
        localID = self.handleLocalJob(jobNode)
        if localID:
            return localID
        else:
            self.checkResourceRequest(jobNode.memory, jobNode.cores, jobNode.disk)
            jobID = self.getNextJobID()
            jobName = self.jobPrefix + str(jobID)
            job = {'command':jobNode.command, 
             'environment':self.environment.copy()}
            job['workerCleanupInfo'] = self.workerCleanupInfo
            if self.userScript is not None:
                job['userScript'] = self.userScript
            encodedJob = base64.b64encode(pickle.dumps(job, pickle.HIGHEST_PROTOCOL)).decode('utf-8')
            requirements_dict = {'cpu':jobNode.cores, 
             'memory':jobNode.memory + 536870912, 
             'ephemeral-storage':jobNode.disk + 536870912}
            limits_dict = requirements_dict
            resources = kubernetes.client.V1ResourceRequirements(limits=limits_dict, requests=requirements_dict)
            volumes = []
            mounts = []
            if self.host_path is not None:
                host_path_volume_name = 'workdir'
                host_path_volume_source = kubernetes.client.V1HostPathVolumeSource(path=(self.host_path), type='Directory')
                host_path_volume = kubernetes.client.V1Volume(name=host_path_volume_name, host_path=host_path_volume_source)
                volumes.append(host_path_volume)
                host_path_volume_mount = kubernetes.client.V1VolumeMount(mount_path=(self.workerWorkDir), name=host_path_volume_name)
                mounts.append(host_path_volume_mount)
            else:
                ephemeral_volume_name = 'workdir'
                ephemeral_volume_source = kubernetes.client.V1EmptyDirVolumeSource()
                ephemeral_volume = kubernetes.client.V1Volume(name=ephemeral_volume_name, empty_dir=ephemeral_volume_source)
                volumes.append(ephemeral_volume)
                ephemeral_volume_mount = kubernetes.client.V1VolumeMount(mount_path=(self.workerWorkDir), name=ephemeral_volume_name)
                mounts.append(ephemeral_volume_mount)
            if self.awsSecretName is not None:
                secret_volume_name = 's3-credentials'
                secret_volume_source = kubernetes.client.V1SecretVolumeSource(secret_name=(self.awsSecretName))
                secret_volume = kubernetes.client.V1Volume(name=secret_volume_name, secret=secret_volume_source)
                volumes.append(secret_volume)
                secret_volume_mount = kubernetes.client.V1VolumeMount(mount_path='/root/.aws', name=secret_volume_name)
                mounts.append(secret_volume_mount)
            container = kubernetes.client.V1Container(command=['_toil_kubernetes_executor', encodedJob], image=(self.dockerImage),
              name='runner-container',
              resources=resources,
              volume_mounts=mounts)
            pod_spec = kubernetes.client.V1PodSpec(containers=[container], volumes=volumes,
              restart_policy='Never')
            template = kubernetes.client.V1PodTemplateSpec(spec=pod_spec)
            job_spec = kubernetes.client.V1JobSpec(template=template, backoff_limit=0)
            metadata = kubernetes.client.V1ObjectMeta(name=jobName)
            job = kubernetes.client.V1Job(spec=job_spec, metadata=metadata,
              api_version='batch/v1',
              kind='Job')
            launched = self._try_kubernetes(self._api('batch').create_namespaced_job, self.namespace, job)
            logger.debug('Launched job: %s', jobName)
            return jobID

    def _isJobOurs(self, jobObject):
        """
        Determine if a Kubernetes job belongs to us.
        
        :param kubernetes.client.V1Job jobObject: a Kubernetes job being considered.

        :return: True if the job is our responsibility, and false otherwise.
        :rtype: bool
        """
        return jobObject.metadata.name.startswith(self.jobPrefix)

    def _ourJobObjects(self, onlySucceeded=False, limit=None):
        """
        Yield all Kubernetes V1Job objects that we are responsible for that the
        cluster knows about.

        Doesn't support a free-form selector, because there's only about 3
        things jobs can be selected on: https://stackoverflow.com/a/55808444
        
        :param bool onlySucceeded: restrict results to succeeded jobs.
        :param int limit: max results to yield.
        """
        token = None
        seen = 0
        while 1:
            kwargs = {}
            if onlySucceeded:
                kwargs['field_selector'] = 'status.successful==1'
            if token is not None:
                kwargs['_continue'] = token
            results = (self._try_kubernetes)((self._api('batch').list_namespaced_job), (self.namespace), **kwargs)
            for job in results.items:
                if self._isJobOurs(job):
                    yield job
                    seen += 1
                    if limit is not None:
                        if seen >= limit:
                            return

            token = getattr(results.metadata, 'continue', None)
            if token is None:
                break

    def _getPodForJob(self, jobObject):
        """
        Get the pod that belongs to the given job, or None if the job's pod is
        missing. The pod knows about things like the job's exit code.

        :param kubernetes.client.V1Job jobObject: a Kubernetes job to look up
                                       pods for.

        :return: The pod for the job, or None if no pod is found.
        :rtype: kubernetes.client.V1Pod
        """
        token = None
        query = 'job-name={}'.format(jobObject.metadata.name)
        while 1:
            kwargs = {'label_selector': query}
            if token is not None:
                kwargs['_continue'] = token
            results = (self._try_kubernetes)((self._api('core').list_namespaced_pod), (self.namespace), **kwargs)
            for pod in results.items:
                return pod

            token = getattr(results.metadata, 'continue', None)
            if token is None:
                break

    def _getLogForPod(self, podObject):
        """
        Get the log for a pod.

        :param kubernetes.client.V1Pod podObject: a Kubernetes pod with one
                                       container to get the log from.

        :return: The log for the only container in the pod.
        :rtype: str

        """
        return self._try_kubernetes((self._api('core').read_namespaced_pod_log), (podObject.metadata.name), namespace=(self.namespace))

    def _isPodStuckOOM(self, podObject, minFreeBytes=2097152):
        """
        Poll the current memory usage for the pod from the cluster.

        Return True if the pod looks to be in a soft/stuck out of memory (OOM)
        state, where it is using too much memory to actually make progress, but
        not enough to actually trigger the OOM killer to kill it. For some
        large memory limits, on some Kubernetes clusters, pods can get stuck in
        this state when their memory limits are high (approx. 200 Gi).

        We operationalize "OOM" as having fewer than minFreeBytes bytes free.

        We assume the pod has only one container, as Toil's pods do.

        :param kubernetes.client.V1Pod podObject: a Kubernetes pod with one
                                       container to check up on.
        :param int minFreeBytes: Minimum free bytes to not be OOM.

        :return: True if the pod is OOM, false otherwise.
        :rtype: bool
        """
        query = 'metadata.name=' + podObject.metadata.name
        response = self._try_kubernetes((self._api('customObjects').list_namespaced_custom_object), 'metrics.k8s.io',
          'v1beta1', (self.namespace),
          'pods', field_selector=query)
        items = response.get('items', [])
        if len(items) == 0:
            return False
        containers = items[0].get('containers', [{}])
        if len(containers) == 0:
            return False
        bytesUsed = human2bytes(containers[0].get('usage', {}).get('memory', '0'))
        bytesAllowed = human2bytes(podObject.spec.containers[0].resources.limits['memory'])
        if bytesAllowed - bytesUsed < minFreeBytes:
            logger.warning('Pod %s has used %d of %d bytes of memory; reporting as stuck due to OOM.', podObject.metadata.name, bytesUsed, bytesAllowed)
            return True

    def _getIDForOurJob(self, jobObject):
        """
        Get the JobID number that belongs to the given job that we own.

        :param kubernetes.client.V1Job jobObject: a Kubernetes job object that is a job we issued.

        :return: The JobID for the job.
        :rtype: int
        """
        return int(jobObject.metadata.name[len(self.jobPrefix):])

    def getUpdatedBatchJob(self, maxWait):
        entry = datetime.datetime.now()
        result = self._getUpdatedBatchJobImmediately()
        if result is not None or maxWait == 0:
            return result
        else:
            if self.enableWatching:
                w = kubernetes.watch.Watch()
                if self.enableWatching:
                    for j in self._ourJobObjects():
                        for event in w.stream((self._api('core').list_namespaced_pod), (self.namespace), timeout_seconds=maxWait):
                            pod = event['object']
                            if pod.metadata.name.startswith(self.jobPrefix):
                                if pod.status.phase == 'Failed' or pod.status.phase == 'Succeeded':
                                    containerStatuses = pod.status.container_statuses
                                    logger.debug('FINISHED')
                                    if containerStatuses is None or len(containerStatuses) == 0:
                                        logger.debug('No job container statuses for job %s' % pod.metadata.owner_references[0].name)
                                        return UpdatedBatchJobInfo(jobID=(int(pod.metadata.owner_references[0].name[len(self.jobPrefix):])), exitStatus=EXIT_STATUS_UNAVAILABLE_VALUE, wallTime=0, exitReason=None)
                                    termination = pod.status.container_statuses[0].state.terminated
                                    logger.info('REASON: %s Exit Code: %s', termination.reason, termination.exit_code)
                                    if termination.exit_code != 0:
                                        logger.debug('Failed pod information: %s', str(pod))
                                        logger.warning('Log from failed pod: %s', self._getLogForPod(pod))
                                jobID = int(pod.metadata.owner_references[0].name[len(self.jobPrefix):])
                                terminated = pod.status.container_statuses[0].state.terminated
                                runtime = slow_down((terminated.finished_at - terminated.started_at).total_seconds())
                                result = UpdatedBatchJobInfo(jobID=jobID, exitStatus=(terminated.exit_code), wallTime=runtime, exitReason=None)
                                self._try_kubernetes((self._api('batch').delete_namespaced_job), (pod.metadata.owner_references[0].name),
                                  (self.namespace),
                                  propagation_policy='Foreground')
                                self._waitForJobDeath(pod.metadata.owner_references[0].name)
                                return result
                                continue

            else:
                while result is None and (datetime.datetime.now() - entry).total_seconds() < maxWait:
                    result = self._getUpdatedBatchJobImmediately()
                    if result is None:
                        time.sleep(min(maxWait / 2, 1.0))

                return result

    def _getUpdatedBatchJobImmediately(self):
        """
        Return None if no updated (completed or failed) batch job is currently
        available, and jobID, exitCode, runtime if such a job can be found.
        """
        local_tuple = self.getUpdatedLocalJob(0)
        if local_tuple:
            return local_tuple
        jobObject = None
        chosenFor = ''
        for j in self._ourJobObjects(onlySucceeded=True, limit=1):
            jobObject = j
            chosenFor = 'done'

        if jobObject is None:
            for j in self._ourJobObjects():
                failCount = getattr(j.status, 'failed', 0)
                if failCount is None:
                    failCount = 0
                elif failCount > 0:
                    jobObject = j
                    chosenFor = 'failed'
                    break

        if jobObject is None:
            for j in self._ourJobObjects():
                pod = self._getPodForJob(j)
                if pod is None:
                    continue
                containerStatuses = pod.status.container_statuses
                if not containerStatuses is None:
                    if len(containerStatuses) == 0:
                        pass
                    else:
                        waitingInfo = getattr(getattr(pod.status.container_statuses[0], 'state', None), 'waiting', None)
                        if waitingInfo is not None and waitingInfo.reason == 'ImagePullBackOff':
                            jobObject = j
                            chosenFor = 'stuck'
                            logger.warning('Failing stuck job; did you try to run a non-existent Docker image? Check TOIL_APPLIANCE_SELF.')
                            break
                        if self._isPodStuckOOM(pod):
                            jobObject = j
                            chosenFor = 'stuck'
                            break

        if jobObject is None:
            return
        else:
            jobID = int(jobObject.metadata.name[len(self.jobPrefix):])
            jobSubmitTime = getattr(jobObject.status, 'start_time', None)
            if jobSubmitTime is None:
                jobSubmitTime = utc_now()
            pod = self._getPodForJob(jobObject)
            if pod is not None:
                if chosenFor == 'done' or chosenFor == 'failed':
                    containerStatuses = pod.status.container_statuses
                    startTime = getattr(pod.status, 'start_time', None)
                    if startTime is None:
                        startTime = jobSubmitTime
                    if containerStatuses is None or len(containerStatuses) == 0:
                        logger.warning('Exit code and runtime unavailable; pod has no container statuses')
                        logger.warning('Pod: %s', str(pod))
                        exitCode = EXIT_STATUS_UNAVAILABLE_VALUE
                        runtime = slow_down((utc_now() - startTime).total_seconds())
                    else:
                        terminatedInfo = getattr(getattr(containerStatuses[0], 'state', None), 'terminated', None)
                        if terminatedInfo is None:
                            logger.warning('Exit code and runtime unavailable; pod stopped without container terminating')
                            logger.warning('Pod: %s', str(pod))
                            exitCode = EXIT_STATUS_UNAVAILABLE_VALUE
                            runtime = slow_down((utc_now() - startTime).total_seconds())
                        else:
                            exitCode = terminatedInfo.exit_code
                    runtime = slow_down((terminatedInfo.finished_at - pod.status.start_time).total_seconds())
                    if chosenFor == 'failed':
                        logger.warning('Log from failed pod: %s', self._getLogForPod(pod))
                else:
                    assert chosenFor == 'stuck'
                    exitCode = EXIT_STATUS_UNAVAILABLE_VALUE
                    runtime = slow_down((utc_now() - jobSubmitTime).total_seconds())
            else:
                logging.warning('Exit code and runtime unavailable; pod vanished')
                exitCode = EXIT_STATUS_UNAVAILABLE_VALUE
                runtime = slow_down((utc_now() - jobSubmitTime).total_seconds())
            try:
                self._try_kubernetes((self._api('batch').delete_namespaced_job), (jobObject.metadata.name), (self.namespace),
                  propagation_policy='Foreground')
                self._waitForJobDeath(jobObject.metadata.name)
            except kubernetes.client.rest.ApiException:
                pass

            return UpdatedBatchJobInfo(jobID=jobID, exitStatus=exitCode, wallTime=runtime, exitReason=None)

    def _waitForJobDeath(self, jobName):
        """
        Block until the job with the given name no longer exists.
        """
        backoffTime = 0.1
        maxBackoffTime = 6.4
        while True:
            try:
                self._try_kubernetes(self._api('batch').read_namespaced_job, jobName, self.namespace)
                time.sleep(backoffTime)
                if backoffTime < maxBackoffTime:
                    backoffTime *= 2
            except kubernetes.client.rest.ApiException:
                break

    def shutdown(self):
        self.shutdownLocal()
        for job in self._ourJobObjects():
            jobName = job.metadata.name
            try:
                pod = self._getPodForJob(job)
                if pod.status.phase == 'Failed':
                    logger.debug('Failed pod encountered at shutdown: %s', str(pod))
            except:
                pass

            try:
                response = self._try_kubernetes((self._api('batch').delete_namespaced_job), jobName, (self.namespace),
                  propagation_policy='Background')
                logger.debug('Killed job for shutdown: %s', jobName)
            except ApiException as e:
                logger.error('Exception when calling BatchV1Api->delte_namespaced_job: %s' % e)

    def _getIssuedNonLocalBatchJobIDs(self):
        """
        Get the issued batch job IDs that are not for local jobs.
        """
        jobIDs = []
        got_list = self._ourJobObjects()
        for job in got_list:
            jobIDs.append(self._getIDForOurJob(job))

        return jobIDs

    def getIssuedBatchJobIDs(self):
        return self._getIssuedNonLocalBatchJobIDs() + list(self.getIssuedLocalJobIDs())

    def getRunningBatchJobIDs(self):
        secondsPerJob = dict()
        for job in self._ourJobObjects():
            pod = self._getPodForJob(job)
            if pod is None:
                continue
            if pod.status.phase == 'Running':
                runtime = (utc_now() - pod.status.start_time).total_seconds()
                secondsPerJob[self._getIDForOurJob(job)] = runtime

        secondsPerJob.update(self.getRunningLocalJobIDs())
        return secondsPerJob

    def killBatchJobs(self, jobIDs):
        self.killLocalJobs(jobIDs)
        issuedOnKubernetes = set(self._getIssuedNonLocalBatchJobIDs())
        for jobID in jobIDs:
            if jobID not in issuedOnKubernetes:
                pass
            else:
                jobName = self.jobPrefix + str(jobID)
                response = self._try_kubernetes((self._api('batch').delete_namespaced_job), jobName, (self.namespace),
                  propagation_policy='Foreground')
                logger.debug('Killed job by request: %s', jobName)

        for jobID in jobIDs:
            jobName = self.jobPrefix + str(jobID)
            self._waitForJobDeath(jobName)


def executor():
    """
    Main function of the _toil_kubernetes_executor entrypoint.

    Runs inside the Toil container.

    Responsible for setting up the user script and running the command for the
    job (which may in turn invoke the Toil worker entrypoint).

    """
    logging.basicConfig(level=(logging.DEBUG))
    logger.debug('Starting executor')
    exit_code = EXIT_STATUS_UNAVAILABLE_VALUE
    if len(sys.argv) != 2:
        logger.error('Executor requires exactly one base64-encoded argument')
        sys.exit(exit_code)
    try:
        job = pickle.loads(base64.b64decode(sys.argv[1].encode('utf-8')))
    except:
        exc_info = sys.exc_info()
        logger.error('Exception while unpickling task: ', exc_info=exc_info)
        sys.exit(exit_code)

    if 'environment' in job:
        logger.debug('Adopting environment: %s', str(job['environment'].keys()))
        for var, value in job['environment'].items():
            os.environ[var] = value

    logger.debug('Preparing system for resource download')
    Resource.prepareSystem()
    try:
        if 'userScript' in job:
            job['userScript'].register()
        cleanupInfo = job['workerCleanupInfo']
        arena = LastProcessStandingArena(Toil.getToilWorkDir(cleanupInfo.workDir), cleanupInfo.workflowID + '-kube-executor')
        arena.enter()
        try:
            logger.debug("Invoking command: '%s'", job['command'])
            child = subprocess.Popen((job['command']), preexec_fn=(lambda : os.setpgrp()),
              shell=True)
            exit_code = child.wait()
        finally:
            for _ in arena.leave():
                logger.debug('Cleaning up worker')
                BatchSystemSupport.workerCleanup(cleanupInfo)

    finally:
        logger.debug('Cleaning up resources')
        Resource.cleanSystem()
        logger.debug('Shutting down')
        sys.exit(exit_code)