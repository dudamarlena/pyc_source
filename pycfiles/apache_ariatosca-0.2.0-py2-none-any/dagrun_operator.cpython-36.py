# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/dagrun_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3902 bytes
import datetime, six
from airflow.models import BaseOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults
from airflow.api.common.experimental.trigger_dag import trigger_dag
import json

class DagRunOrder(object):

    def __init__(self, run_id=None, payload=None):
        self.run_id = run_id
        self.payload = payload


class TriggerDagRunOperator(BaseOperator):
    """TriggerDagRunOperator"""
    template_fields = ('trigger_dag_id', 'execution_date')
    ui_color = '#ffefeb'

    @apply_defaults
    def __init__(self, trigger_dag_id, python_callable=None, execution_date=None, *args, **kwargs):
        (super(TriggerDagRunOperator, self).__init__)(*args, **kwargs)
        self.python_callable = python_callable
        self.trigger_dag_id = trigger_dag_id
        if isinstance(execution_date, datetime.datetime):
            self.execution_date = execution_date.isoformat()
        else:
            if isinstance(execution_date, six.string_types):
                self.execution_date = execution_date
            else:
                if execution_date is None:
                    self.execution_date = execution_date
                else:
                    raise TypeError('Expected str or datetime.datetime type for execution_date. Got {}'.format(type(execution_date)))

    def execute(self, context):
        if self.execution_date is not None:
            run_id = 'trig__{}'.format(self.execution_date)
            self.execution_date = timezone.parse(self.execution_date)
        else:
            run_id = 'trig__' + timezone.utcnow().isoformat()
        dro = DagRunOrder(run_id=run_id)
        if self.python_callable is not None:
            dro = self.python_callable(context, dro)
        else:
            if dro:
                trigger_dag(dag_id=(self.trigger_dag_id), run_id=(dro.run_id),
                  conf=(json.dumps(dro.payload)),
                  execution_date=(self.execution_date),
                  replace_microseconds=False)
            else:
                self.log.info('Criteria not met, moving on')