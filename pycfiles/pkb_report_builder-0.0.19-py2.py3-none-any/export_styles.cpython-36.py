# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\export_models\export_styles.py
# Compiled at: 2019-01-30 09:38:01
# Size of source mod 2**32: 1130 bytes
from models.export_models.export_document_elements import ExportElementStyle
import logging
row_title_style = None
row_value_style = None
table_header_style = None
table_rows_content_style = None
table_rows_root_content_style = None
table_not_classificated_rows = None

def init_styles():
    global row_title_style
    global row_value_style
    global table_header_style
    global table_not_classificated_rows
    global table_rows_content_style
    global table_rows_root_content_style
    try:
        row_title_style = ExportElementStyle(fw='bold')
        row_value_style = ExportElementStyle()
        table_header_style = ExportElementStyle(fw='bold', bgc='#e6e6ff')
        table_rows_content_style = ExportElementStyle()
        table_rows_root_content_style = ExportElementStyle(fw='bold', bgc='#e6f7ff')
        table_not_classificated_rows = ExportElementStyle(fw='bold', bgc='#ffb3b3', fs='italic')
        logging.info('Styles init successful')
    except Exception as e:
        logging.error('Error initialization. ' + str(e))