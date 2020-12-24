# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/pig_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3394 bytes
from __future__ import print_function
import subprocess
from tempfile import NamedTemporaryFile
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.utils.file import TemporaryDirectory

class PigCliHook(BaseHook):
    __doc__ = '\n    Simple wrapper around the pig CLI.\n\n    Note that you can also set default pig CLI properties using the\n    ``pig_properties`` to be used in your connection as in\n    ``{"pig_properties": "-Dpig.tmpfilecompression=true"}``\n\n    '

    def __init__(self, pig_cli_conn_id='pig_cli_default'):
        conn = self.get_connection(pig_cli_conn_id)
        self.pig_properties = conn.extra_dejson.get('pig_properties', '')
        self.conn = conn

    def run_cli(self, pig, pig_opts=None, verbose=True):
        """
        Run an pig script using the pig cli

        >>> ph = PigCliHook()
        >>> result = ph.run_cli("ls /;", pig_opts="-x mapreduce")
        >>> ("hdfs://" in result)
        True
        """
        with TemporaryDirectory(prefix='airflow_pigop_') as (tmp_dir):
            with NamedTemporaryFile(dir=tmp_dir) as (f):
                f.write(pig.encode('utf-8'))
                f.flush()
                fname = f.name
                pig_bin = 'pig'
                cmd_extra = []
                pig_cmd = [
                 pig_bin]
                if self.pig_properties:
                    pig_properties_list = self.pig_properties.split()
                    pig_cmd.extend(pig_properties_list)
                if pig_opts:
                    pig_opts_list = pig_opts.split()
                    pig_cmd.extend(pig_opts_list)
                pig_cmd.extend(['-f', fname] + cmd_extra)
                if verbose:
                    self.log.info('%s', ' '.join(pig_cmd))
                sp = subprocess.Popen(pig_cmd,
                  stdout=(subprocess.PIPE),
                  stderr=(subprocess.STDOUT),
                  cwd=tmp_dir,
                  close_fds=True)
                self.sp = sp
                stdout = ''
                for line in iter(sp.stdout.readline, b''):
                    stdout += line.decode('utf-8')
                    if verbose:
                        self.log.info(line.strip())

                sp.wait()
                if sp.returncode:
                    raise AirflowException(stdout)
                return stdout

    def kill(self):
        if hasattr(self, 'sp'):
            if self.sp.poll() is None:
                print('Killing the Pig job')
                self.sp.kill()