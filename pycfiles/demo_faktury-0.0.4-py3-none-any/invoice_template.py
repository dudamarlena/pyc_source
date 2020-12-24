# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\invoice_template.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 8639 bytes
"""
This module abstracts templates for invoice providers.

Templates are initially read from .yml files and then kept as class.
"""
import re, dateparser
from unidecode import unidecode
import logging
from collections import OrderedDict
from .plugins import lines, tables
logger = logging.getLogger(__name__)
OPTIONS_DEFAULT = {'remove_whitespace':False, 
 'remove_accents':False, 
 'lowercase':False, 
 'currency':'EUR', 
 'date_formats':[],  'languages':[],  'decimal_separator':'.', 
 'replace':[]}
PLUGIN_MAPPING = {'lines':lines, 
 'tables':tables}

class InvoiceTemplate(OrderedDict):
    __doc__ = '\n    Represents single template files that live as .yml files on the disk.\n\n    Methods\n    -------\n    prepare_input(extracted_str)\n        Input raw string and do transformations, as set in template file.\n    matches_input(optimized_str)\n        See if string matches keywords set in template file\n    parse_number(value)\n        Parse number, remove decimal separator and add other options\n    parse_date(value)\n        Parses date and returns date after parsing\n    coerce_type(value, target_type)\n        change type of values\n    extract(optimized_str)\n        Given a template file and a string, extract matching data fields.\n    '

    def __init__(self, *args, **kwargs):
        (super(InvoiceTemplate, self).__init__)(*args, **kwargs)
        self.options = OPTIONS_DEFAULT.copy()
        for lang in self.options['languages']:
            assert len(lang) == 2, 'lang code must have 2 letters'

        if 'options' in self:
            self.options.update(self['options'])
        if 'issuer' not in self.keys():
            self['issuer'] = self['keywords'][0]

    def prepare_input(self, extracted_str):
        """
        Input raw string and do transformations, as set in template file.
        """
        if self.options['remove_whitespace']:
            optimized_str = re.sub(' +', '', extracted_str)
        else:
            optimized_str = extracted_str
        if self.options['remove_accents']:
            optimized_str = unidecode(optimized_str)
        if self.options['lowercase']:
            optimized_str = optimized_str.lower()
        for replace in self.options['replace']:
            assert len(replace) == 2, 'A replace should be a list of 2 items'
            optimized_str = optimized_str.replace(replace[0], replace[1])

        return optimized_str

    def matches_input(self, optimized_str):
        """See if string matches keywords set in template file"""
        if all([keyword in optimized_str for keyword in self['keywords']]):
            logger.debug('Matched template %s', self['template_name'])
            return True

    def parse_number(self, value):
        assert value.count(self.options['decimal_separator']) < 2, 'Decimal separator cannot be present several times'
        amount_pipe = value.replace(self.options['decimal_separator'], '|')
        amount_pipe_no_thousand_sep = re.sub('[.,\\s]', '', amount_pipe)
        return float(amount_pipe_no_thousand_sep.replace('|', '.'))

    def parse_date(self, value):
        """Parses date and returns date after parsing"""
        res = dateparser.parse(value,
          date_formats=(self.options['date_formats']),
          languages=(self.options['languages']))
        logger.debug('result of date parsing=%s', res)
        return res

    def coerce_type(self, value, target_type):
        if target_type == 'int':
            if not value.strip():
                return 0
            return int(self.parse_number(value))
        if target_type == 'float':
            if not value.strip():
                return 0.0
            return float(self.parse_number(value))
        if target_type == 'date':
            return self.parse_date(value)
        assert False, 'Unknown type'

    def extract(self, optimized_str):
        """
        Given a template file and a string, extract matching data fields.
        """
        logger.debug('START optimized_str ========================')
        logger.debug(optimized_str)
        logger.debug('END optimized_str ==========================')
        logger.debug('Date parsing: languages=%s date_formats=%s', self.options['languages'], self.options['date_formats'])
        logger.debug('Float parsing: decimal separator=%s', self.options['decimal_separator'])
        logger.debug('keywords=%s', self['keywords'])
        logger.debug(self.options)
        output = {}
        output['issuer'] = self['issuer']
        for k, v in self['fields'].items():
            if k.startswith('static_'):
                logger.debug('field=%s | static value=%s', k, v)
                output[k.replace('static_', '')] = v
            else:
                logger.debug('field=%s | regexp=%s', k, v)
                sum_field = False
                if k.startswith('sum_amount'):
                    if type(v) is list:
                        k = k[4:]
                        sum_field = True
                    else:
                        if type(v) is list:
                            res_find = []
                            for v_option in v:
                                res_val = re.findall(v_option, optimized_str)
                                if res_val:
                                    if sum_field:
                                        res_find += res_val
                                    else:
                                        res_find.extend(res_val)

                        else:
                            res_find = re.findall(v, optimized_str)
                        if res_find:
                            logger.debug('res_find=%s', res_find)
                            if k.startswith('date') or k.endswith('date'):
                                output[k] = self.parse_date(res_find[0])
                                output[k] or logger.error("Date parsing failed on date '%s'", res_find[0])
                                return
                            else:
                                if k.startswith('amount'):
                                    if sum_field:
                                        output[k] = 0
                                        for amount_to_parse in res_find:
                                            output[k] += self.parse_number(amount_to_parse)

                                else:
                                    output[k] = self.parse_number(res_find[0])
                        else:
                            res_find = list(set(res_find))
                            if len(res_find) == 1:
                                output[k] = res_find[0]
                            else:
                                output[k] = res_find
                else:
                    logger.warning("regexp for field %s didn't match", k)

        output['currency'] = self.options['currency']
        for plugin_keyword, plugin_func in PLUGIN_MAPPING.items():
            if plugin_keyword in self.keys():
                plugin_func.extract(self, optimized_str, output)

        if 'required_fields' not in self.keys():
            required_fields = [
             'date', 'amount', 'invoice_number', 'issuer']
        else:
            required_fields = []
            for v in self['required_fields']:
                required_fields.append(v)

        if set(required_fields).issubset(output.keys()):
            output['desc'] = 'Invoice from %s' % self['issuer']
            logger.debug(output)
            return output
        fields = list(set(output.keys()))
        logger.error('Unable to match all required fields. The required fields are: {0}. Output contains the following fields: {1}.'.format(required_fields, fields))
        return