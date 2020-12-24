# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2Excel\xmind2Excel\libs\xmind2xlsnew.py
# Compiled at: 2019-07-02 06:05:42
# Size of source mod 2**32: 4381 bytes
__author__ = '8034.com'
__date__ = '2018-10-22'
import sys, os, xmind
from xmind.core import workbook, saver
from xmind.core.topic import TopicElement
import json, xlrd, xlwt
import xlutils.copy as xlscopy

class XmindParse(object):
    source_xmind_file = None
    xmind_workbook = None

    def __init__(self, xmind_path):
        self.source_xmind_file = xmind_path
        self.xmind_workbook = xmind.load(self.source_xmind_file)
        if not self.xmind_workbook:
            raise Exception('xmind文件解析异常。请确认xmind文件路径.')

    def get_sheet_by_name(self, sheet_name):
        for sheet in self.xmind_workbook.getSheets():
            if sheet.getTitle() == sheet_name:
                return sheet

    def get_primary_sheet(self):
        return self.xmind_workbook.getPrimarySheet()

    def show_sheets_info(self):
        xmind_workbook_info = {}
        index = 0
        for sheet in self.xmind_workbook.getSheets():
            xmind_workbook_info[index] = sheet.getTitle()
            index = index + 1

        return xmind_workbook_info

    def get_ponit_info(self, topic):
        point = {}
        point['title'] = topic.getTitle()
        point['notes'] = topic.getNotes()
        point['marker'] = None
        if topic.getMarkers():
            topic_marker_id = topic.getMarkers()[0].getMarkerId()
            topic_marker_name = self.switch_priority(topic_marker_id)
            point['marker'] = topic_marker_name
        return point

    def parse_topic_tree(self, _root_topic, _to_excel_row):
        _point_info = self.get_ponit_info(_root_topic)
        _to_excel_row.append(_point_info)
        sub_topic_list = _root_topic.getSubTopics()
        if not sub_topic_list:
            yield _to_excel_row
        else:
            for topic in sub_topic_list:
                copy_to_excel_row = _to_excel_row.copy()
                to_excel_row = self.parse_topic_tree(topic, copy_to_excel_row)
                for i in to_excel_row:
                    yield i

    def parse_xmind(self, sheet):
        to_excel_row = []
        root_topic = sheet.getRootTopic()
        to_excel_row = self.parse_topic_tree(root_topic, to_excel_row)
        for i in to_excel_row:
            print('parse_xmind.to_excel_row >> {}'.format(i))

        return to_excel_row

    def addCasetoworkbook(self, case, to_workbook, srows):
        case_sheet = to_workbook.get_sheet(0)
        case_sheet.write(srows, 0, case['group'])
        case_sheet.write(srows, 1, case['title'])
        case_sheet.write(srows, 2, case['priority'])
        case_sheet.write(srows, 3, case['pestep'])
        case_sheet.write(srows, 4, case['step'])
        case_sheet.write(srows, 5, case['expect'])
        case_sheet.write(srows, 6, case['remarks'])
        case_sheet.write(srows, 7, case['upload'])
        return srows + 1

    def switch_priority(self, xmind_priority):
        if xmind_priority == 'priority-1':
            return '高'
        if xmind_priority == 'priority-2':
            return '中'
        if xmind_priority == 'priority-3':
            return '低'
        return '中'

    def fit_step(self, mainstep, substep):
        separator = '\n==========\n'
        full_step = mainstep + separator + substep
        return full_step

    def fit_title(self, title, num):
        return title + ' 组用例-%d' % num


if __name__ == '__main__':
    pass