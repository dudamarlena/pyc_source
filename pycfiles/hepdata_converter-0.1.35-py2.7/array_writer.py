# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/writers/array_writer.py
# Compiled at: 2020-03-05 14:33:22
import logging
from math import sqrt
import os
from hepdata_converter.common import Option
from hepdata_converter.writers import Writer
import abc
from hepdata_converter.writers.utils import error_value_processor
logging.basicConfig()
log = logging.getLogger(__name__)

class ObjectWrapper(object):
    __metaclass__ = abc.ABCMeta
    accept_alphanumeric = True
    core_object = True

    @classmethod
    def is_number_var(cls, *variables):
        is_number_list = []
        for variable in variables:
            for element in variable['values']:
                if 'value' in element and isinstance(element['value'], (str, unicode)):
                    try:
                        element['value'] = float(element['value'])
                        is_number_list.append(True)
                    except ValueError:
                        is_number_list.append(False)

                else:
                    is_number_list.append(True)

        return is_number_list

    @classmethod
    def sanitize_name(cls, name):
        return name.replace(' ', '_').replace('/', '_')

    @classmethod
    def is_value_var(cls, variable):
        return cls._is_attr_variable('value', variable)

    @classmethod
    def is_range_var(cls, variable):
        return cls._is_attr_variable('high', variable) and cls._is_attr_variable('low', variable)

    @classmethod
    def has_errors(cls, variable):
        return cls._is_attr_variable('errors', variable)

    @classmethod
    def _is_attr_variable(cls, attr_name, variable):
        for element in variable['values']:
            if attr_name not in element:
                return False

        return True

    def __init__(self, independent_variable_map, dependent_variable, dependent_variable_index):
        self.xval = []
        self.yval = []
        self.xerr_minus = []
        self.xerr_plus = []
        self.yerr_minus = []
        self.yerr_plus = []
        self.err_breakdown = {}
        self.independent_variables = list(independent_variable_map)
        self.independent_variable_map = independent_variable_map
        self.dependent_variable = dependent_variable
        self.dependent_variable_index = dependent_variable_index

    @classmethod
    def match(cls, independent_variables_map, dependent_variable):
        if not cls.accept_alphanumeric:
            for independent_variable in independent_variables_map:
                if False in cls.is_number_var(independent_variable):
                    return False

            if False in cls.is_number_var(dependent_variable):
                return False
        return True

    @classmethod
    def match_and_create(cls, independent_variables_map, dependent_variable, dependent_variable_index):
        if cls.match(independent_variables_map, dependent_variable):
            return cls(independent_variables_map, dependent_variable, dependent_variable_index).create_objects()
        return []

    def calculate_total_errors(self):
        is_number_list = self.is_number_var(self.dependent_variable)
        for independent_variable in self.independent_variable_map:
            xerr_minus = []
            self.xerr_minus.append(xerr_minus)
            xerr_plus = []
            self.xerr_plus.append(xerr_plus)
            xval = []
            self.xval.append(xval)
            ArrayWriter.calculate_total_errors(independent_variable, is_number_list, xerr_minus, xerr_plus, xval)

        ArrayWriter.calculate_total_errors(self.dependent_variable, is_number_list, self.yerr_minus, self.yerr_plus, self.yval, self.err_breakdown)

    @abc.abstractmethod
    def create_objects(self):
        pass


class ObjectFactory(object):

    def __init__(self, class_list, independent_variables, dependent_variables):
        self.class_list = class_list
        self.map = {}
        self.independent_variables = independent_variables
        self.dependent_variables = dependent_variables
        for variable_index in xrange(len(dependent_variables)):
            self.map[variable_index] = list(independent_variables)

    def get_next_object(self):
        for dependent_variable_index in xrange(len(self.dependent_variables)):
            auxiliary_object_created = False
            for class_wrapper in self.class_list:
                if not class_wrapper.core_object and auxiliary_object_created:
                    continue
                objects = class_wrapper.match_and_create(self.map[dependent_variable_index], self.dependent_variables[dependent_variable_index], dependent_variable_index)
                if objects and not class_wrapper.core_object:
                    auxiliary_object_created = True
                for obj in objects:
                    yield obj


