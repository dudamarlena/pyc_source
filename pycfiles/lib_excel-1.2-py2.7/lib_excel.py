# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib_excel.py
# Compiled at: 2018-05-09 09:49:12
import os, lib_common, lib_excel_package, lib_logger
logger = lib_logger.logger()

class excel:

    def __init__(self, pathname, auto_save=True, must_exist=False, test=False):
        if test:
            return
        self.ws_list = []
        self.auto_save = auto_save
        while True:
            if os.path.isfile(pathname):
                self._openFile(pathname)
                break
            elif must_exist:
                lib_common.assert_file_exist(pathname)
            else:
                self._createFile(pathname)
                break

    def _createFile(self, pathname, ws_tab_list=None):
        self.wb_pathname = pathname
        self.wb = lib_excel_package.create_workbook()
        ws = lib_excel_package.get_active_worksheet(self.wb)
        if ws_tab_list != None:
            lib_excel_package.set_new_worksheet_name(self.wb, ws, ws_tab_list[0])
        if len(ws_tab_list) > 1:
            for n in range(1, len(ws_tab_list)):
                self.addWorksheet(ws_tab_list[n])

        folder = os.path.dirname(pathname)
        if not os.path.exists(folder):
            os.makedirs(folder)
        lib_excel_package.save_workbook(self.wb, pathname)
        return

    def _openFile(self, pathname):
        logger.log('debug', 'Opening Workbook = %s' % pathname)
        self.wb = lib_excel_package.open_workbook(pathname)
        self.wb_pathname = pathname
        logger.log('debug', 'worksheet names = %s' % str(lib_excel_package.get_sheet_name_list(self.wb)))

    def get_tab_list(self, wb=None):
        if wb == None:
            wb = self.wb
        all_tabs = lib_excel_package.get_sheet_name_list(wb)
        return all_tabs

    def required_tabs(self, tab_list):
        issue_list = []
        all_tabs = lib_excel_package.get_sheet_name_list(self.wb)
        for tab in tab_list:
            if tab not in all_tabs:
                issue_list.append(tab)

        return issue_list

    def addWorksheet(self, ws_title=''):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            return lib_excel_package.get_worksheet(self.wb, ws_title)
        ws = lib_excel_package.create_worksheet(self.wb, ws_title)
        if self.auto_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return ws

    def changeWorksheetName(self, ws_new_title, ws_old_title):
        if ws_new_title == ws_old_title:
            return True
        if ws_old_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_old_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_old_title)
            return False
        if ws_new_title in lib_excel_package.get_sheet_name_list(self.wb):
            return True
        lib_excel_package.set_new_worksheet_name(self.wb, ws, ws_new_title)
        if self.auto_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return True

    def writeCell(self, ws_title, col, row, cellValue, force_save=False, save=False):
        names = lib_excel_package.get_sheet_name_list(self.wb)
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        colx = col
        if not str(col).isdigit():
            colx = lib_excel_package.column_letter_to_number(col)
        lib_excel_package.set_cell_value(self.wb, ws, row=row, column=colx, value=cellValue)
        if save and self.auto_save or force_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return True

    def writeCellBlock(self, ws_title, cell_value_list_of_lists, topleft, row_col='row', save=False):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        col_start, row_start = self.get_cell_coordinate(topleft, 'number')
        if row_col == 'row':
            primary_dim = len(cell_value_list_of_lists)
            primary_start = row_start
            secondary_start = col_start
        else:
            primary_dim = len(cell_value_list_of_lists)
            primary_start = col_start
            secondary_start = row_start
        max_primary_len = primary_dim
        max_secondary_len = 0
        for primary_index in range(0, primary_dim):
            line_list = cell_value_list_of_lists[primary_index]
            if max_secondary_len < len(line_list):
                max_secondary_len = len(line_list)
            for secondary_index in range(0, len(line_list)):
                if row_col == 'row':
                    row = primary_start + primary_index
                    col = secondary_start + secondary_index
                else:
                    col = primary_start + primary_index
                    row = secondary_start + secondary_index
                value = line_list[secondary_index]
                lib_excel_package.set_cell_value(self.wb, ws, row=row, column=col, value=line_list[secondary_index])
                logger.log('debug', 'Writing Cell[%s%s]=%s' % (col, row, value))

        if row_col == 'row':
            max_row = primary_start + max_primary_len - 1
            max_col = lib_excel_package.column_number_to_letter(secondary_start + max_secondary_len - 1)
        else:
            max_col = lib_excel_package.column_number_to_letter(primary_start + max_primary_len - 1)
            max_row = secondary_start + max_secondary_len - 1
        botright = max_col + str(max_row)
        cell_area = topleft + ':' + botright
        if save and self.auto_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return cell_area

    def formatWorksheet(self, ws_title, cell_area='', save=False):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist %s' % (ws_title, lib_excel_package.get_sheet_name_list(self.wb)))
            return False
        if cell_area == '':
            maxCell = lib_excel_package.column_number_to_letter(lib_excel_package.get_max_column_on_worksheet(self.wb, ws)) + str(lib_excel_package.get_max_row_on_worksheet(self.wb, ws))
            cell_area = 'A1:' + maxCell
            logger.log('debug', 'cell_range = %s' % cell_area)
        if ':' not in cell_area:
            logger.log('error', 'Invalid cell area format: [%s]' % cell_area)
            return False
        cell_format = lib_excel_package.cell_formatting(operator='equal', formula=['"DN"'], color_fill='RED', color_font='WHITE', bold=True)
        lib_excel_package.cell_area_conditional_formatting(self.wb, ws, cell_area, cell_format)
        cell_format = lib_excel_package.cell_formatting(operator='equal', formula=['"UP"'], color_fill='GREEN')
        lib_excel_package.cell_area_conditional_formatting(self.wb, ws, cell_area, cell_format)
        cell_format = lib_excel_package.cell_formatting(operator='equal', formula=['"adminDN"'], color_fill='DARKYELLOW', color_font='WHITE', bold=True)
        lib_excel_package.cell_area_conditional_formatting(self.wb, ws, cell_area, cell_format)
        cell_format = lib_excel_package.cell_formatting(operator='equal', formula=['"ISSUE"'], color_fill='YELLOW', bold=True)
        lib_excel_package.cell_area_conditional_formatting(self.wb, ws, cell_area, cell_format)
        topleft = cell_area.split(':')[0]
        botright = cell_area.split(':')[1]
        sides = {'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'}
        edges = {'left': 'thick', 'right': 'thick', 'top': 'thick', 'bottom': 'thin'}
        self.draw_border(ws_title, topleft, botright, sides=sides, edges=edges)
        if save and self.auto_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return True

    def draw_border(self, ws_title, topleft, botright, sides={'left': 'thin', 'right': 'thin', 'top': 'thin', 'bottom': 'thin'}, edges={'left': 'thick', 'right': 'thick', 'top': 'thick', 'bottom': 'thick'}, save=False):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist %s' % (ws_title, lib_excel_package.get_sheet_name_list(self.wb)))
            return False
        col_start, row_start = self.get_cell_coordinate(topleft, 'number')
        col_dim, row_dim = self.get_block_dimension(ws_title, topleft, botright)
        lib_excel_package.set_border(ws, col_start, row_start, col_dim, row_dim, sides, edges)
        if save and self.auto_save:
            lib_excel_package.save_workbook(self.wb, self.wb_pathname)
        return True

    def cell_area_dimension(self, topleft, bottomright):
        columns = 0
        rows = 0
        return (columns, rows)

    def get_max_row_on_worksheet(self, ws_title):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist %s' % (ws_title, lib_excel_package.get_sheet_name_list(self.wb)))
            return False
        max_row = lib_excel_package.get_max_row_on_worksheet(self.wb, ws)
        return max_row

    def get_max_column_on_worksheet(self, ws_title, type):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist %s', lib_common.stack_frame(10) % (ws_title, lib_excel_package.get_sheet_name_list(self.wb)))
            return False
        max_col = lib_excel_package.get_max_column_on_worksheet(self.wb, ws)
        if type == 'letter':
            max_col = lib_excel_package.column_number_to_letter(max_col)
        return max_col

    def readCell(self, ws_title, col, row):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        colx = col
        if not str(col).isdigit():
            colx = lib_excel_package.column_letter_to_number(col)
        cellValue = lib_excel_package.get_cell_value(self.wb, ws, row=row, column=colx)
        return cellValue

    def readCellBlock(self, ws_title, topleft, bottomright, row_col='row', wb=None):
        if wb == None:
            wb = self.wb
        if ws_title in lib_excel_package.get_sheet_name_list(wb):
            ws = lib_excel_package.get_worksheet(wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        col_dim, row_dim = self.get_block_dimension(ws_title, topleft, bottomright, wb=wb)
        col_start, row_start = self.get_cell_coordinate(topleft, 'number')
        if row_col == 'row':
            primary_start = row_start
            primary_end = row_start + row_dim - 1
            secondary_start = col_start
            secondary_end = col_start + col_dim - 1
        else:
            primary_start = col_start
            primary_end = col_start + col_dim - 1
            secondary_start = row_start
            secondary_end = row_start + row_dim - 1
        cell_list_of_lists = []
        for primary_index in range(primary_start, primary_end + 1):
            cell_list = []
            for secondary_index in range(secondary_start, secondary_end + 1):
                if row_col == 'row':
                    row = primary_index
                    col = secondary_index
                else:
                    col = primary_index
                    row = secondary_index
                cellValue = lib_excel_package.get_cell_value(wb, ws, row=row, column=col)
                cell_list.append(cellValue)
                logger.log('debug', '%s[%s:%s]=%s' % (lib_excel_package.get_cell_value(wb, ws, row=row, column=col), row, col, cellValue))

            cell_list_of_lists.append(cell_list)

        cell_list_of_lists = self.__unicode_to_string(cell_list_of_lists)
        logger.log('debug', 'cellValueList=%s' % cell_list_of_lists)
        return cell_list_of_lists

    def getTable(self, ws_title, searchList=None, extend=True, row_col='row', headers=False, keys=False, emptyCell=False, listDefault=False, hierarchical=False, topLeft=None, bottomRight=None):
        ws_list = self._extractTableList(ws_title, searchList=searchList, extend=extend, row_col=row_col, topLeft=topLeft, bottomRight=bottomRight)
        if not ws_list:
            return
        if hierarchical:
            print 'table method; _getTableDict(listElement=%s)' % listDefault
            tableDict = self._getTableDict(ws_list, listElement=listDefault)
        elif not headers and not keys:
            print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (headers, listDefault)
            tableDict = self._getSimpleTableDict(ws_list, headers=headers, keys=keys, emptyCell=emptyCell, listElement=listDefault)
        elif headers and not keys:
            print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (headers, listDefault)
            tableDict = self._getSimpleTableDict(ws_list, headers=headers, keys=keys, emptyCell=emptyCell, listElement=listDefault)
        elif not headers and keys:
            print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (headers, listDefault)
            tableDict = self._getSimpleTableDict(ws_list, headers=headers, keys=keys, emptyCell=emptyCell, listElement=listDefault)
        else:
            print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (headers, listDefault)
            tableDict = self._getSimpleTableDict(ws_list, headers=headers, keys=keys, emptyCell=emptyCell, listElement=listDefault)
        return tableDict

    def getTableDict(self, ws_title, headerList=None, extend=False, tableType=None, row_col='column', listElement=False, dictDefault=False, topLeft=None, bottomRight=None):
        ws_list = self._extractTableList(ws_title, searchList=headerList, extend=extend, row_col=row_col, topLeft=topLeft, bottomRight=bottomRight)
        if not ws_list:
            return
        else:
            if tableType == None:
                print 'table method; _getTableDict(listElement=%s)' % listElement
                tableDict = self._getTableDict(ws_list, listElement=listElement)
            elif tableType == 'firstHeader':
                print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (True, listElement)
                tableDict = self._getSimpleTableDict(ws_list, headers=True, keys=True, listElement=listElement)
            else:
                print 'table method; _getSimpleTableDict(firstHeader=%s, listElement=%s)' % (False, listElement)
                tableDict = self._getSimpleTableDict(ws_list, headers=False, keys=True, listElement=listElement)
            return tableDict

    def _getSimpleTableDict(self, ws_list, headers=False, emptyCell=False, keys=True, listElement=False):
        table_dict = {}
        tmp_table_dict = {}
        n = 0
        for line in ws_list:
            if any(line):
                tmp_table_dict[n] = line
                n += 1

        if not headers:
            for n in range(len(tmp_table_dict[0])):
                if keys:
                    mainKey = tmp_table_dict[0][n]
                    first_col = 1
                else:
                    mainKey = n
                    first_col = 0
                table_dict[mainKey] = []
                for m in range(first_col, len(tmp_table_dict)):
                    if not emptyCell and tmp_table_dict[m][n] == None:
                        continue
                    table_dict[mainKey].append(tmp_table_dict[m][n])

        else:
            for n in range(1, len(tmp_table_dict[0])):
                if keys:
                    mainKey = tmp_table_dict[0][n]
                    first_col = 1
                else:
                    mainKey = n
                    first_col = 0
                table_dict[mainKey] = {}
                for m in range(first_col, len(tmp_table_dict)):
                    if tmp_table_dict[m][0] != None:
                        key = tmp_table_dict[m][0]
                        table_dict[mainKey][key] = []
                    if tmp_table_dict[m][n] == None:
                        continue
                    table_dict[mainKey][key].append(tmp_table_dict[m][n])

        if not listElement:
            for mainKey, itemDict in table_dict.iteritems():
                if type(itemDict) == list:
                    if len(itemDict) == 1:
                        table_dict[mainKey] = itemDict[0]
                        continue
                if type(itemDict) == list:
                    continue
                for key, valueList in itemDict.iteritems():
                    if len(valueList) == 1:
                        table_dict[mainKey][key] = valueList[0]

        return table_dict

    def _getTableDict(self, ws_list, listElement=False, dd=None, Row=0, Col=0, Depth=0):
        if dd == None:
            dd = {}
        col = Col
        row = Row
        depth = Depth
        while True:
            if col > 0:
                left = self.__getCellValue(ws_list, row, col - 1)
            else:
                left = None
            right = self.__getCellValue(ws_list, row, col + 1)
            under = self.__getCellValue(ws_list, row + 1, col)
            under_leftMost_row, under_leftMost_col = self.__leftMostCell(ws_list, row + 1, col)
            leftMost_row, leftMost_col = self.__leftMostCell(ws_list, row, col)
            if right != None:
                if leftMost_col == col:
                    item = filter(None, ws_list[row][col + 1:])
                    if not listElement and len(item) == 1:
                        item = item[0]
                    dd[ws_list[row][col]] = item
                    row += 1
                if row == len(ws_list):
                    if depth == 0:
                        break
                    depth -= 1
                    return (
                     row, col, depth)
                under_leftMost_row, under_leftMost_col = self.__leftMostCell(ws_list, row, col)
                if under_leftMost_col < col:
                    col -= 1
                    depth -= 1
                    return (
                     row, col, depth)
                if under_leftMost_col == leftMost_col and under_leftMost_row == leftMost_row:
                    print 'Table is not compatible with _getTableDict()'
                    return (None, None, None)
            elif under != None and left == None:
                if under != None:
                    dd[ws_list[row][col]] = None
                    row += 1
            else:
                if right == None and row + 1 == len(ws_list):
                    dd[ws_list[row][col]] = None
                    if depth == 0:
                        break
                    depth -= 1
                    return (
                     row, col, depth)
                if under_leftMost_col <= col:
                    if depth == 0:
                        break
                    col -= 1
                    depth -= 1
                    return (
                     row, col, depth)
                dd[ws_list[row][col]] = {}
                newdd = dd[ws_list[row][col]]
                row += 1
                col += 1
                depth += 1
                row, col, depth = self._getTableDict(ws_list, listElement=listElement, dd=newdd, Row=row, Col=col, Depth=depth)
                if (row, col, depth) == (None, None, None):
                    return (None, None, None)

        return dd

    def __getCellValue(self, ws_list, row, col):
        try:
            line = ws_list[row]
        except:
            return

        if col < 0:
            return
        else:
            if row < 0:
                return
            return line[col]

    def __leftMostCell(self, ws_list, row, col):
        try:
            line = ws_list[row]
        except:
            return (row - 1, col)

        leftMost = 0
        while 1:
            if True:
                if line[leftMost] == None:
                    leftMost += 1
                continue
            return (
             row, leftMost)

        return

    def _extractTableList(self, ws_title, searchList=None, extend=False, row_col='column', topLeft=None, bottomRight=None):
        if searchList == None:
            if topLeft == None:
                logger.log('error', 'When no Header is specified, the table topLeft boundary must be specified.')
                return False
            bottom_right = bottomRight
            if bottomRight == None:
                bottom_right = self.__find_tableBottomEdge(ws_title, topLeft=topLeft, row_col=row_col)
        else:
            topLeft = self.__find_cellLine(ws_title, searchList, row_col=row_col)
            if not topLeft:
                logger.log('warning', 'Headers have not been found. Warning: the headers are case-sensitive.')
                return False
            tableLength = None
            if not extend:
                tableLength = len(searchList)
            bottom_right = self.__find_tableBottomEdge(ws_title, topLeft=topLeft, tableLength=tableLength, row_col=row_col)
        if row_col == 'row':
            row_col = 'column'
        else:
            row_col = 'row'
        cell_table = self.readCellBlock(ws_title, topleft=topLeft, bottomright=bottom_right, row_col=row_col)
        return cell_table

    def __unicode_to_string(self, input, output=None):
        if type(input) == unicode:
            return str(input).strip()
        if type(input) == str:
            return input.strip()
        if type(input) == list:
            for n in range(len(input)):
                if type(input[n]) == unicode:
                    input[n] = str(input[n]).strip()
                elif type(input[n]) == list:
                    input[n] = self.__unicode_to_string(input[n])

            return input
        if type(input) == dict:
            output = {}
            for key in input.keys():
                if type(key) == unicode:
                    output[str(key)] = self.__unicode_to_string(input[key])
                else:
                    output[key] = self.__unicode_to_string(input[key])

            return output

    def __find_tableBottomEdge(self, ws_title, topLeft=None, tableLength=None, row_col='row', litteral=True):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        if row_col == 'row':
            if tableLength == None:
                bottomright = '++'
            else:
                bottomright = '+%s+' % tableLength
            row_T_col = 'col'
        else:
            if tableLength == None:
                bottomright = '++'
            else:
                bottomright = '++%s' % tableLength
            row_T_col = 'row'
        ws_cell = self.readCellBlock(ws_title, topleft=topLeft, bottomright=bottomright, row_col=row_col)
        if tableLength != None:
            for n in range(len(ws_cell)):
                if not any(ws_cell[n][0:tableLength]):
                    break

        else:
            ws_T_cell = self.readCellBlock(ws_title, topleft=topLeft, bottomright=bottomright, row_col=row_T_col)
            foundNone = False
            for m in range(len(ws_T_cell)):
                if not any(ws_T_cell[m][0:tableLength]):
                    foundNone = True
                    break

            if not foundNone:
                m += 1
            tableLength = m
            foundNone = False
            for n in range(len(ws_cell)):
                if not any(ws_cell[n][0:m]):
                    foundNone = True
                    break

        if not foundNone:
            n += 1
        tlCol, ltRow = self.get_cell_coordinate(topLeft, type='number')
        if row_col == 'row':
            row = ltRow + n - 1
            col = tlCol + tableLength - 1
        else:
            col = tlCol + n - 1
            row = ltRow + tableLength - 1
        if litteral:
            colRow = self.get_cell_litteral(col, row)
            return colRow
        else:
            return (
             col, row)

    def __find_cellLine(self, ws_title, cell_line, row_col='row', litteral=True, left_empty=True):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        occur_list = []
        n = 0
        ws_cell = self.readCellBlock(ws_title, topleft='A1', bottomright='++', row_col=row_col)
        for n in range(0, len(ws_cell)):
            lineList = ws_cell[n]
            occur_list = self.___find_sub_list(cell_line, lineList, left_empty=left_empty)
            if occur_list == []:
                continue
            break

        if occur_list == []:
            logger.log('warning', 'Linear cell range %s NOT found in worksheet %s' % (cell_line, ws_title))
            return False
        if row_col == 'row':
            col = occur_list[0][0] + 1
            row = n + 1
        else:
            row = occur_list[0][0] + 1
            col = n + 1
        if litteral:
            colRow = self.get_cell_litteral(col, row)
            return colRow
        return (col, row)

    def ___find_sub_list(self, sl, l, left_empty=True):
        results = []
        sll = len(sl)
        for ind in (i for i, e in enumerate(l) if e == sl[0]):
            if l[ind:ind + sll] == sl:
                if left_empty:
                    try:
                        left_cell = l[ind - 1:ind][0]
                    except:
                        left_cell = None

                    if left_cell == None:
                        results.append((ind, ind + sll - 1))

        return results

    def get_pattern_cell_values(self, ws_title, column_pattern, row_pattern, retval=False):
        col, row = self.search_cell_by_pattern(ws_title, column_pattern, row_pattern, primary='row')
        if (col, row) == (-1, -1):
            if retval:
                return ''
            logger.log('error', 'The row_pattern "%s" in worksheet "%s" was not found!' % row_pattern, ws_title)
            return False
        cell_value = self.readCell(ws_title, col, row)
        logger.log('info', 'msn_pe_port = %s' % cell_value)
        return cell_value

    def search_cell_by_pattern(self, ws_title, col_pattern, row_pattern, primary='row'):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        if primary == 'row':
            primary_pattern = row_pattern
            secondary_pattern = col_pattern
        else:
            primary_pattern = col_pattern
            secondary_pattern = row_pattern
        primary_col = 0
        primary_row = 0
        for row in range(1, lib_excel_package.get_max_row_on_worksheet(self.wb, ws) + 1):
            for col in range(1, lib_excel_package.get_max_column_on_worksheet(self.wb, ws) + 1):
                cellValue = str(lib_excel_package.get_cell_value(self.wb, ws, row=row, column=col))
                if cellValue == None:
                    continue
                if primary_pattern in cellValue:
                    primary_col = col
                    primary_row = row
                    break

            if primary_col != 0:
                break

        if primary_row == 0:
            logger.log('info', 'Pattern %s not found.' % primary_pattern)
            return (-1, -1)
        else:
            secondary_col = 0
            secondary_row = 0
            for col in range(primary_col, lib_excel_package.get_max_row_on_worksheet(self.wb, ws) + 1):
                for row in range(1, lib_excel_package.get_max_column_on_worksheet(self.wb, ws) + 1):
                    cellValue = str(lib_excel_package.get_cell_value(self.wb, ws, row=row, column=col))
                    if cellValue == None:
                        continue
                    if secondary_pattern in cellValue:
                        secondary_col = col
                        secondary_row = row
                        break

                if secondary_col != 0:
                    break

            if secondary_col == 0:
                logger.log('error', 'Pattern %s not found.' % secondary_pattern)
                return (-1, -1)
            return (
             secondary_col, primary_row)

    def get_last_row_in_column(self, ws_title, column, wb=None):
        if wb == None:
            wb = self.wb
        if ws_title in lib_excel_package.get_sheet_name_list(wb):
            ws = lib_excel_package.get_worksheet(wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        col = column
        if not str(col).isdigit():
            col = lib_excel_package.column_letter_to_number(column)
        max_row = lib_excel_package.get_max_row_on_worksheet(wb, ws)
        logger.log('debug', 'max_row = %s' % max_row)
        for index in range(max_row, 0, -1):
            logger.log('debug', 'Column %s row %s:  cell = %s' % (column, index, lib_excel_package.get_cell_value(wb, ws, row=index, column=col)))
            if lib_excel_package.get_cell_value(wb, ws, row=index, column=col) is not None:
                return index

        return 0

    def get_last_column_in_row(self, ws_title, row, type='letter', wb=None):
        if wb == None:
            wb = self.wb
        if ws_title in lib_excel_package.get_sheet_name_list(wb):
            ws = lib_excel_package.get_worksheet(wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        max_col = lib_excel_package.get_max_column_on_worksheet(wb, ws)
        for index in range(max_col, 0, -1):
            logger.log('debug', 'Column %s row %s:  cell = %s' % (index, row, lib_excel_package.get_cell_value(wb, ws, row=row, column=index)))
            if lib_excel_package.get_cell_value(wb, ws, row=row, column=index) is not None:
                if type == 'letter':
                    column = lib_excel_package.column_number_to_letter(index)
                    index = column
                return index

        return 0

    def get_first_non_blank_cell(self, ws_title, type='letter'):
        if ws_title in lib_excel_package.get_sheet_name_list(self.wb):
            ws = lib_excel_package.get_worksheet(self.wb, ws_title)
        else:
            logger.log('error', 'Worksheet [%s] does NOT exist' % ws_title)
            return False
        max_col = lib_excel_package.get_max_column_on_worksheet(self.wb, ws)
        max_row = lib_excel_package.get_max_row_on_worksheet(self.wb, ws)
        for row in range(1, max_row + 1, 1):
            for col in range(1, max_col + 1, 1):
                logger.log('debug', 'Column %s row %s:  cell = %s'(col, row, lib_excel_package.get_cell_value(self.wb, ws, row=row, column=col)))
                if lib_excel_package.get_cell_value(self.wb, ws, row=row, column=col) is not None:
                    column = col
                    if type == 'letter':
                        column = lib_excel_package.column_number_to_letter(col)
                    return (
                     column, row)

        return (-1, -1)

    def get_block_dimension(self, ws_title, t_left, b_right, wb=None):
        if wb == None:
            wb = self.wb
        try:
            col_start, row_start = lib_excel_package.get_coordinate_from_string(t_left, col_type='number')
            col_end, row_end = lib_excel_package.get_coordinate_from_string(b_right)
            col_end = lib_excel_package.column_letter_to_number(col_end)
            col_dim = col_end - col_start + 1
            row_dim = row_end - row_start + 1
        except:
            ll = b_right.split('+')
            if len(ll) > 3:
                print 'Invalid cell: t_left[%s] b_right[%s] ' % (t_left, b_right)
                return (-1, -1)
            if ll[0] != '':
                print 'Invalid cell: t_left[%s] b_right[%s] ' % (t_left, b_right)
                return (-1, -1)
            col_dim = 0
            row_dim = 0
            if ll[1] != '':
                col_dim = int(ll[1])
            if ll[2] != '':
                row_dim = int(ll[2])

        if col_dim == 0 or row_dim == 0:
            ws = lib_excel_package.get_worksheet(wb, ws_title)
            dim = ws.calculate_dimension()
            last_col = dim.split(':')[1][0]
            col_end = lib_excel_package.column_letter_to_number(last_col)
            row_end = int(dim.split(':')[1][1:])
            col_dim = col_end - col_start + 1
            row_dim = row_end - row_start + 1
        logger.log('debug', '%s:%s = (%s, %s)' % (t_left, b_right, col_dim, row_dim))
        return (
         col_dim, row_dim)

    def get_cell_coordinate(self, cell_location_string, type='letter'):
        column, row = lib_excel_package.get_coordinate_from_string(cell_location_string)
        if type != 'letter':
            column = lib_excel_package.column_letter_to_number(column)
        return (
         column, row)

    def get_cell_litteral(self, column, row):
        col_letter = lib_excel_package.column_number_to_letter(column)
        cell_location = col_letter + str(row)
        return cell_location