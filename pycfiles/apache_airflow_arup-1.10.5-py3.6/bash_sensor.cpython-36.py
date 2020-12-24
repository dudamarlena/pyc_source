# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/bash_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3530 bytes
from builtins import bytes
import os
from subprocess import Popen, STDOUT, PIPE
from tempfile import gettempdir, NamedTemporaryFile
from airflow.utils.decorators import apply_defaults
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.file import TemporaryDirectory

class BashSensor(BaseSensorOperator):
    __doc__ = "\n    Executes a bash command/script and returns True if and only if the\n    return code is 0.\n\n    :param bash_command: The command, set of commands or reference to a\n        bash script (must be '.sh') to be executed.\n    :type bash_command: str\n\n    :param env: If env is not None, it must be a mapping that defines the\n        environment variables for the new process; these are used instead\n        of inheriting the current process environment, which is the default\n        behavior. (templated)\n    :type env: dict\n    :param output_encoding: output encoding of bash command.\n    :type output_encoding: str\n    "
    template_fields = ('bash_command', 'env')

    @apply_defaults
    def __init__(self, bash_command, env=None, output_encoding='utf-8', *args, **kwargs):
        (super(BashSensor, self).__init__)(*args, **kwargs)
        self.bash_command = bash_command
        self.env = env
        self.output_encoding = output_encoding

    def poke(self, context):
        """
        Execute the bash command in a temporary directory
        which will be cleaned afterwards
        """
        bash_command = self.bash_command
        self.log.info('Tmp dir root location: \n %s', gettempdir())
        with TemporaryDirectory(prefix='airflowtmp') as (tmp_dir):
            with NamedTemporaryFile(dir=tmp_dir, prefix=(self.task_id)) as (f):
                f.write(bytes(bash_command, 'utf_8'))
                f.flush()
                fname = f.name
                script_location = tmp_dir + '/' + fname
                self.log.info('Temporary script location: %s', script_location)
                self.log.info('Running command: %s', bash_command)
                sp = Popen([
                 'bash', fname],
                  stdout=PIPE,
                  stderr=STDOUT,
                  close_fds=True,
                  cwd=tmp_dir,
                  env=(self.env),
                  preexec_fn=(os.setsid))
                self.sp = sp
                self.log.info('Output:')
                line = ''
                for line in iter(sp.stdout.readline, b''):
                    line = line.decode(self.output_encoding).strip()
                    self.log.info(line)

                sp.wait()
                self.log.info('Command exited with return code %s', sp.returncode)
                return not sp.returncode