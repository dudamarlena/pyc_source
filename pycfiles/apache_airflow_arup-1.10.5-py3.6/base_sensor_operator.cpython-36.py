# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/base_sensor_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6138 bytes
from time import sleep
from datetime import timedelta
from airflow.exceptions import AirflowException, AirflowSensorTimeout, AirflowSkipException, AirflowRescheduleException
from airflow.models import BaseOperator, SkipMixin, TaskReschedule
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults
from airflow.ti_deps.deps.ready_to_reschedule import ReadyToRescheduleDep

class BaseSensorOperator(BaseOperator, SkipMixin):
    __doc__ = "\n    Sensor operators are derived from this class and inherit these attributes.\n\n    Sensor operators keep executing at a time interval and succeed when\n    a criteria is met and fail if and when they time out.\n\n    :param soft_fail: Set to true to mark the task as SKIPPED on failure\n    :type soft_fail: bool\n    :param poke_interval: Time in seconds that the job should wait in\n        between each tries\n    :type poke_interval: int\n    :param timeout: Time, in seconds before the task times out and fails.\n    :type timeout: int\n    :param mode: How the sensor operates.\n        Options are: ``{ poke | reschedule }``, default is ``poke``.\n        When set to ``poke`` the sensor is taking up a worker slot for its\n        whole execution time and sleeps between pokes. Use this mode if the\n        expected runtime of the sensor is short or if a short poke interval\n        is required. Note that the sensor will hold onto a worker slot and\n        a pool slot for the duration of the sensor's runtime in this mode.\n        When set to ``reschedule`` the sensor task frees the worker slot when\n        the criteria is not yet met and it's rescheduled at a later time. Use\n        this mode if the time before the criteria is met is expected to be\n        quite long. The poke interval should be more than one minute to\n        prevent too much load on the scheduler.\n    :type mode: str\n    "
    ui_color = '#e6f1f2'
    valid_modes = ['poke', 'reschedule']

    @apply_defaults
    def __init__(self, poke_interval=60, timeout=604800, soft_fail=False, mode='poke', *args, **kwargs):
        (super(BaseSensorOperator, self).__init__)(*args, **kwargs)
        self.poke_interval = poke_interval
        self.soft_fail = soft_fail
        self.timeout = timeout
        self.mode = mode
        self._validate_input_values()

    def _validate_input_values(self):
        if not isinstance(self.poke_interval, (int, float)) or self.poke_interval < 0:
            raise AirflowException('The poke_interval must be a non-negative number')
        else:
            if not isinstance(self.timeout, (int, float)) or self.timeout < 0:
                raise AirflowException('The timeout must be a non-negative number')
            if self.mode not in self.valid_modes:
                raise AirflowException("The mode must be one of {valid_modes},'{d}.{t}'; received '{m}'.".format(valid_modes=(self.valid_modes),
                  d=(self.dag.dag_id if self.dag else ''),
                  t=(self.task_id),
                  m=(self.mode)))

    def poke(self, context):
        """
        Function that the sensors defined while deriving this class should
        override.
        """
        raise AirflowException('Override me.')

    def execute(self, context):
        started_at = timezone.utcnow()
        if self.reschedule:
            task_reschedules = TaskReschedule.find_for_task_instance(context['ti'])
            if task_reschedules:
                started_at = task_reschedules[0].start_date
        while not self.poke(context):
            if (timezone.utcnow() - started_at).total_seconds() > self.timeout:
                if self.soft_fail:
                    if not context['ti'].is_eligible_to_retry():
                        self._do_skip_downstream_tasks(context)
                        raise AirflowSkipException('Snap. Time is OUT.')
                else:
                    raise AirflowSensorTimeout('Snap. Time is OUT.')
            if self.reschedule:
                reschedule_date = timezone.utcnow() + timedelta(seconds=(self.poke_interval))
                raise AirflowRescheduleException(reschedule_date)
            else:
                sleep(self.poke_interval)

        self.log.info('Success criteria met. Exiting.')

    def _do_skip_downstream_tasks(self, context):
        downstream_tasks = context['task'].get_flat_relatives(upstream=False)
        self.log.debug('Downstream task_ids %s', downstream_tasks)
        if downstream_tasks:
            self.skip(context['dag_run'], context['ti'].execution_date, downstream_tasks)

    @property
    def reschedule(self):
        return self.mode == 'reschedule'

    @property
    def deps(self):
        """
        Adds one additional dependency for all sensor operators that
        checks if a sensor task instance can be rescheduled.
        """
        return BaseOperator.deps.fget(self) | {ReadyToRescheduleDep()}