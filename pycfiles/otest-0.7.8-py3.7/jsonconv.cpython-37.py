# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/jsonconv.py
# Compiled at: 2016-11-27 03:39:22
# Size of source mod 2**32: 5794 bytes
"""
JSON 2 HTML convertor
=====================

(c) Varun Malhotra 2013
Source Code: https://github.com/softvar/json2html

Rewritten to work with Python3

Contributors:
-------------
1. Michel Müller(@muellermichel), https://github.com/softvar/json2html/pull/2
2. Roland Hedberg

LICENSE: MIT
--------
"""
from past.builtins.misc import unicode
import json

class Json2Html(object):

    def __init__(self):
        self.root_table_attributes = ''
        self.table_attributes = ''

    def convert(self, json_input='', **kwargs):
        """
            Convert JSON to HTML Table format
        """
        if 'root_table_attributes' in kwargs:
            self.root_table_attributes = kwargs['root_table_attributes']
        else:
            self.root_table_attributes = 'border="1"'
        if 'table_attributes' in kwargs:
            self.table_attributes = kwargs['table_attributes']
        else:
            self.table_attributes = ''
        if json_input:
            try:
                json.loads(json_input)
            except:
                json_input = json.dumps(json_input)

        else:
            raise Exception("Can't convert NULL!")
        input = json.loads(json_input)
        return self.iter_json(input, root=True)

    @staticmethod
    def column_headers_from_list_of_dicts(input):
        """
            If suppose some key has array of objects and all the keys are same,
            instead of creating a new row for each such entry,
            club such values, thus it makes more sense and more readable table.

            @example:
                jsonObject = {
                    "sampleData": [
                        {"a":1, "b":2, "c":3},
                        {"a":5, "b":6, "c":7}
                    ]
                }
                OUTPUT:
                _____________________________
                |               |   |   |   |
                |               | a | c | b |
                |   sampleData  |---|---|---|
                |               | 1 | 3 | 2 |
                |               | 5 | 7 | 6 |
                -----------------------------

            @contributed by: @muellermichel
        """
        if len(input) < 2:
            return
        else:
            return isinstance(input[0], dict) or None
        column_headers = input[0].keys()
        for entry in input:
            if not isinstance(entry, dict):
                return
                if len(list(entry.keys())) != len(column_headers):
                    return
                for header in column_headers:
                    if header not in entry:
                        return

        return column_headers

    def iter_json(self, input, root=False):
        """
            Iterate over the JSON and process it
            to generate the super awesome HTML Table format
        """

        def markup(entry):
            if isinstance(entry, unicode):
                return unicode(entry)
            else:
                if isinstance(entry, int) or isinstance(entry, float):
                    return str(entry)
                if isinstance(entry, list) and len(entry) == 0:
                    return ''
            if isinstance(entry, list):
                listMarkup = ''
                listMarkup += '<ul><li>'
                listMarkup += '</li><li>'.join([markup(child) for child in entry])
                listMarkup += '</li></ul>'
                return listMarkup
            if isinstance(entry, dict):
                return self.iter_json(entry)
            return ''

        converted_output = ''
        if root:
            table_init_markup = '<table {}>'.format(self.root_table_attributes)
        else:
            table_init_markup = '<table {}>'.format(self.table_attributes)
        converted_output += table_init_markup
        try:
            for k, v in input.items():
                converted_output += '<tr>'
                converted_output = converted_output + '<th>' + markup(k) + '</th>'
                if v is None:
                    v = unicode('')
                if isinstance(v, list):
                    column_headers = self.column_headers_from_list_of_dicts(v)
                    if column_headers is not None:
                        converted_output += '<td>'
                        converted_output += table_init_markup
                        converted_output += '<tr><td>' + '</td><td>'.join(column_headers) + '</td></tr>'
                        for list_entry in v:
                            converted_output = converted_output
                            converted_output += '<tr><td>'
                            converted_output += '</td><td>'.join([markup(list_entry[column_header]) for column_header in column_headers])
                            converted_output += '</td></tr>'

                        converted_output += '</table></td></tr>'
                        continue
                converted_output = converted_output + '<td>' + markup(v) + '</td>'
                converted_output += '</tr>'

            converted_output += '</table>'
        except:
            raise Exception('Not a valid JSON list')

        return converted_output


json2html = Json2Html()