class ArrayWriter(Writer):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def process_error_labels(value):
        """ Process the error labels of a dependent variable 'value' to ensure uniqueness. """
        observed_error_labels = {}
        for error in value.get('errors', []):
            label = error.get('label', 'error')
            if label not in observed_error_labels:
                observed_error_labels[label] = 0
            observed_error_labels[label] += 1
            if observed_error_labels[label] > 1:
                error['label'] = label + '_' + str(observed_error_labels[label])
            if observed_error_labels[label] == 2:
                for error1 in value.get('errors', []):
                    error1_label = error1.get('label', 'error')
                    if error1_label == label:
                        error1['label'] = label + '_1'
                        break

    @staticmethod
    def calculate_total_errors(variable, is_number_list, min_errs, max_errs, values, err_breakdown={}):
        i_numeric = -1
        for i, entry in enumerate(variable['values']):
            if not is_number_list[i]:
                continue
            else:
                i_numeric += 1
            if 'value' in entry:
                values.append(entry['value'])
                if 'errors' in entry:
                    errors_min = 0.0
                    errors_max = 0.0
                    err_breakdown[i_numeric] = {}
                    ArrayWriter.process_error_labels(entry)
                    for error in entry['errors']:
                        label = error.get('label', 'error')
                        err_breakdown[i_numeric][label] = {}
                        if 'asymerror' in error:
                            try:
                                err_minus = error_value_processor(entry['value'], error['asymerror']['minus'])
                                err_plus = error_value_processor(entry['value'], error['asymerror']['plus'])
                                errors_min += pow(min(err_plus, err_minus, 0.0), 2)
                                errors_max += pow(max(err_plus, err_minus, 0.0), 2)
                                err_breakdown[i_numeric][label]['up'] = err_plus
                                err_breakdown[i_numeric][label]['dn'] = err_minus
                            except TypeError:
                                log.error(('TypeError encountered when parsing {0} and {1}').format(unicode(error['asymerror']['minus']).encode('utf8', 'replace'), unicode(error['asymerror']['plus']).encode('utf8', 'replace')))

                        elif 'symerror' in error:
                            try:
                                err = error_value_processor(entry['value'], error['symerror'])
                                errors_min += pow(err, 2)
                                errors_max += pow(err, 2)
                                err_breakdown[i_numeric][label]['up'] = err
                                err_breakdown[i_numeric][label]['dn'] = -err
                            except TypeError:
                                log.error(('TypeError encountered when parsing {0}').format(unicode(error['symerror']).encode('utf8', 'replace')))

                    min_errs.append(sqrt(errors_min))
                    max_errs.append(sqrt(errors_max))
                elif 'low' in entry and 'high' in entry:
                    min_errs.append(entry['value'] - entry['low'])
                    max_errs.append(entry['high'] - entry['value'])
                else:
                    min_errs.append(0.0)
                    max_errs.append(0.0)
            else:
                middle_val = (entry['high'] - entry['low']) * 0.5 + entry['low']
                values.append(middle_val)
                min_errs.append(middle_val - entry['low'])
                max_errs.append(entry['high'] - middle_val)

    @classmethod
    def options(cls):
        options = super(ArrayWriter, cls).options()
        options['table'] = Option('table', 't', required=False, variable_mapping='table_id', default=None, help='Specifies which table should be exported, if not specified all tables will be exported (in this case output must be a directory, not a file)')
        return options

    def __init__(self, *args, **kwargs):
        kwargs['single_file_output'] = True
        super(ArrayWriter, self).__init__(*args, **kwargs)
        self.tables = []
        self.extension = None
        return

    @abc.abstractmethod
    def _write_table(self, data_out, table):
        pass

    def _get_tables(self, data_in):
        if self.table_id is not None:
            if isinstance(self.table_id, int):
                self.tables.append(data_in.get_table(id=self.table_id))
            else:
                try:
                    tab = data_in.get_table(file=self.table_id)
                except IndexError:
                    tab = data_in.get_table(name=self.table_id)

                self.tables.append(tab)
        else:
            self.tables = data_in.tables
        return

    def _prepare_outputs(self, data_out, outputs):
        if isinstance(data_out, (str, unicode)):
            self.file_emulation = True
            if self.table_id is not None:
                f = open(data_out, 'w')
                outputs.append(f)
            else:
                self.create_dir(data_out)
                for table in self.tables:
                    outputs.append(open(os.path.join(data_out, table.name.replace(' ', '').replace('/', '-').replace('$', '').replace('\\', '') + '.' + self.extension), 'w'))

        elif len(self.tables) > 1 and not isinstance(data_out, (str, unicode)):
            raise ValueError('Multiple tables, output must be a directory')
        else:
            outputs.append(data_out)
        return

    def write(self, data_in, data_out, *args, **kwargs):
        """

        :param data_in:
        :type data_in: hepconverter.parsers.ParsedData
        :param data_out: filelike object
        :type data_out: file
        :param args:
        :param kwargs:
        """
        self._get_tables(data_in)
        self.file_emulation = False
        outputs = []
        self._prepare_outputs(data_out, outputs)
        for i in xrange(len(self.tables)):
            data_out = outputs[i]
            table = self.tables[i]
            self._write_table(data_out, table)
            if self.file_emulation:
                data_out.close()

    @classmethod
    def _extract_independent_variables(cls, table, headers, data, qualifiers_marks):
        for independent_variable in table.independent_variables:
            name = independent_variable['header']['name']
            if 'units' in independent_variable['header']:
                name += ' [%s]' % independent_variable['header']['units']
            headers.append(unicode(name).encode('utf8', 'replace'))
            x_data = []
            x_data_low = []
            x_data_high = []
            for value in independent_variable['values']:
                if 'high' in value and 'low' in value:
                    x_data_low.append(value['low'])
                    x_data_high.append(value['high'])
                    if 'value' in value:
                        x_data.append(value['value'])
                    else:
                        x_data.append(0.5 * (value['low'] + value['high']))
                else:
                    x_data_low.append(value['value'])
                    x_data_high.append(value['value'])
                    x_data.append(value['value'])

            data.append(x_data)
            if x_data_high != x_data_low:
                data.append(x_data_low)
                data.append(x_data_high)
                header = headers[(-1)]
                headers.append(header + ' LOW')
                qualifiers_marks.append(False)
                headers.append(header + ' HIGH')
                qualifiers_marks.append(False)

    @classmethod
    def _parse_dependent_variable(cls, dependent_variable, headers, qualifiers, qualifiers_marks, data):
        units = ''
        if 'units' in dependent_variable['header']:
            units = ' [%s]' % dependent_variable['header']['units']
        headers.append(unicode(dependent_variable['header']['name'] + units).encode('utf8', 'replace'))
        qualifiers_marks.append(True)
        y_order = []
        y_data = {'values': []}
        y_order.append(y_data['values'])
        for value in dependent_variable['values']:
            cls.process_error_labels(value)
            for error in value.get('errors', []):
                label = error.get('label', 'error')
                if label + '_plus' not in y_data:
                    headers.append(label + ' +')
                    qualifiers_marks.append(False)
                    headers.append(label + ' -')
                    qualifiers_marks.append(False)
                    plus = []
                    y_data[label + '_plus'] = plus
                    y_order.append(plus)
                    minus = []
                    y_data[label + '_minus'] = minus
                    y_order.append(minus)

        for value in dependent_variable['values']:
            y_data['values'].append(value['value'])
            if 'errors' not in value:
                for key, val in y_data.items():
                    if key != 'values':
                        val.append(0)

            else:
                for key, val in y_data.items():
                    has_error = False
                    for i in xrange(len(value.get('errors', []))):
                        error = value['errors'][i]
                        label = error.get('label', 'error')
                        if 'symerror' in error:
                            error_plus = error['symerror']
                            if isinstance(error_plus, (str, unicode)):
                                error_plus = error_plus.strip()
                                if len(error_plus) > 1 and error_plus[0] == '-':
                                    error_minus = error_plus[1:]
                                elif error_plus:
                                    error_minus = '-' + error_plus
                                else:
                                    error_minus = error_plus
                            else:
                                error_minus = -error_plus
                        else:
                            error_plus = error['asymerror']['plus']
                            error_minus = error['asymerror']['minus']
                        if key == label + '_plus':
                            val.append(error_plus)
                            has_error = True
                        elif key == label + '_minus':
                            val.append(error_minus)
                            has_error = True

                    if key != 'values' and not has_error:
                        val.append(0)

        for entry in y_order:
            data.append(entry)

        for qualifier in dependent_variable.get('qualifiers', []):
            units = ''
            if 'units' in qualifier:
                units = ' [%s]' % qualifier['units']
            name = qualifier['name'] + units
            if name not in qualifiers:
                qualifiers[name] = []
            qualifiers[name].append(qualifier['value'])