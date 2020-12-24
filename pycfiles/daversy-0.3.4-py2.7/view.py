# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\view.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import ViewColumn, View
from column import ViewColumnBuilder

class ViewBuilder(object):
    """Represents a builder for a database view."""
    DbClass = View
    XmlTag = 'view'
    Query = "\n        SELECT v.view_name, v.text, c.comments\n        FROM   sys.user_views v, sys.user_tab_comments c\n        WHERE  v.view_name = c.table_name\n        AND    c.table_type = 'VIEW'\n        ORDER BY v.view_name\n    "
    PropertyList = odict((
     'VIEW_NAME', Property('name')), (
     'TEXT', Property('definition', cdata=True)), (
     'COMMENTS', Property('comment')))

    @staticmethod
    def addToState(state, view):
        view.definition = trim_spaces(view.definition)
        view.comment = trim_spaces(view.comment)
        state.views[view.name] = view

    @staticmethod
    def createSQL(view):
        template = '\nCREATE OR REPLACE FORCE VIEW %(name)s (\n  %(column_sql)s\n)\nAS\n%(definition)s\n/\n'
        column_sql = (',\n  ').join([ column.name for column in view.columns.values() ])
        return render(template, view, column_sql=column_sql)

    @staticmethod
    def commentSQL(view):
        template = "COMMENT ON TABLE %(name)s IS '%(comment)s';"
        result = []
        if view.comment:
            result.append(render(template, view, comment=sql_escape(view.comment)))
        for column in view.columns.values():
            col_comment = ViewColumnBuilder.commentSQL(view, column)
            if col_comment:
                result.append(col_comment)

        return result