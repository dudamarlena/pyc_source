# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/scalrtools/api/view.py
# Compiled at: 2015-05-22 06:53:03
"""
Created on Feb 21th, 2011

@author: Dmytro Korsakov
"""
from prettytable import PrettyTable
from types_ import DynamicScalrObject, Page

class TableViewer:
    data = None

    def __str__(self):
        lines = []
        for (table, text) in self.data.items():
            line = ''
            if text:
                line += '%s\n' % text
            if isinstance(table, PrettyTable):
                line += '%s\n' % table
            lines.append(line)

        return ('\n').join(lines)

    def __init__(self, response):
        """
                data = @dict(table=title)
                """
        self.data = {}
        if response:
            if isinstance(response, list):
                self.data[self.prepare_table(response)] = None
            elif isinstance(response, DynamicScalrObject):
                pt = PrettyTable([response.__title__, 'Value'])
                for (k, v) in response.data:
                    pt.add_row([k, v])

                self.data[pt] = None
            elif isinstance(response, Page):
                objects = response.scalr_objects
                plain_text = 'Total records: %s\nStart:%s\nLimit:%s\n' % (
                 response.total_records,
                 response.start_from,
                 response.records_limit)
                self.data[self.prepare_table(objects) if objects else response.total_records] = plain_text
        return

    def apply_aliases(self, column_names, aliases):
        if aliases:
            for key in aliases:
                if key in column_names:
                    column_names[column_names.index(key)] = aliases[key]

        return column_names

    def get_column_names(self, objects):
        column_names = []
        if objects:
            object = objects[0]
            column_names = object.__titles__.values()
            aliases = object.__aliases__
            return self.apply_aliases(column_names, aliases)

    def prepare_table(self, objects):
        column_names = self.get_column_names(objects)
        pt = PrettyTable(column_names, caching=False)
        if hasattr(pt, 'align'):
            pt.align = 'l'
        for field in column_names:
            pt.set_field_align(field, 'l')

        for scalr_obj in objects:
            row = []
            for attribute in scalr_obj.__titles__.keys():
                cell = getattr(scalr_obj, attribute)
                if isinstance(cell, list):
                    cell = (';').join(cell)
                elif isinstance(cell, dict):
                    cell = (';').join([ '%s=%s' % (k, v) for (k, v) in cell.items() ])
                row.append(cell)

            pt.add_row(row)

        return pt