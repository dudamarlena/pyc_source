# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymysqlbatchimport/mysqlimport.py
# Compiled at: 2018-06-16 02:58:19
# Size of source mod 2**32: 3644 bytes
import os, shutil, pathlib, subprocess, mysql.connector
from contextlib import contextmanager

class LoadDataInFile:
    CNF_PRIORITY = 'priority'
    CNF_REPLACEMENT = 'replacement'
    CNF_CHARSET = 'charset'
    CNF_FIELDS_TERMINATED_BY = 'fields_terminated_by'
    CNF_FIELDS_ENCLOSED_BY = 'fields_enclosed_by'
    CNF_FIELDS_ESCAPED_BY = 'fields_escaped_by'
    CNF_LINES_TERMINATED_BY = 'lines_terminated_by'
    CNF_LINES_STARTING_BY = 'lines_starting_by'
    CNF_IGNORE_LINES = 'ignore_lines'
    CNF_COLUMNS = 'columns'
    CNF_SET = 'set'

    def __init__(self, cache_dir, database, table, config):
        self._cache_dir = cache_dir
        self._database = database
        self._table = table
        self._config = config

    @classmethod
    @contextmanager
    def context(cls, **args):
        try:
            cnx = (mysql.connector.connect)(**args)
            yield cnx
        finally:
            cnx.disconnect()

    def run(self, file, ctx_obj):
        conn = ctx_obj
        stmt = self._generate(file.filepath)
        result = conn.cmd_query(stmt)
        return result

    def _generate(self, filepath):
        prepared_stmt = '\n            LOAD DATA {PRIORITY} LOCAL INFILE "{FILE}"\n            {REPLACEMENT}\n            INTO TABLE {TABLE}\n            CHARACTER SET {CHARSET}\n            FIELDS\n                TERMINATED BY {COLUMNS_TERMINATED_BY}\n                ENCLOSED BY {COLUMNS_ENCLOSED_BY}\n                ESCAPED BY {COLUMNS_ESCAPED_BY}\n            LINES\n                STARTING BY {LINES_STARTING_BY}\n                TERMINATED BY {LINES_TERMINATED_BY}\n            IGNORE {IGNORE_LINES} ROWS\n            ({COLUMNS})\n            SET {SET}\n        '
        stmt = prepared_stmt.format(FILE=filepath,
          PRIORITY=(self._config[LoadDataInFile.CNF_PRIORITY]),
          TABLE=(self._table),
          REPLACEMENT=(self._config[LoadDataInFile.CNF_REPLACEMENT]),
          CHARSET=(self._config[LoadDataInFile.CNF_CHARSET]),
          COLUMNS_TERMINATED_BY=(self._config[LoadDataInFile.CNF_FIELDS_TERMINATED_BY]),
          COLUMNS_ENCLOSED_BY=(self._config[LoadDataInFile.CNF_FIELDS_ENCLOSED_BY]),
          COLUMNS_ESCAPED_BY=(self._config[LoadDataInFile.CNF_FIELDS_ESCAPED_BY]),
          LINES_STARTING_BY=(self._config[LoadDataInFile.CNF_LINES_STARTING_BY]),
          LINES_TERMINATED_BY=(self._config[LoadDataInFile.CNF_LINES_TERMINATED_BY]),
          IGNORE_LINES=(self._config[LoadDataInFile.CNF_IGNORE_LINES]),
          COLUMNS=(self._config[LoadDataInFile.CNF_COLUMNS]),
          SET=(self._config[LoadDataInFile.CNF_SET]))
        return stmt


class ImportCommand:

    def __init__(self, command, cache_dir, database, table, config):
        self._cmd = command
        self._cache_dir = cache_dir
        self._database = database
        self._table = table
        self._config = config

    @contextmanager
    @classmethod
    def context(cls, **args):
        yield

    def run(self, file):
        tmp_filename = '%s.%s' % (self._table, file.filename)
        tmp_filepath = str(pathlib.PurePath(os.getcwd(), self._cache_dir, tmp_filename))
        shutil.copy(file.filepath, tmp_filepath)
        cmd = [
         self._cmd,
         '--local',
         '--replace']
        for item in self._config:
            cmd.append('--%s=%s' % (item, self._config[item]))

        cmd.append(self._database)
        cmd.append(tmp_filepath)
        p = subprocess.run(cmd)
        return p.returncode