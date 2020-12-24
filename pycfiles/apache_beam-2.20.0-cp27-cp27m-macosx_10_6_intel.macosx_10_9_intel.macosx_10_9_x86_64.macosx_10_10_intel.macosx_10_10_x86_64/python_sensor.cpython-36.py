# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/python_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3233 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class PythonSensor(BaseSensorOperator):
    """PythonSensor"""
    template_fields = ('templates_dict', )

    @apply_defaults
    def __init__(self, python_callable, op_args=None, op_kwargs=None, provide_context=False, templates_dict=None, *args, **kwargs):
        (super(PythonSensor, self).__init__)(*args, **kwargs)
        self.python_callable = python_callable
        self.op_args = op_args or []
        self.op_kwargs = op_kwargs or {}
        self.provide_context = provide_context
        self.templates_dict = templates_dict

    def poke(self, context):
        if self.provide_context:
            context.update(self.op_kwargs)
            context['templates_dict'] = self.templates_dict
            self.op_kwargs = context
        self.log.info('Poking callable: %s', str(self.python_callable))
        return_value = (self.python_callable)(*self.op_args, **self.op_kwargs)
        return bool(return_value)