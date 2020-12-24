# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/csv.py
# Compiled at: 2017-11-24 11:42:25
# Size of source mod 2**32: 2985 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import csv
from wasp_general.verify import verify_type, verify_value

class WCSVExporter:

    @verify_type(titles=bool)
    def __init__(self, output_obj, titles=True, **csv_fmtparams):
        self._WCSVExporter__output_obj = output_obj
        self._WCSVExporter__titles = titles
        self._WCSVExporter__csv_fmtparams = csv_fmtparams
        self._WCSVExporter__csv_writer = None
        self._WCSVExporter__omitted_fields = set()

    def output_obj(self):
        return self._WCSVExporter__output_obj

    def titles(self):
        return self._WCSVExporter__titles

    def csv_fmtparams(self):
        return self._WCSVExporter__csv_fmtparams

    @verify_type(field_name=str)
    @verify_value(field_name=lambda x: len(x) > 0)
    def omit_field(self, field_name):
        self._WCSVExporter__omitted_fields.add(field_name)

    def omitted_fields(self):
        return tuple(self._WCSVExporter__omitted_fields)

    @verify_type(dict_record=dict)
    def export(self, dict_record):
        dict_record = self._WCSVExporter__filter_field(dict_record)
        if self._WCSVExporter__csv_writer is None:
            self.export_titles(dict_record)
        self._WCSVExporter__check_record(dict_record)
        self._WCSVExporter__csv_writer.writerow(dict_record)

    @verify_type(dict_record=dict)
    def export_titles(self, dict_record):
        if self._WCSVExporter__csv_writer is not None:
            raise RuntimeError('Unable to export titles multiple time')
        fields = dict_record.keys()
        self._WCSVExporter__csv_writer = csv.DictWriter(self.output_obj(), fieldnames=fields, **self.csv_fmtparams())
        if self.titles() is True:
            self._WCSVExporter__csv_writer.writeheader()

    @verify_type(dict_record=dict)
    def __filter_field(self, dict_record):
        result = dict_record.copy()
        for field in self.omitted_fields():
            if field in result.keys():
                result.pop(field)
                continue

        return result

    @verify_type(dict_record=dict)
    def __check_record(self, dict_record):
        for key, value in dict_record.items():
            if isinstance(key, str) is False:
                raise TypeError('Invalid field name')
            if value is not None and isinstance(value, (str, int, float)) is False:
                raise TypeError('Invalid value for field "%s"' % key)
                continue