# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/python_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 18333 bytes
import inspect, os, pickle, subprocess, sys, types
from builtins import str
from textwrap import dedent
from typing import Optional, Iterable, Dict, Callable
import dill
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, SkipMixin
from airflow.utils.decorators import apply_defaults
from airflow.utils.file import TemporaryDirectory
from airflow.utils.operator_helpers import context_to_airflow_vars

class PythonOperator(BaseOperator):
    """PythonOperator"""
    template_fields = ('templates_dict', 'op_args', 'op_kwargs')
    ui_color = '#ffefeb'
    shallow_copy_attrs = ('python_callable', 'op_kwargs')

    @apply_defaults
    def __init__(self, python_callable, op_args=None, op_kwargs=None, provide_context=False, templates_dict=None, templates_exts=None, *args, **kwargs):
        (super(PythonOperator, self).__init__)(*args, **kwargs)
        if not callable(python_callable):
            raise AirflowException('`python_callable` param must be callable')
        self.python_callable = python_callable
        self.op_args = op_args or []
        self.op_kwargs = op_kwargs or {}
        self.provide_context = provide_context
        self.templates_dict = templates_dict
        if templates_exts:
            self.template_ext = templates_exts

    def execute(self, context):
        airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
        self.log.info('Exporting the following env vars:\n%s', '\n'.join(['{}={}'.format(k, v) for k, v in airflow_context_vars.items()]))
        os.environ.update(airflow_context_vars)
        if self.provide_context:
            context.update(self.op_kwargs)
            context['templates_dict'] = self.templates_dict
            self.op_kwargs = context
        return_value = self.execute_callable()
        self.log.info('Done. Returned value was: %s', return_value)
        return return_value

    def execute_callable(self):
        return (self.python_callable)(*self.op_args, **self.op_kwargs)


class BranchPythonOperator(PythonOperator, SkipMixin):
    """BranchPythonOperator"""

    def execute(self, context):
        branch = super(BranchPythonOperator, self).execute(context)
        self.skip_all_except(context['ti'], branch)


class ShortCircuitOperator(PythonOperator, SkipMixin):
    """ShortCircuitOperator"""

    def execute(self, context):
        condition = super(ShortCircuitOperator, self).execute(context)
        self.log.info('Condition result is %s', condition)
        if condition:
            self.log.info('Proceeding with downstream tasks...')
            return
        self.log.info('Skipping downstream tasks...')
        downstream_tasks = context['task'].get_flat_relatives(upstream=False)
        self.log.debug('Downstream task_ids %s', downstream_tasks)
        if downstream_tasks:
            self.skip(context['dag_run'], context['ti'].execution_date, downstream_tasks)
        self.log.info('Done.')


