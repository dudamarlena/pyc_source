# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\datasource.py
# Compiled at: 2016-04-03 07:05:43
# Size of source mod 2**32: 4014 bytes
from datetime import datetime
from io import StringIO
from os import makedirs
from os.path import exists, dirname
from re import search
from mad.log import FileLog
from mad.evaluation import Simulation
from mad.monitoring import CSVReportFactory

class Settings:
    TRACE_FILE = 'trace.log'
    REPORT_NAME = '%s.log'

    @staticmethod
    def new_identifier():
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Project:
    __doc__ = "\n    Represent a simulation 'request'\n    "

    def __init__(self, root_mad_file, limit):
        self.file_name = root_mad_file
        self.limit = limit

    @property
    def root_file(self):
        return self.file_name

    @property
    def name(self):
        match = search('([^\\\\/]+)\\.(\\w+)$', self.file_name)
        if match:
            return match.group(1)
        else:
            return self.file_name

    @property
    def output_directory(self):
        return '%s_%s' % (self.name, Settings.new_identifier())

    @property
    def log_file(self):
        return '%s/%s' % (self.output_directory, Settings.TRACE_FILE)

    def report_for(self, entity_name):
        report_name = Settings.REPORT_NAME % entity_name
        return '%s/%s' % (self.output_directory, report_name)


class Mad:
    __doc__ = '\n    Represent the simulation engine. It access the repository, parse the model and\n    build the simulation.\n    '

    def __init__(self, parser, output):
        self.parser = parser
        self.output = output

    def load(self, project):
        logger = self._create_logger(project.log_file)
        simulation = Simulation(logger, CSVReportFactory(project, self.output))
        expression = self.parser.parse(project.root_file)
        simulation.evaluate(expression)
        return simulation

    def _create_logger(self, file_name):
        return FileLog(self.output.open_stream_to(file_name), '%5d %-20s %-s\n')


class DataSource:
    __doc__ = '\n    Unified interface for opening resources, identified by name\n    '

    @staticmethod
    def open_stream_to(path):
        raise NotImplementedError('Method Repository::open_stream_to is abstract')

    @staticmethod
    def read(model):
        raise NotImplementedError('Method Repository::read is abstract')


class InFilesDataSource(DataSource):
    __doc__ = '\n    Represent a source where data are stored on the file systems\n    '

    @staticmethod
    def open_stream_to(path):
        if not exists(path):
            makedirs(dirname(path), exist_ok=True)
        return open(path, 'w+')

    @staticmethod
    def read(model):
        with open(model) as (file):
            return file.read()


class InMemoryDataSource(DataSource):
    __doc__ = '\n    A data source that holds data in memory, in a hash map\n    '

    def __init__(self, streams={}):
        self.streams = streams

    def open_stream_to(self, path):
        if path not in self.streams:
            self.streams[path] = StringIO()
        return self.streams[path]

    def read(self, model):
        if model not in self.streams:
            raise RuntimeError("Unknown resource '%s' (Candidates are %s)" % (model, str(self.streams.keys())))
        else:
            return self.streams[model]