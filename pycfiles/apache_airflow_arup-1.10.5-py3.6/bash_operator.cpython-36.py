# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/bash_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5249 bytes
import os, signal
from subprocess import Popen, STDOUT, PIPE
from tempfile import gettempdir, NamedTemporaryFile
from builtins import bytes
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.file import TemporaryDirectory
from airflow.utils.operator_helpers import context_to_airflow_vars

class BashOperator(BaseOperator):
    __doc__ = "\n    Execute a Bash script, command or set of commands.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:BashOperator`\n\n    :param bash_command: The command, set of commands or reference to a\n        bash script (must be '.sh') to be executed. (templated)\n    :type bash_command: str\n    :param xcom_push: If xcom_push is True, the last line written to stdout\n        will also be pushed to an XCom when the bash command completes.\n    :type xcom_push: bool\n    :param env: If env is not None, it must be a mapping that defines the\n        environment variables for the new process; these are used instead\n        of inheriting the current process environment, which is the default\n        behavior. (templated)\n    :type env: dict\n    :param output_encoding: Output encoding of bash command\n    :type output_encoding: str\n    "
    template_fields = ('bash_command', 'env')
    template_ext = ('.sh', '.bash')
    ui_color = '#f0ede4'

    @apply_defaults
    def __init__(self, bash_command, xcom_push=False, env=None, output_encoding='utf-8', *args, **kwargs):
        (super(BashOperator, self).__init__)(*args, **kwargs)
        self.bash_command = bash_command
        self.env = env
        self.xcom_push_flag = xcom_push
        self.output_encoding = output_encoding

    def execute(self, context):
        """
        Execute the bash command in a temporary directory
        which will be cleaned afterwards
        """
        self.log.info('Tmp dir root location: \n %s', gettempdir())
        env = self.env
        if env is None:
            env = os.environ.copy()
        airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
        self.log.info('Exporting the following env vars:\n%s', '\n'.join(['{}={}'.format(k, v) for k, v in airflow_context_vars.items()]))
        env.update(airflow_context_vars)
        self.lineage_data = self.bash_command
        with TemporaryDirectory(prefix='airflowtmp') as (tmp_dir):
            with NamedTemporaryFile(dir=tmp_dir, prefix=(self.task_id)) as (f):
                f.write(bytes(self.bash_command, 'utf_8'))
                f.flush()
                fname = f.name
                script_location = os.path.abspath(fname)
                self.log.info('Temporary script location: %s', script_location)

                def pre_exec():
                    for sig in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                        if hasattr(signal, sig):
                            signal.signal(getattr(signal, sig), signal.SIG_DFL)

                    os.setsid()

                self.log.info('Running command: %s', self.bash_command)
                sp = Popen([
                 'bash', fname],
                  stdout=PIPE,
                  stderr=STDOUT,
                  cwd=tmp_dir,
                  env=env,
                  preexec_fn=pre_exec)
                self.sp = sp
                self.log.info('Output:')
                line = ''
                for line in iter(sp.stdout.readline, b''):
                    line = line.decode(self.output_encoding).rstrip()
                    self.log.info(line)

                sp.wait()
                self.log.info('Command exited with return code %s', sp.returncode)
                if sp.returncode:
                    raise AirflowException('Bash command failed')
        if self.xcom_push_flag:
            return line

    def on_kill(self):
        self.log.info('Sending SIGTERM signal to bash process group')
        os.killpg(os.getpgid(self.sp.pid), signal.SIGTERM)