class PythonVirtualenvOperator(PythonOperator):
    """PythonVirtualenvOperator"""

    @apply_defaults
    def __init__(self, python_callable, requirements=None, python_version=None, use_dill=False, system_site_packages=True, op_args=None, op_kwargs=None, provide_context=False, string_args=None, templates_dict=None, templates_exts=None, *args, **kwargs):
        (super(PythonVirtualenvOperator, self).__init__)(args, python_callable=python_callable, op_args=op_args, op_kwargs=op_kwargs, templates_dict=templates_dict, templates_exts=templates_exts, provide_context=provide_context, **kwargs)
        self.requirements = requirements or []
        self.string_args = string_args or []
        self.python_version = python_version
        self.use_dill = use_dill
        self.system_site_packages = system_site_packages
        dill_in_requirements = map(lambda x: x.lower().startswith('dill'), self.requirements)
        if not system_site_packages:
            if use_dill:
                if not any(dill_in_requirements):
                    raise AirflowException('If using dill, dill must be in the environment either via system_site_packages or requirements')
        if not isinstance(self.python_callable, types.FunctionType) or self.python_callable.__name__ == (lambda x: 0).__name__:
            raise AirflowException('{} only supports functions for python_callable arg', self.__class__.__name__)
        if python_version is not None:
            if str(python_version)[0] != str(sys.version_info[0]):
                if self._pass_op_args():
                    raise AirflowException('Passing op_args or op_kwargs is not supported across different Python major versions for PythonVirtualenvOperator. Please use string_args.')

    def execute_callable(self):
        with TemporaryDirectory(prefix='venv') as (tmp_dir):
            if self.templates_dict:
                self.op_kwargs['templates_dict'] = self.templates_dict
            input_filename = os.path.join(tmp_dir, 'script.in')
            output_filename = os.path.join(tmp_dir, 'script.out')
            string_args_filename = os.path.join(tmp_dir, 'string_args.txt')
            script_filename = os.path.join(tmp_dir, 'script.py')
            self._execute_in_subprocess(self._generate_virtualenv_cmd(tmp_dir))
            cmd = self._generate_pip_install_cmd(tmp_dir)
            if cmd:
                self._execute_in_subprocess(cmd)
            self._write_args(input_filename)
            self._write_script(script_filename)
            self._write_string_args(string_args_filename)
            self._execute_in_subprocess(self._generate_python_cmd(tmp_dir, script_filename, input_filename, output_filename, string_args_filename))
            return self._read_result(output_filename)

    def _pass_op_args(self):
        return len(self.op_args) + len(self.op_kwargs) > 0

    def _execute_in_subprocess(self, cmd):
        try:
            self.log.info('Executing cmd\n%s', cmd)
            output = subprocess.check_output(cmd, stderr=(subprocess.STDOUT),
              close_fds=True)
            if output:
                self.log.info('Got output\n%s', output)
        except subprocess.CalledProcessError as e:
            self.log.info('Got error output\n%s', e.output)
            raise

    def _write_string_args(self, filename):
        with open(filename, 'w') as (f):
            f.write('\n'.join(map(str, self.string_args)))

    def _write_args(self, input_filename):
        if self._pass_op_args():
            with open(input_filename, 'wb') as (f):
                arg_dict = {'args':self.op_args, 
                 'kwargs':self.op_kwargs}
                if self.use_dill:
                    dill.dump(arg_dict, f)
                else:
                    pickle.dump(arg_dict, f)

    def _read_result(self, output_filename):
        if os.stat(output_filename).st_size == 0:
            return
        with open(output_filename, 'rb') as (f):
            try:
                if self.use_dill:
                    return dill.load(f)
                else:
                    return pickle.load(f)
            except ValueError:
                self.log.error('Error deserializing result. Note that result deserialization is not supported across major Python versions.')
                raise

    def _write_script(self, script_filename):
        with open(script_filename, 'w') as (f):
            python_code = self._generate_python_code()
            self.log.debug('Writing code to file\n{}'.format(python_code))
            f.write(python_code)

    def _generate_virtualenv_cmd(self, tmp_dir):
        cmd = ['virtualenv', tmp_dir]
        if self.system_site_packages:
            cmd.append('--system-site-packages')
        if self.python_version is not None:
            cmd.append('--python=python{}'.format(self.python_version))
        return cmd

    def _generate_pip_install_cmd(self, tmp_dir):
        if len(self.requirements) == 0:
            return []
        else:
            cmd = [
             '{}/bin/pip'.format(tmp_dir), 'install']
            return cmd + self.requirements

    @staticmethod
    def _generate_python_cmd(tmp_dir, script_filename, input_filename, output_filename, string_args_filename):
        return [
         '{}/bin/python'.format(tmp_dir), script_filename,
         input_filename, output_filename, string_args_filename]

    def _generate_python_code(self):
        if self.use_dill:
            pickling_library = 'dill'
        else:
            pickling_library = 'pickle'
        fn = self.python_callable
        if self._pass_op_args():
            load_args_line = 'with open(sys.argv[1], "rb") as f: arg_dict = {}.load(f)'.format(pickling_library)
        else:
            load_args_line = 'arg_dict = {"args": [], "kwargs": {}}'
        return dedent('        import {pickling_library}\n        import sys\n        {load_args_code}\n        args = arg_dict["args"]\n        kwargs = arg_dict["kwargs"]\n        with open(sys.argv[3], \'r\') as f:\n            virtualenv_string_args = list(map(lambda x: x.strip(), list(f)))\n        {python_callable_lines}\n        res = {python_callable_name}(*args, **kwargs)\n        with open(sys.argv[2], \'wb\') as f:\n            res is not None and {pickling_library}.dump(res, f)\n        ').format(load_args_code=load_args_line, python_callable_lines=(dedent(inspect.getsource(fn))),
          python_callable_name=(fn.__name__),
          pickling_library=pickling_library)