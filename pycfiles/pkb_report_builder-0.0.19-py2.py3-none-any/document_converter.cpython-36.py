# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\document_converters\document_converter.py
# Compiled at: 2019-01-28 08:13:39
# Size of source mod 2**32: 5941 bytes
import logging, models.export_models.export_document_report_model as export_document_report_model, json

def set_zero_row(document, sheet_id, widths):
    try:
        id = 1
        for width in widths:
            json = export_document_report_model.ExportDocumentReportCellContent('', width=width, height=45)
            cell = export_document_report_model.ExportDocumentReportCell(sheet_id, 0, id, json)
            document.cells.append(cell)
            id += 1

    except Exception as e:
        logging.error('Error. ' + str(e))


def set_zero_column(document):
    try:
        json = export_document_report_model.ExportDocumentReportCellContent('', height=45)
        cell = export_document_report_model.ExportDocumentReportCell(1, 0, 0, json)
        document.cells.append(cell)
    except Exception as e:
        logging.error('Error. ' + str(e))


def get_max_width(export_document):
    try:
        columns = []
        rows = []
        for element in export_document.export_elements:
            if element.type.value == 0:
                rows.append(element.row)
            else:
                rows.append(element.table.header_row)
                for r in element.table.rows:
                    rows.append(r)

        for r in rows:
            id = 0
            for c in r.cells:
                l = len(str(c.value))
                if l > 0:
                    if len(columns) < id + 1:
                        columns.append(l)
                    elif columns[id] < l:
                        columns[id] = l
                id += 1

        widths = []
        for c in columns:
            w = c * 6
            if w > 240:
                w = 240
            widths.append(w)

        return widths
    except Exception as e:
        logging.error('Error. ' + str(e))


def init_row(document, row, row_index, show_grid):
    try:
        id = 1
        for cell in row.cells:
            style = cell.style
            back_color = style.bgc
            font_color = style.color
            font_family = style.ff
            font_style = style.fs
            font_size = style.fz
            text_align = style.ta
            font_weight = style.fw
            if font_style == 'bold':
                font_weight = 'bold'
                font_style = 'normal'
            if font_style == 'bolditalic':
                font_weight = 'bold'
                font_style = 'italic'
            if font_style == 'italic':
                font_weight = 'normal'
                font_style = 'italic'
            fm = ''
            cell_content = export_document_report_model.ExportDocumentReportCellContent(data=(cell.value),
              bgc=back_color,
              color=font_color,
              ta=text_align,
              fz=font_size,
              ff=font_family,
              fw=font_weight,
              fs=font_style,
              show_grid=show_grid,
              fm=fm,
              contains_data=True)
            report_cell = export_document_report_model.ExportDocumentReportCell(1, row_index, id, cell_content)
            document.cells.append(report_cell)
            id += 1

    except Exception as e:
        logging.error('Error. ' + str(e))


def init_rows(export_document, document):
    try:
        rows = []
        for element in export_document.export_elements:
            if element.type.value == 0:
                rows.append(element.row)
            else:
                rows.append(element.table.header_row)
                for r in element.table.rows:
                    rows.append(r)

        row_index = 1
        for row in rows:
            show_grid = True
            init_row(document, row, row_index, show_grid)
            row_index += 1

    except Exception as e:
        logging.error('Error. ' + str(e))


def init_document_cells(export_document, document):
    try:
        width_columns = get_max_width(export_document)
        set_zero_row(document, 1, width_columns)
        set_zero_column(document)
        init_rows(export_document, document)
    except Exception as e:
        logging.error('Error. ' + str(e))


def convert_document_to_sheet_format(export_document):
    try:
        document_report_model = export_document_report_model.ExportDocumentReportModel('Отчет ПКБ')
        id = 1
        sheets = ['Детализация отчета ПКБ']
        for sheet in sheets:
            document_report_model.add_sheet(id, sheet)
            id += 1

        document_groups = []
        for group_row in export_document.group_rows:
            document_groups.append(export_document_report_model.ExportDocumentGroup(1, group_row))

        json_string = json.dumps([ob.__dict__ for ob in document_groups])
        json_string = json_string.replace('"', '')
        fl = export_document_report_model.ExportDocumentReportFloatings(1, 'rowGroups', 'rowgroup', json_string)
        document_report_model.floatings.append(fl)
        init_document_cells(export_document, document_report_model)
        return document_report_model.toJSON()
    except Exception as e:
        logging.error('Error. ' + str(e))