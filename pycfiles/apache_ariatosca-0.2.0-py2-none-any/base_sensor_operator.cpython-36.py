# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """BaseSensorOperator"""
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