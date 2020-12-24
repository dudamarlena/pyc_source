# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matthew/Documents/rets/env/lib/python3.8/site-packages/rets/utils/search.py
# Compiled at: 2020-03-03 14:04:26
# Size of source mod 2**32: 7982 bytes
import collections, datetime, logging
from six import string_types
logger = logging.getLogger('rets')

class DMQLHelper(object):
    __doc__ = 'Ensures Data Mining Query Language is Valid'

    @staticmethod
    def dmql(query):
        """Client supplied raw DMQL, ensure quote wrap."""
        if isinstance(query, dict):
            raise ValueError('You supplied a dictionary to the dmql_query parameter, but a string is required. Did you mean to pass this to the search_filter parameter? ')
        if len(query) > 0:
            if query != '*':
                if query[0] != '(':
                    if query[(-1)] != ')':
                        query = '({})'.format(query)
        return query

    @staticmethod
    def filter_to_dmql(filter_dict):
        """Converts the filter dictionary into DMQL"""
        if not isinstance(filter_dict, (dict, collections.OrderedDict)):
            raise TypeError('Expected a dictionary type buy got {} instead.'.format(type(filter_dict)))

        def is_date_time_type(val):
            """Returns True if the value is a datetime"""
            return isinstance(val, (datetime.datetime, datetime.date, datetime.time))

        def evaluate_datetime(val):
            """Converts the datetime object into the RETS expected format"""
            date_format = '%Y-%m-%d'
            time_format = '%H:%M:%S'
            datetime_format = '{}T{}'.format(date_format, time_format)
            if isinstance(val, datetime.datetime):
                evaluated = val.strftime(datetime_format)
            else:
                if isinstance(val, datetime.date):
                    evaluated = val.strftime(date_format)
                else:
                    if isinstance(val, datetime.time):
                        evaluated = val.strftime(time_format)
                    else:
                        evaluated = val
            return evaluated

        def evaluate_operators(key_dict):
            allowed_operators = [
             '$gte',
             '$lte',
             '$contains',
             '$begins',
             '$ends',
             '$in',
             '$nin',
             '$neq']
            if not all((op in allowed_operators for op in key_dict.keys())):
                raise ValueError('You have supplied an invalid operator. Please provide one of the following {}'.format(allowed_operators))
            else:
                keys = key_dict.keys()
                string = ''
                if len(keys) == 2:
                    if all((k in ('$gte', '$lte') for k in keys)):
                        if all((is_date_time_type(key_dict[v]) for v in keys)):
                            string = '{}-{}'.format(evaluate_datetime(key_dict['$gte']), evaluate_datetime(key_dict['$lte']))
                    else:
                        try:
                            float(key_dict['$gte'])
                            float(key_dict['$lte'])
                        except ValueError:
                            raise ValueError('$gte and $lte expect numeric or datetime values')
                        else:
                            string = '{:.2f}-{:.2f}'.format(key_dict['$gte'], key_dict['$lte'])
                else:
                    if len(keys) == 1:
                        if '$gte' in key_dict:
                            if is_date_time_type(key_dict['$gte']):
                                string = '{}+'.format(evaluate_datetime(key_dict['$gte']))
                            else:
                                try:
                                    float(key_dict['$gte'])
                                except ValueError:
                                    raise ValueError('$gte expects a numeric value or a datetime object')
                                else:
                                    string = '{:.2f}+'.format(key_dict['$gte'])
                        elif '$lte' in key_dict:
                            if is_date_time_type(key_dict['$lte']):
                                string = '{}-'.format(evaluate_datetime(key_dict['$lte']))
                            else:
                                try:
                                    float(key_dict['$lte'])
                                except ValueError:
                                    raise ValueError('$lte expects a numeric value or a datetime object')
                                else:
                                    string = '{:.2f}-'.format(key_dict['$lte'])
                        elif '$in' in key_dict:
                            if not isinstance(key_dict['$in'], list):
                                raise ValueError('$in expects a list of strings')
                            key_dict['$in'] = [evaluate_datetime(v) for v in key_dict['$in']]
                            if not all((isinstance(v, string_types) for v in key_dict['$in'])):
                                raise ValueError('$in expects a list of strings')
                            options = ','.join(key_dict['$in'])
                            string = '{}'.format(options)
                        elif '$nin' in key_dict:
                            if not isinstance(key_dict['$nin'], list):
                                raise ValueError('$nin expects a list of strings')
                            key_dict['$nin'] = [evaluate_datetime(v) for v in key_dict['$nin']]
                            if not all((isinstance(v, string_types) for v in key_dict['$nin'])):
                                raise ValueError('$nin expects a list of strings')
                            options = ','.join(key_dict['$nin'])
                            string = '~{}'.format(options)
                        else:
                            if '$contains' in key_dict:
                                if not isinstance(key_dict['$contains'], string_types):
                                    raise ValueError('$contains expects a string.')
                                string = '*{}*'.format(key_dict['$contains'])
                            else:
                                if '$begins' in key_dict:
                                    if not isinstance(key_dict['$begins'], string_types):
                                        raise ValueError('$begins expects a string.')
                                    string = '{}*'.format(key_dict['$begins'])
                                else:
                                    if '$ends' in key_dict:
                                        if not isinstance(key_dict['$ends'], string_types):
                                            raise ValueError('$ends expects a string.')
                                        string = '*{}'.format(key_dict['$ends'])
                                    else:
                                        if '$neq' in key_dict:
                                            string = '~{}'.format(key_dict['$neq'])
                    else:
                        raise ValueError('Please supply $gte and $lte for getting values between numbers or 1 of {}'.format(allowed_operators))
            return string

        dmql_search_filters = []
        for filt, value in filter_dict.items():
            dmql_string = '({}='.format(filt)
            if isinstance(value, dict):
                dmql_string += evaluate_operators(key_dict=value)
            else:
                dmql_string += '{}'.format(evaluate_datetime(value))
            dmql_string += ')'
            dmql_search_filters.append(dmql_string)
        else:
            search_string = ','.join(dmql_search_filters)
            logger.debug('Filter returned the following DMQL: {}'.format(search_string))
            return search_string