# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/es_task_handler.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 10718 bytes
import elasticsearch, logging, sys, pendulum
from elasticsearch_dsl import Search
from airflow.utils import timezone
from airflow.utils.helpers import parse_template_string
from airflow.utils.log.file_task_handler import FileTaskHandler
from airflow.utils.log.json_formatter import JSONFormatter
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.configuration import conf

class ElasticsearchTaskHandler(FileTaskHandler, LoggingMixin):
    PAGE = 0
    MAX_LINE_PER_PAGE = 1000

    def __init__(self, base_log_folder, filename_template, log_id_template, end_of_log_mark, write_stdout, json_format, json_fields, host='localhost:9200', es_kwargs=conf.getsection('elasticsearch_configs') or {}):
        """
        :param base_log_folder: base folder to store logs locally
        :param log_id_template: log id template
        :param host: Elasticsearch host name
        """
        super(ElasticsearchTaskHandler, self).__init__(base_log_folder, filename_template)
        self.closed = False
        self.log_id_template, self.log_id_jinja_template = parse_template_string(log_id_template)
        self.client = (elasticsearch.Elasticsearch)([host], **es_kwargs)
        self.mark_end_on_close = True
        self.end_of_log_mark = end_of_log_mark
        self.write_stdout = write_stdout
        self.json_format = json_format
        self.json_fields = [label.strip() for label in json_fields.split(',')]
        self.handler = None

    def _render_log_id(self, ti, try_number):
        if self.log_id_jinja_template:
            jinja_context = ti.get_template_context()
            jinja_context['try_number'] = try_number
            return (self.log_id_jinja_template.render)(**jinja_context)
        else:
            if self.json_format:
                execution_date = self._clean_execution_date(ti.execution_date)
            else:
                execution_date = ti.execution_date.isoformat()
            return self.log_id_template.format(dag_id=(ti.dag_id), task_id=(ti.task_id),
              execution_date=execution_date,
              try_number=try_number)

    @staticmethod
    def _clean_execution_date(execution_date):
        """
        Clean up an execution date so that it is safe to query in elasticsearch
        by removing reserved characters.
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters
        :param execution_date: execution date of the dag run.
        """
        return execution_date.strftime('%Y_%m_%dT%H_%M_%S_%f')

    def _read(self, ti, try_number, metadata=None):
        """
        Endpoint for streaming log.
        :param ti: task instance object
        :param try_number: try_number of the task instance
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        :return: a list of log documents and metadata.
        """
        if not metadata:
            metadata = {'offset': 0}
        else:
            if 'offset' not in metadata:
                metadata['offset'] = 0
            offset = metadata['offset']
            log_id = self._render_log_id(ti, try_number)
            logs = self.es_read(log_id, offset, metadata)
            next_offset = offset if not logs else logs[(-1)].offset
            metadata['offset'] = str(next_offset)
            metadata['end_of_log'] = False if not logs else logs[(-1)].message == self.end_of_log_mark.strip()
            cur_ts = pendulum.now()
            if 'last_log_timestamp' in metadata:
                last_log_ts = timezone.parse(metadata['last_log_timestamp'])
                if cur_ts.diff(last_log_ts).in_minutes() >= 5 or 'max_offset' in metadata and offset >= metadata['max_offset']:
                    metadata['end_of_log'] = True
            if offset != next_offset or 'last_log_timestamp' not in metadata:
                metadata['last_log_timestamp'] = str(cur_ts)
        i = len(logs) if not metadata['end_of_log'] else len(logs) - 1
        message = '\n'.join([log.message for log in logs[0:i]])
        return (
         message, metadata)

    def es_read(self, log_id, offset, metadata):
        """
        Returns the logs matching log_id in Elasticsearch and next offset.
        Returns '' if no log is found or there was an error.
        :param log_id: the log_id of the log to read.
        :type log_id: str
        :param offset: the offset start to read log from.
        :type offset: str
        :param metadata: log metadata, used for steaming log download.
        :type metadata: dict
        """
        s = Search(using=(self.client)).query('match_phrase',
          log_id=log_id).sort('offset')
        s = s.filter('range', offset={'gt': int(offset)})
        max_log_line = s.count()
        if 'download_logs' in metadata:
            if metadata['download_logs']:
                if 'max_offset' not in metadata:
                    try:
                        metadata['max_offset'] = s[(max_log_line - 1)].execute()[(-1)].offset if max_log_line > 0 else 0
                    except Exception:
                        self.log.exception('Could not get current log size with log_id: {}'.format(log_id))

        logs = []
        if max_log_line != 0:
            try:
                logs = s[self.MAX_LINE_PER_PAGE * self.PAGE:self.MAX_LINE_PER_PAGE].execute()
            except Exception as e:
                self.log.exception('Could not read log with log_id: %s, error: %s', log_id, str(e))

        return logs

    def set_context(self, ti):
        super(ElasticsearchTaskHandler, self).set_context(ti)
        self.mark_end_on_close = not ti.raw
        if self.write_stdout:
            self.handler = logging.StreamHandler(stream=(sys.__stdout__))
            self.handler.setLevel(self.level)
            if self.json_format:
                if not ti.raw:
                    self.handler.setFormatter(JSONFormatter((self.formatter._fmt), json_fields=(self.json_fields), extras={'dag_id':str(ti.dag_id), 
                     'task_id':str(ti.task_id), 
                     'execution_date':self._clean_execution_date(ti.execution_date), 
                     'try_number':str(ti.try_number)}))
            self.handler.setFormatter(self.formatter)
        else:
            super(ElasticsearchTaskHandler, self).set_context(ti)

    def emit(self, record):
        if self.write_stdout:
            self.formatter.format(record)
            if self.handler is not None:
                self.handler.emit(record)
        else:
            super(ElasticsearchTaskHandler, self).emit(record)

    def flush(self):
        if self.handler is not None:
            self.handler.flush()

    def close(self):
        if self.closed:
            return
        else:
            if not self.mark_end_on_close:
                self.closed = True
                return
            else:
                if self.handler is None:
                    self.closed = True
                    return
                if self.handler.stream is None or self.handler.stream.closed:
                    self.handler.stream = self.handler._open()
            self.handler.emit(logging.makeLogRecord({'msg': self.end_of_log_mark}))
            if self.write_stdout:
                self.handler.close()
                sys.stdout = sys.__stdout__
        super(ElasticsearchTaskHandler, self).close()
        self.closed = True