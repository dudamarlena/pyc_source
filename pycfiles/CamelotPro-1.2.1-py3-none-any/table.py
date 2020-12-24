# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/table.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nA :class:`Table` and a :class:`ColumnGroup` class to define table views that\nare more complex.\n\n'

class ColumnGroup(object):
    """
    A group of columns to be displayed in a table view.  By building a Table
    with multiple column groups, lots of data can be displayed in a limited
    space.
    
        :param verbose_name: the text to be displayed in the tab widget of the
            column group
        :param columns: a list of fields to display within this column group
        :param icon: a :class:`camelot.view.art.Icon` object
        
    .. literalinclude:: ../../test/test_view.py
       :start-after: begin column group
       :end-before: end column group
       
    .. image:: /_static/controls/column_group.png

    """

    def __init__(self, verbose_name, columns, icon=None):
        self.verbose_name = verbose_name
        self.icon = icon
        self.columns = columns

    def get_fields(self):
        """
        :return: an ordered list of field names displayed in the column group
        """
        return self.columns


class Table(object):
    """
    Represents the columns that should be displayed in a table view.
    
        :param columns: a list of strings with the fields to be displayed, or a 
            list of :class:`ColumnGroup` objects
    """

    def __init__(self, columns):
        self.columns = columns

    def get_fields(self):
        """
        :return: a ordered list of field names displayed in the table
        """
        fields = []
        for column in self.columns:
            if isinstance(column, basestring):
                fields.append(column)
            else:
                fields.extend(column.get_fields())

        return fields

    def render(self, item_view, parent=None):
        """
        Create a tab widget that allows the user to switch between column 
        groups.
        
            :param item_view: a :class:`QtGui.QAbstractItemView` object.
            :param parent: a :class:`QtGui.QWidget` object
        """
        pass


def structure_to_table(structure):
    """Convert a python data structure to a table, using the following rules :

   * if structure is an instance of Table, return structure
   * if structure is a list, create a Table from this list
    """
    if isinstance(structure, Table):
        return structure
    return Table(structure)