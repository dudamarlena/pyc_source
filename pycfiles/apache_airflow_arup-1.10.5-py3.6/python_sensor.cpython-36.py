# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/python_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3233 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class PythonSensor(BaseSensorOperator):
    __doc__ = "\n    Waits for a Python callable to return True.\n\n    User could put input argument in templates_dict\n    e.g ``templates_dict = {'start_ds': 1970}``\n    and access the argument by calling ``kwargs['templates_dict']['start_ds']``\n    in the the callable\n\n    :param python_callable: A reference to an object that is callable\n    :type python_callable: python callable\n    :param op_kwargs: a dictionary of keyword arguments that will get unpacked\n        in your function\n    :type op_kwargs: dict\n    :param op_args: a list of positional arguments that will get unpacked when\n        calling your callable\n    :type op_args: list\n    :param provide_context: if set to true, Airflow will pass a set of\n        keyword arguments that can be used in your function. This set of\n        kwargs correspond exactly to what you can use in your jinja\n        templates. For this to work, you need to define `**kwargs` in your\n        function header.\n    :type provide_context: bool\n    :param templates_dict: a dictionary where the values are templates that\n        will get templated by the Airflow engine sometime between\n        ``__init__`` and ``execute`` takes place and are made available\n        in your callable's context after the template has been applied.\n    :type templates_dict: dict of str\n    "
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