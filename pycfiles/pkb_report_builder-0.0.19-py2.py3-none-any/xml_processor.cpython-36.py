# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\xml_parser\xml_processor.py
# Compiled at: 2019-01-30 09:27:36
# Size of source mod 2**32: 5606 bytes
import logging, modules.xml_parser.xml_table_processor as xml_table_processor, models.tree_models.xml_navigator as navigator, models.export_models.export_styles as export_styles

def recursive_navigate(node, paths, index):
    try:
        r = node
        for result in node.findall(paths[index]):
            if index < len(paths) - 1:
                return recursive_navigate(result, paths, index + 1)
            else:
                return result

        return
    except Exception as e:
        logging.error('Error. ' + str(e))


def process_cell(root, cell):
    try:
        cell_value = ''
        index = 0
        for path in cell.paths:
            node = recursive_navigate(root, path, 0)
            if node == None:
                return
            value = node.get(cell.value_attribute)
            cell_value += value
            if index < len(cell.paths) - 1:
                cell_value += '\n'
            index += 1

        cell.set_cell_value(cell_value)
        return cell
    except Exception as e:
        logging.error('Error. ' + str(e))
        return


def process_row(root, export_element):
    try:
        for cell in export_element.row.cells:
            res = process_cell(root, cell)
            if res == None:
                export_element.include_in_report = False

    except Exception as e:
        logging.error('Error. ' + str(e))


def check_field(element, name):
    try:
        v = getattr(element, name)
        return v
    except Exception as e:
        return


def add_element_to_document(document, style, values):
    try:
        t = 0
        navigate_params = navigator.XmlNavigator('', '', '', style)
        document.add_export_element([0, '', navigate_params])
        last_element = document.export_elements[(len(document.export_elements) - 1)]
        last_element.row.set_row_style(style.bgc, style.color, style.ta, style.fz, style.fm, style.fw, style.fs, style.u, style.ff)
        str_values = []
        for value in values:
            is_str = type(value) is str
            element_value = ''
            if is_str == False:
                element_value = check_field(value, 'title')
                if element_value == None:
                    element_value = check_field(value, 'value')
            else:
                element_value = str(value)
            str_values.append(element_value)

        last_element.row.init_value_cells(navigate_params, str_values)
        last_element.row.set_row_cells_style()
        t = 0
    except Exception as e:
        pass


def check_clean_row(row):
    try:
        for cell in row.cells:
            if cell.value != '':
                return False

        return True
    except Exception as e:
        logging.error('Error. ' + str(e))
        return True


def clean_empty_rows(document):
    try:
        clean_export_elements = []
        for export_element in document.export_elements:
            if check_clean_row(export_element.row) == False:
                clean_export_elements.append(export_element)

        document.export_elements = []
        document.export_elements = clean_export_elements
        t = 0
    except Exception as e:
        logging.error('Error. ' + str(e))


def generate_group_rows(document, table):
    try:
        elements_count = len(document.export_elements)
        for group_row in table.group_rows:
            n_group = [group_row[0] + elements_count + 1, group_row[1] + elements_count + 1]
            document.group_rows.append(n_group)

    except Exception as e:
        logging.error('Error. ' + str(e))


def process_table(document):
    try:
        clean_empty_rows(document)
        add_element_to_document(document, export_styles.row_title_style, [''])
        for table in document.xml_document_tables:
            add_element_to_document(document, export_styles.row_title_style, [table.title])
            generate_group_rows(document, table)
            add_element_to_document(document, export_styles.table_header_style, table.columns)
            for row in table.rows:
                if row.not_classificated == True:
                    add_element_to_document(document, export_styles.table_not_classificated_rows, row.cells)
                else:
                    if row.is_root == False:
                        add_element_to_document(document, export_styles.table_rows_content_style, row.cells)
                    else:
                        add_element_to_document(document, export_styles.table_rows_root_content_style, row.cells)

            add_element_to_document(document, export_styles.row_title_style, [''])

    except Exception as e:
        logging.error('Error. ' + str(e))


def process_document(root, document):
    try:
        for export_element in document.export_elements:
            type_id = export_element.type.value
            if type_id == 0:
                process_row(root, export_element)
            elif type_id == 1:
                pass

        xml_table_processor.process_table(root, document)
        process_table(document)
    except Exception as e:
        logging.error('Error. ' + str(e))