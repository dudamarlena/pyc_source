# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\tables.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 2098 bytes
"""
Plugin to extract tables from an invoice.
"""
import re, logging
logger = logging.getLogger(__name__)
DEFAULT_OPTIONS = {'field_separator':'\\s+', 
 'line_separator':'\\n'}

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
        if not (start and end):
            logger.warning('no table body found - start %s, end %s', start, end)
            continue
        table_body = content[start.end():end.start()]
        for line in re.split(table['line_separator'], table_body):
            if line.strip('').strip('\n'):
                if not line:
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
                            else:
                                if field.startswith('amount'):
                                    output[field] = self.parse_number(value)
                        else:
                            output[field] = value

                logger.debug("ignoring *%s* because it doesn't match anything", line)