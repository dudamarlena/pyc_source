# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\io_modues\io_module.py
# Compiled at: 2019-01-22 06:04:52
# Size of source mod 2**32: 378 bytes
import io, json, models.settings.config as config, logging

def export_json_to_file(data):
    try:
        with open(config.export_json_file_full_path, 'w') as (f):
            json.dump(data, f, ensure_ascii=False)
        logging.info('Data successfully exported')
    except Exception as e:
        logging.error('Error. ' + str(e))