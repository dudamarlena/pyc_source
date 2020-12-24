# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/admin/services_manager.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 22529 bytes
import os, logging, traceback, socket
from collections import defaultdict
from contextlib import closing
from singa_auto.constants import ServiceStatus, ServiceType, BudgetOption, InferenceBudgetOption, TrainJobStatus, InferenceJobStatus
from singa_auto.meta_store import MetaStore
from singa_auto.container import DockerSwarmContainerManager, ContainerManager, ContainerService
from singa_auto.model import parse_model_install_command
logger = logging.getLogger(__name__)

class ServiceDeploymentError(Exception):
    pass


ENVIRONMENT_VARIABLES_AUTOFORWARD = [
 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_USER', 'POSTGRES_PASSWORD',
 'SUPERADMIN_PASSWORD', 'POSTGRES_DB', 'REDIS_HOST', 'REDIS_PORT',
 'ADMIN_HOST', 'ADMIN_PORT', 'DATA_DIR_PATH', 'LOGS_DIR_PATH', 'PARAMS_DIR_PATH', 'KAFKA_HOST', 'KAFKA_PORT']
DEFAULT_TRAIN_GPU_COUNT = 0
DEFAULT_INFERENCE_GPU_COUNT = 0
SERVICE_STATUS_WAIT_SECS = 1

