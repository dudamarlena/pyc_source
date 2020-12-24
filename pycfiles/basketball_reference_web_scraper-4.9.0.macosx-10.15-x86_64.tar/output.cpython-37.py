# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/basketball_reference_web_scraper/output.py
# Compiled at: 2020-01-10 17:57:04
# Size of source mod 2**32: 1181 bytes
from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.json_encoders import BasketballReferenceJSONEncoder
from basketball_reference_web_scraper.writers import JSONWriter, WriteOptions

def output(values, output_type, output_file_path, csv_writer, output_write_option=None, json_options=None):
    if output_type is None:
        return values
    write_option = OutputWriteOption.WRITE if output_write_option is None else output_write_option
    if output_type == OutputType.JSON:
        options = WriteOptions(file_path=output_file_path, mode=write_option, custom_options=json_options)
        writer = JSONWriter(encoder=BasketballReferenceJSONEncoder)
        return writer.write(data=values, options=options)
    if output_type == OutputType.CSV:
        options = WriteOptions(file_path=output_file_path, mode=write_option)
        if options.should_write_to_file():
            return csv_writer.write(data=values, options=options)
        raise ValueError('CSV output must contain a file path')
    raise ValueError('Unknown output type: {output_type}'.format(output_type=output_type))