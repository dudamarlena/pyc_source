# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/output/result_encoder.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 5118 bytes
from __future__ import print_function
import datetime, json, os, dateutil
from sqlitedict import SqliteDict
from ScoutSuite import DEFAULT_REPORT_DIRECTORY
from ScoutSuite.core.console import print_exception, print_info
from ScoutSuite.output.utils import get_filename, prompt_for_overwrite

class ScoutJsonEncoder(json.JSONEncoder):
    __doc__ = '\n    JSON encoder class\n    '

    def default(self, o):
        try:
            if type(o) == datetime.datetime:
                return str(o)
            if hasattr(o, 'profile'):
                del o.profile
            if hasattr(o, 'credentials'):
                del o.credentials
            if hasattr(o, 'metadata_path'):
                del o.metadata_path
            if hasattr(o, 'services_config'):
                del o.services_config
            return vars(o)
        except Exception as e:
            try:
                return str(o)
            finally:
                e = None
                del e


class ScoutResultEncoder(object):

    def __init__(self, report_name=None, report_dir=None, timestamp=None):
        self.report_name = report_name
        if self.report_name:
            self.report_name = report_name.replace('/', '_').replace('\\', '_')
        self.report_dir = report_dir if report_dir else DEFAULT_REPORT_DIRECTORY
        self.current_time = datetime.datetime.now(dateutil.tz.tzlocal())
        self.timestamp = self.current_time.strftime('%Y-%m-%d_%Hh%M%z') if not timestamp else timestamp

    @staticmethod
    def to_dict(config):
        return json.loads(json.dumps(config, separators=(',', ': '), cls=ScoutJsonEncoder))


class SqlLiteEncoder(ScoutResultEncoder):

    def load_from_file(self, config_type, config_path=None):
        if not config_path:
            config_path, _ = get_filename(config_type, self.report_name, self.report_dir)
        return SqliteDict(config_path, autocommit=True).data

    def save_to_file(self, config, config_type, force_write, _debug):
        config_path, first_line = get_filename(config_type, (self.report_name), (self.report_dir), file_extension='db')
        print_info('Saving data to %s' % config_path)
        try:
            with self._SqlLiteEncoder__open_file(config_path, force_write) as (database):
                result_dict = self.to_dict(config)
                for k, v in result_dict.items():
                    database[k] = v

                database.commit()
        except Exception as e:
            try:
                print_exception(e)
            finally:
                e = None
                del e

    @staticmethod
    def __open_file(config_filename, force_write):
        """

        :param config_filename:
        :param force_write:
        :param quiet:
        :return:
        """
        if prompt_for_overwrite(config_filename, force_write):
            try:
                config_dirname = os.path.dirname(config_filename)
                if not os.path.isdir(config_dirname):
                    os.makedirs(config_dirname)
                if os.path.exists(config_filename):
                    os.remove(config_filename)
                return SqliteDict(config_filename)
            except Exception as e:
                try:
                    print_exception(e)
                finally:
                    e = None
                    del e

        else:
            return


class JavaScriptEncoder(ScoutResultEncoder):
    __doc__ = '\n    Reader/Writer for JS and JSON files\n    '

    def load_from_file(self, file_type, file_path=None, first_line=None):
        if not file_path:
            file_path, first_line = get_filename(file_type, self.report_name, self.report_dir)
        with open(file_path, 'rt') as (f):
            json_payload = f.readlines()
            if first_line:
                json_payload.pop(0)
            json_payload = ''.join(json_payload)
        return json.loads(json_payload)

    def save_to_file(self, content, file_type, force_write, debug):
        config_path, first_line = get_filename(file_type, self.report_name, self.report_dir)
        print_info('Saving data to %s' % config_path)
        try:
            with self._JavaScriptEncoder__open_file(config_path, force_write) as (f):
                if first_line:
                    print(('%s' % first_line), file=f)
                print(('%s' % json.dumps(content, indent=(4 if debug else None), separators=(',',
                                                                                             ': '), sort_keys=True, cls=ScoutJsonEncoder)),
                  file=f)
        except AttributeError as e:
            try:
                pass
            finally:
                e = None
                del e

        except Exception as e:
            try:
                print_exception(e)
            finally:
                e = None
                del e

    @staticmethod
    def __open_file(config_filename, force_write):
        """

        :param config_filename:
        :param force_write:
        :param quiet:
        :return:
        """
        if prompt_for_overwrite(config_filename, force_write):
            try:
                config_dirname = os.path.dirname(config_filename)
                if not os.path.isdir(config_dirname):
                    os.makedirs(config_dirname)
                return open(config_filename, 'wt')
            except Exception as e:
                try:
                    print_exception(e)
                finally:
                    e = None
                    del e

        else:
            return