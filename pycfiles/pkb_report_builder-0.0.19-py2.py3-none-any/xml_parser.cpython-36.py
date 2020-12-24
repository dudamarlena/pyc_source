# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\xml_parser\xml_parser.py
# Compiled at: 2019-02-04 06:49:13
# Size of source mod 2**32: 1281 bytes
import xml.etree.ElementTree as ET, models.export_models.export_document as export_document, modules.xml_parser.xml_processor as xml_processor, modules.document_converters.document_converter as document_converter, logging, modules.io_modues.io_module as io_module, modules.table_processing.init_document_tables as init_document_tables, modules.root_processor.root_processor as root_processor

def parse_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        document = export_document.ExportDocument()
        document.xml_document_tables = init_document_tables.init_document_tables(root)
        document.init_document_elements()
        xml_processor.process_document(root, document)
        result = document_converter.convert_document_to_sheet_format(document)
        logging.info('File parse  successfully completed')
        io_module.export_json_to_file(result)
        return result
    except Exception as e:
        logging.error('Error. ' + str(e))


def parse_data_string(data):
    try:
        root = ET.fromstring(data)
    except Exception as e:
        logging.error('Error. ' + str(e))