class ServicesManager(object):
    __doc__ = '\n        Manages deployment of services and statuses of train jobs & inference jobs\n    '

    def __init__(self, meta_store=None, container_manager=None, var_autoforward=None):
        if var_autoforward is None:
            var_autoforward = ENVIRONMENT_VARIABLES_AUTOFORWARD
        self._meta_store = meta_store or MetaStore()
        self._container_manager = container_manager or DockerSwarmContainerManager()
        for x in var_autoforward:
            if x not in os.environ:
                raise ServiceDeploymentError('{} is not in environment variables'.format(x))

        self._var_autoforward = var_autoforward
        version = os.environ['SINGA_AUTO_VERSION']
        self._data_dir_path = os.environ['DATA_DIR_PATH']
        self._logs_dir_path = os.environ['LOGS_DIR_PATH']
        self._params_dir_path = os.environ['PARAMS_DIR_PATH']
        self._host_workdir_path = os.environ['HOST_WORKDIR_PATH']
        self._docker_workdir_path = os.environ['DOCKER_WORKDIR_PATH']
        self._predictor_image = f"{os.environ['SINGA_AUTO_IMAGE_PREDICTOR']}:{version}"
        self._predictor_port = os.environ['PREDICTOR_PORT']
        self._app_mode = os.environ['APP_MODE']
        self._singa_auto_addr = os.environ['SINGA_AUTO_ADDR']
        self._app_mode = os.environ['APP_MODE']

    def create_inference_services(self, inference_job_id, use_checkpoint=False):
        inference_job = self._meta_store.get_inference_job(inference_job_id)
        total_gpus = int(inference_job.budget.get(InferenceBudgetOption.GPU_COUNT, DEFAULT_INFERENCE_GPU_COUNT))
        try:
            predictor_service = self._create_predictor(inference_job)
            if use_checkpoint:
                self._create_inference_job_worker(inference_job=inference_job, model_id=(inference_job.model_id),
                  gpus=total_gpus)
            else:
                sub_train_jobs = self._meta_store.get_sub_train_jobs_of_train_job(inference_job.train_job_id)
                jobs_ids, jobs_gpus = self._get_deployment_for_inference_job(total_gpus, sub_train_jobs)
                for trial_id, gpus in zip(jobs_ids, jobs_gpus):
                    trial = self._meta_store.get_trial(trial_id)
                    self._create_inference_job_worker(inference_job=inference_job, trial=trial,
                      gpus=gpus)

            return (
             inference_job, predictor_service)
        except Exception as e:
            self.stop_inference_services(inference_job_id)
            self._meta_store.mark_inference_job_as_errored(inference_job)
            raise ServiceDeploymentError(e)

    def stop_inference_services(self, inference_job_id):
        inference_job = self._meta_store.get_inference_job(inference_job_id)
        if inference_job.predictor_service_id is not None:
            service = self._meta_store.get_service(inference_job.predictor_service_id)
            self._stop_service(service)
        workers = self._meta_store.get_workers_of_inference_job(inference_job_id)
        for worker in workers:
            service = self._meta_store.get_service(worker.service_id)
            self._stop_service(service)

        self.refresh_inference_job_status(inference_job_id)
        return inference_job

    def refresh_inference_job_status(self, inference_job_id):
        inference_job = self._meta_store.get_inference_job(inference_job_id)
        assert inference_job is not None
        if inference_job.status == InferenceJobStatus.ERRORED:
            return
        predictor_service_id = inference_job.predictor_service_id
        workers = self._meta_store.get_workers_of_inference_job(inference_job_id)
        predictor_service = self._meta_store.get_service(predictor_service_id) if predictor_service_id is not None else None
        services = [self._meta_store.get_service(x.service_id) for x in workers]
        worker_counts = defaultdict(int)
        for service in services:
            if service is not None:
                worker_counts[service.status] += 1

        predictor_status = predictor_service.status if predictor_service is not None else None
        if predictor_status == ServiceStatus.RUNNING:
            if worker_counts[ServiceStatus.RUNNING] >= 1:
                self._meta_store.mark_inference_job_as_running(inference_job)
        if predictor_status == ServiceStatus.STOPPED:
            self._meta_store.mark_inference_job_as_stopped(inference_job)
        else:
            if predictor_status == ServiceStatus.ERRORED or worker_counts[ServiceStatus.ERRORED] == len(workers):
                self._meta_store.mark_inference_job_as_errored(inference_job)
                self.stop_inference_services(inference_job_id)
        self._meta_store.commit()

    def create_train_services(self, train_job_id):
        train_job = self._meta_store.get_train_job(train_job_id)
        sub_train_jobs = self._meta_store.get_sub_train_jobs_of_train_job(train_job_id)
        total_gpus = int(train_job.budget.get(BudgetOption.GPU_COUNT, DEFAULT_TRAIN_GPU_COUNT))
        jobs_gpus, jobs_cpus = self._get_deployment_for_train_job(total_gpus, sub_train_jobs)
        try:
            for sub_train_job, gpus, cpus in zip(sub_train_jobs, jobs_gpus, jobs_cpus):
                self._create_advisor(sub_train_job)
                for _ in range(gpus):
                    self._create_train_job_worker(sub_train_job)

                for _ in range(cpus):
                    self._create_train_job_worker(sub_train_job, gpus=0)

            return train_job
        except Exception as e:
            self.stop_train_services(train_job_id)
            self._meta_store.mark_train_job_as_errored(train_job)
            raise ServiceDeploymentError(e)

    def stop_train_services(self, train_job_id):
        train_job = self._meta_store.get_train_job(train_job_id)
        assert train_job is not None
        sub_train_jobs = self._meta_store.get_sub_train_jobs_of_train_job(train_job_id)
        for sub_train_job in sub_train_jobs:
            self.stop_sub_train_job_services(sub_train_job.id)

    def stop_sub_train_job_services(self, sub_train_job_id):
        sub_train_job = self._meta_store.get_sub_train_job(sub_train_job_id)
        assert sub_train_job is not None
        workers = self._meta_store.get_workers_of_sub_train_job(sub_train_job_id)
        if sub_train_job.advisor_service_id is not None:
            service = self._meta_store.get_service(sub_train_job.advisor_service_id)
            self._stop_service(service)
        for worker in workers:
            service = self._meta_store.get_service(worker.service_id)
            self._stop_service(service)

        self.refresh_sub_train_job_status(sub_train_job_id)
        return sub_train_job

    def refresh_sub_train_job_status(self, sub_train_job_id):
        sub_train_job = self._meta_store.get_sub_train_job(sub_train_job_id)
        assert sub_train_job is not None
        if sub_train_job.status == TrainJobStatus.ERRORED:
            return
        advisor_service_id = sub_train_job.advisor_service_id
        workers = self._meta_store.get_workers_of_sub_train_job(sub_train_job_id)
        advisor_service = self._meta_store.get_service(advisor_service_id) if advisor_service_id is not None else None
        services = [self._meta_store.get_service(x.service_id) for x in workers]
        worker_counts = defaultdict(int)
        for service in services:
            if service is not None:
                worker_counts[service.status] += 1

        advisor_status = advisor_service.status if advisor_service is not None else None
        if advisor_status == ServiceStatus.RUNNING:
            if worker_counts[ServiceStatus.RUNNING] >= 1:
                self._meta_store.mark_sub_train_job_as_running(sub_train_job)
        if advisor_status == ServiceStatus.STOPPED:
            self._meta_store.mark_sub_train_job_as_stopped(sub_train_job)
        else:
            if advisor_status == ServiceStatus.ERRORED or worker_counts[ServiceStatus.ERRORED] == len(workers):
                self._meta_store.mark_sub_train_job_as_errored(sub_train_job)
                self.stop_sub_train_job_services(sub_train_job_id)
        self._meta_store.commit()
        self.refresh_train_job_status(sub_train_job.train_job_id)

    def refresh_train_job_status(self, train_job_id):
        train_job = self._meta_store.get_train_job(train_job_id)
        assert train_job is not None
        sub_train_jobs = self._meta_store.get_sub_train_jobs_of_train_job(train_job_id)
        if train_job.status == TrainJobStatus.ERRORED:
            return
        counts = defaultdict(int)
        for job in sub_train_jobs:
            counts[job.status] += 1

        if counts[TrainJobStatus.RUNNING] >= 1:
            self._meta_store.mark_train_job_as_running(train_job)
        else:
            if counts[TrainJobStatus.STOPPED] == len(sub_train_jobs):
                self._meta_store.mark_train_job_as_stopped(train_job)
            elif counts[TrainJobStatus.ERRORED] >= 1:
                if counts[TrainJobStatus.ERRORED] + counts[TrainJobStatus.STOPPED] == len(sub_train_jobs):
                    self._meta_store.mark_train_job_as_errored(train_job)

    def _get_deployment_for_train_job(self, total_gpus, sub_train_jobs):
        N = len(sub_train_jobs)
        base_gpus = total_gpus // N
        extra_gpus = total_gpus - base_gpus * N
        jobs_gpus = [base_gpus + 1] * extra_gpus + [base_gpus] * (N - extra_gpus)
        jobs_cpus = []
        for gpus in jobs_gpus:
            jobs_cpus.append(0 if gpus > 0 else 1)

        return (jobs_gpus, jobs_cpus)

    def _get_deployment_for_inference_job(self, total_gpus, sub_train_jobs):
        trial_ids = []
        for sub_train_job in sub_train_jobs:
            trials = self._meta_store.get_best_trials_of_sub_train_job((sub_train_job.id), max_count=1)
            if len(trials) == 0:
                pass
            else:
                trial_ids.append(trials[0].id)

        N = len(trial_ids)
        base_gpus = total_gpus // N
        extra_gpus = total_gpus - base_gpus * N
        jobs_gpus = [base_gpus + 1] * extra_gpus + [base_gpus] * (N - extra_gpus)
        return (
         trial_ids, jobs_gpus)

    def _create_inference_job_worker(self, inference_job, trial=None, model_id=None, gpus=0):
        trial_id = None
        checkpoint_id = None
        if trial is not None:
            sub_train_job = self._meta_store.get_sub_train_job(trial.sub_train_job_id)
            model = self._meta_store.get_model(sub_train_job.model_id)
            trial_id = trial.id
        else:
            if model_id is not None:
                model = self._meta_store.get_model(model_id)
                checkpoint_id = model.checkpoint_id
            else:
                raise ServiceDeploymentError('No model found')
        service_type = ServiceType.INFERENCE
        install_command = parse_model_install_command((model.dependencies), enable_gpu=(gpus > 0))
        environment_vars = {'WORKER_INSTALL_COMMAND': install_command}
        service = self._create_service(service_type=service_type,
          docker_image=(model.docker_image),
          environment_vars=environment_vars,
          gpus=gpus)
        self._meta_store.create_inference_job_worker(service_id=(service.id),
          inference_job_id=(inference_job.id),
          trial_id=trial_id,
          checkpoint_id=checkpoint_id)
        self._meta_store.commit()
        return service

    def _create_predictor(self, inference_job):
        service_type = ServiceType.PREDICT
        environment_vars = {}
        service = self._create_service(service_type=service_type,
          docker_image=(self._predictor_image),
          environment_vars=environment_vars,
          container_port=(self._predictor_port))
        self._meta_store.update_inference_job(inference_job, predictor_service_id=(service.id))
        self._meta_store.commit()
        return service

    def _create_train_job_worker(self, sub_train_job, gpus=1):
        model = self._meta_store.get_model(sub_train_job.model_id)
        service_type = ServiceType.TRAIN
        install_command = parse_model_install_command((model.dependencies), enable_gpu=(gpus > 0))
        environment_vars = {'WORKER_INSTALL_COMMAND': install_command}
        service = self._create_service(service_type=service_type,
          docker_image=(model.docker_image),
          environment_vars=environment_vars,
          gpus=gpus)
        self._meta_store.create_train_job_worker(service_id=(service.id),
          sub_train_job_id=(sub_train_job.id))
        self._meta_store.commit()
        return service

    def _create_advisor(self, sub_train_job):
        model = self._meta_store.get_model(sub_train_job.model_id)
        service_type = ServiceType.ADVISOR
        install_command = parse_model_install_command((model.dependencies), enable_gpu=False)
        environment_vars = {'WORKER_INSTALL_COMMAND': install_command}
        service = self._create_service(service_type=service_type,
          docker_image=(model.docker_image),
          environment_vars=environment_vars)
        self._meta_store.update_sub_train_job(sub_train_job, advisor_service_id=(service.id))
        self._meta_store.commit()
        return service

    def _stop_service(self, service):
        if service.status == ServiceStatus.STOPPED:
            logger.info('Service of ID "{}" already stopped!'.format(service.id))
            return
        try:
            container_service = self._get_container_service_from_service(service)
            self._container_manager.destroy_service(container_service)
        except:
            logger.info('Error while deleting service with ID {} - maybe already deleted'.format(service.id))
            logger.info(traceback.format_exc())

        self._meta_store.mark_service_as_stopped(service)
        self._meta_store.commit()

    def _create_service(self, service_type, docker_image, replicas=1, environment_vars={}, args=[], container_port=None, gpus=0):
        container_manager_type = type(self._container_manager).__name__
        service = self._meta_store.create_service(service_type=service_type,
          container_manager_type=container_manager_type,
          docker_image=docker_image,
          replicas=replicas,
          gpus=gpus)
        self._meta_store.commit()
        environment_vars = {**{x:os.environ[x] for x in self._var_autoforward}, **environment_vars, **{'SINGA_AUTO_SERVICE_ID':service.id, 
         'SINGA_AUTO_SERVICE_TYPE':service_type, 
         'WORKDIR_PATH':self._docker_workdir_path}}
        if self._app_mode == 'DEV':
            mounts = {self._host_workdir_path: self._docker_workdir_path}
        else:
            mounts = {os.path.join(self._host_workdir_path, self._data_dir_path): os.path.join(self._docker_workdir_path, self._data_dir_path), 
             
             os.path.join(self._host_workdir_path, self._logs_dir_path): os.path.join(self._docker_workdir_path, self._logs_dir_path), 
             
             os.path.join(self._host_workdir_path, self._params_dir_path): os.path.join(self._docker_workdir_path, self._params_dir_path)}
        publish_port = None
        ext_hostname = None
        ext_port = None
        if container_port is not None:
            ext_hostname = self._singa_auto_addr
            ext_port = self._get_available_ext_port()
            publish_port = (ext_port, container_port)
        try:
            container_service_name = 'singa-auto-svc-{}-{}'.format(service_type.lower(), service.id)
            container_service = self._container_manager.create_service(service_name=container_service_name,
              docker_image=docker_image,
              replicas=replicas,
              args=args,
              environment_vars=environment_vars,
              mounts=mounts,
              publish_port=publish_port,
              gpus=gpus)
            self._meta_store.mark_service_as_deploying(service,
              container_service_name=container_service_name,
              container_service_id=(container_service.id),
              hostname=(container_service.hostname),
              port=(container_service.port),
              ext_hostname=ext_hostname,
              ext_port=ext_port,
              container_service_info=(container_service.info))
            self._meta_store.commit()
        except Exception as e:
            logger.error('Error while creating service with ID {}'.format(service.id))
            logger.error(traceback.format_exc())
            self._meta_store.mark_service_as_errored(service)
            self._meta_store.commit()
            raise e

        return service

    def _get_available_ext_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as (s):
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def _get_container_service_from_service(self, service):
        service_id = service.container_service_id
        hostname = service.hostname
        port = service.port
        info = service.container_service_info
        container_service = ContainerService(service_id, hostname, port, info)
        return container_service