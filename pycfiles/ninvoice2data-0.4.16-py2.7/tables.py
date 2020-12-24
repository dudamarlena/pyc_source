# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/extract/plugins/tables.py
# Compiled at: 2019-02-01 05:18:39
"""
Plugin to extract tables from an invoice.
"""
import re, logging as logger
DEFAULT_OPTIONS = {'field_separator': '\\s+', 'line_separator': '\\n'}

def extract(self, content, output):
    """Try to extract tables from an invoice"""
    for table in self['tables']:
        plugin_settings = DEFAULT_OPTIONS.copy()
        plugin_settings.update(table)
        table = plugin_settings
        assert 'start' in table, 'Table start regex missing'
        assert 'end' in table, 'Table end regex missing'
        assert 'body' in table, 'Table body regex missing'
        start = re.search(table['start'], content)
        end = re.search(table['end'], content)
        if not start or not end:
            logger.warning('no table body found - start %s, end %s', start, end)
            continue
        table_body = content[start.end():end.start()]
        for line in re.split(table['line_separator'], table_body):
            if not line.strip('').strip('\n') or not line:
                continue
            match = re.search(table['body'], line)
            if match:
                for field, value in match.groupdict().items():
                    if field in output:
                        continue
                    if field.startswith('date') or field.endswith('date'):
                        output[field] = self.parse_date(value)
                        if not output[field]:
                            logger.error("Date parsing failed on date '%s'", value)
                            return
                    elif field.startswith('amount'):
                        output[field] = self.parse_number(value)
                    else:
                        output[field] = value

            logger.debug("ignoring *%s* because it doesn't match anything", line)

    return