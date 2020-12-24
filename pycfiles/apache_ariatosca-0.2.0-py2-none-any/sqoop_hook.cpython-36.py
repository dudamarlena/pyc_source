# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/sqoop_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 13950 bytes
__doc__ = '\nThis module contains a sqoop 1.x hook\n'
import subprocess
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from copy import deepcopy

class SqoopHook(BaseHook):
    """SqoopHook"""

    def __init__(self, conn_id='sqoop_default', verbose=False, num_mappers=None, hcatalog_database=None, hcatalog_table=None, properties=None):
        self.conn = self.get_connection(conn_id)
        connection_parameters = self.conn.extra_dejson
        self.job_tracker = connection_parameters.get('job_tracker', None)
        self.namenode = connection_parameters.get('namenode', None)
        self.libjars = connection_parameters.get('libjars', None)
        self.files = connection_parameters.get('files', None)
        self.archives = connection_parameters.get('archives', None)
        self.password_file = connection_parameters.get('password_file', None)
        self.hcatalog_database = hcatalog_database
        self.hcatalog_table = hcatalog_table
        self.verbose = verbose
        self.num_mappers = num_mappers
        self.properties = properties or {}
        self.log.info('Using connection to: {}:{}/{}'.format(self.conn.host, self.conn.port, self.conn.schema))

    def get_conn(self):
        return self.conn

    def cmd_mask_password(self, cmd_orig):
        cmd = deepcopy(cmd_orig)
        try:
            password_index = cmd.index('--password')
            cmd[password_index + 1] = 'MASKED'
        except ValueError:
            self.log.debug('No password in sqoop cmd')

        return cmd

    def Popen(self, cmd, **kwargs):
        """
        Remote Popen

        :param cmd: command to remotely execute
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        :return: handle to subprocess
        """
        masked_cmd = ' '.join(self.cmd_mask_password(cmd))
        self.log.info('Executing command: {}'.format(masked_cmd))
        self.sp = (subprocess.Popen)(
 cmd, stdout=subprocess.PIPE, 
         stderr=subprocess.STDOUT, **kwargs)
        for line in iter(self.sp.stdout):
            self.log.info(line.strip())

        self.sp.wait()
        self.log.info('Command exited with return code %s', self.sp.returncode)
        if self.sp.returncode:
            raise AirflowException('Sqoop command failed: {}'.format(masked_cmd))

    def _prepare_command(self, export=False):
        sqoop_cmd_type = 'export' if export else 'import'
        connection_cmd = ['sqoop', sqoop_cmd_type]
        for key, value in self.properties.items():
            connection_cmd += ['-D', '{}={}'.format(key, value)]

        if self.namenode:
            connection_cmd += ['-fs', self.namenode]
        if self.job_tracker:
            connection_cmd += ['-jt', self.job_tracker]
        if self.libjars:
            connection_cmd += ['-libjars', self.libjars]
        if self.files:
            connection_cmd += ['-files', self.files]
        if self.archives:
            connection_cmd += ['-archives', self.archives]
        if self.conn.login:
            connection_cmd += ['--username', self.conn.login]
        if self.conn.password:
            connection_cmd += ['--password', self.conn.password]
        if self.password_file:
            connection_cmd += ['--password-file', self.password_file]
        if self.verbose:
            connection_cmd += ['--verbose']
        if self.num_mappers:
            connection_cmd += ['--num-mappers', str(self.num_mappers)]
        if self.hcatalog_database:
            connection_cmd += ['--hcatalog-database', self.hcatalog_database]
        if self.hcatalog_table:
            connection_cmd += ['--hcatalog-table', self.hcatalog_table]
        connection_cmd += ['--connect',
         '{}:{}/{}'.format(self.conn.host, self.conn.port, self.conn.schema)]
        return connection_cmd

    @staticmethod
    def _get_export_format_argument(file_type='text'):
        if file_type == 'avro':
            return ['--as-avrodatafile']
        else:
            if file_type == 'sequence':
                return ['--as-sequencefile']
            if file_type == 'parquet':
                return ['--as-parquetfile']
            if file_type == 'text':
                return ['--as-textfile']
        raise AirflowException("Argument file_type should be 'avro', 'sequence', 'parquet' or 'text'.")

    def _import_cmd(self, target_dir, append, file_type, split_by, direct, driver, extra_import_options):
        cmd = self._prepare_command(export=False)
        if target_dir:
            cmd += ['--target-dir', target_dir]
        if append:
            cmd += ['--append']
        cmd += self._get_export_format_argument(file_type)
        if split_by:
            cmd += ['--split-by', split_by]
        if direct:
            cmd += ['--direct']
        if driver:
            cmd += ['--driver', driver]
        if extra_import_options:
            for key, value in extra_import_options.items():
                cmd += ['--{}'.format(key)]
                if value:
                    cmd += [str(value)]

        return cmd

    def import_table(self, table, target_dir=None, append=False, file_type='text', columns=None, split_by=None, where=None, direct=False, driver=None, extra_import_options=None):
        """
        Imports table from remote location to target dir. Arguments are
        copies of direct sqoop command line arguments

        :param table: Table to read
        :param target_dir: HDFS destination dir
        :param append: Append data to an existing dataset in HDFS
        :param file_type: "avro", "sequence", "text" or "parquet".
            Imports data to into the specified format. Defaults to text.
        :param columns: <col,col,col…> Columns to import from table
        :param split_by: Column of the table used to split work units
        :param where: WHERE clause to use during import
        :param direct: Use direct connector if exists for the database
        :param driver: Manually specify JDBC driver class to use
        :param extra_import_options: Extra import options to pass as dict.
            If a key doesn't have a value, just pass an empty string to it.
            Don't include prefix of -- for sqoop options.
        """
        cmd = self._import_cmd(target_dir, append, file_type, split_by, direct, driver, extra_import_options)
        cmd += ['--table', table]
        if columns:
            cmd += ['--columns', columns]
        if where:
            cmd += ['--where', where]
        self.Popen(cmd)

    def import_query(self, query, target_dir, append=False, file_type='text', split_by=None, direct=None, driver=None, extra_import_options=None):
        """
        Imports a specific query from the rdbms to hdfs

        :param query: Free format query to run
        :param target_dir: HDFS destination dir
        :param append: Append data to an existing dataset in HDFS
        :param file_type: "avro", "sequence", "text" or "parquet"
            Imports data to hdfs into the specified format. Defaults to text.
        :param split_by: Column of the table used to split work units
        :param direct: Use direct import fast path
        :param driver: Manually specify JDBC driver class to use
        :param extra_import_options: Extra import options to pass as dict.
            If a key doesn't have a value, just pass an empty string to it.
            Don't include prefix of -- for sqoop options.
        """
        cmd = self._import_cmd(target_dir, append, file_type, split_by, direct, driver, extra_import_options)
        cmd += ['--query', query]
        self.Popen(cmd)

    def _export_cmd(self, table, export_dir, input_null_string, input_null_non_string, staging_table, clear_staging_table, enclosed_by, escaped_by, input_fields_terminated_by, input_lines_terminated_by, input_optionally_enclosed_by, batch, relaxed_isolation, extra_export_options):
        cmd = self._prepare_command(export=True)
        if input_null_string:
            cmd += ['--input-null-string', input_null_string]
        if input_null_non_string:
            cmd += ['--input-null-non-string', input_null_non_string]
        if staging_table:
            cmd += ['--staging-table', staging_table]
        if clear_staging_table:
            cmd += ['--clear-staging-table']
        if enclosed_by:
            cmd += ['--enclosed-by', enclosed_by]
        if escaped_by:
            cmd += ['--escaped-by', escaped_by]
        if input_fields_terminated_by:
            cmd += ['--input-fields-terminated-by', input_fields_terminated_by]
        if input_lines_terminated_by:
            cmd += ['--input-lines-terminated-by', input_lines_terminated_by]
        if input_optionally_enclosed_by:
            cmd += ['--input-optionally-enclosed-by',
             input_optionally_enclosed_by]
        if batch:
            cmd += ['--batch']
        if relaxed_isolation:
            cmd += ['--relaxed-isolation']
        if export_dir:
            cmd += ['--export-dir', export_dir]
        if extra_export_options:
            for key, value in extra_export_options.items():
                cmd += ['--{}'.format(key)]
                if value:
                    cmd += [str(value)]

        cmd += ['--table', table]
        return cmd

    def export_table(self, table, export_dir, input_null_string, input_null_non_string, staging_table, clear_staging_table, enclosed_by, escaped_by, input_fields_terminated_by, input_lines_terminated_by, input_optionally_enclosed_by, batch, relaxed_isolation, extra_export_options=None):
        """
        Exports Hive table to remote location. Arguments are copies of direct
        sqoop command line Arguments

        :param table: Table remote destination
        :param export_dir: Hive table to export
        :param input_null_string: The string to be interpreted as null for
            string columns
        :param input_null_non_string: The string to be interpreted as null
            for non-string columns
        :param staging_table: The table in which data will be staged before
            being inserted into the destination table
        :param clear_staging_table: Indicate that any data present in the
            staging table can be deleted
        :param enclosed_by: Sets a required field enclosing character
        :param escaped_by: Sets the escape character
        :param input_fields_terminated_by: Sets the field separator character
        :param input_lines_terminated_by: Sets the end-of-line character
        :param input_optionally_enclosed_by: Sets a field enclosing character
        :param batch: Use batch mode for underlying statement execution
        :param relaxed_isolation: Transaction isolation to read uncommitted
            for the mappers
        :param extra_export_options: Extra export options to pass as dict.
            If a key doesn't have a value, just pass an empty string to it.
            Don't include prefix of -- for sqoop options.
        """
        cmd = self._export_cmd(table, export_dir, input_null_string, input_null_non_string, staging_table, clear_staging_table, enclosed_by, escaped_by, input_fields_terminated_by, input_lines_terminated_by, input_optionally_enclosed_by, batch, relaxed_isolation, extra_export_options)
        self.Popen(cmd)