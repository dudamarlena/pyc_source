# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/gui_dbase_test.py
# Compiled at: 2004-08-27 02:11:56
"""Test GUI browsing of dbase"""
from pytable import dbspecifier, sqlquery, dbresultset, specifierfromoptions
specifier = specifierfromoptions.specifierFromOptions()
if __name__ == '__main__':
    print 'connecting to database', specifier
    (driver, connection) = specifier.connect()
    print 'quering database for schema', driver
    for table in driver.listTables(connection):
        schema = driver.tableStructure(connection, tableName=table)
        break

    print 'got schema', schema.name
    print 'retrieving result-set'
    results = schema.query('SELECT * FROM %(tableName)s;', connection, tableName=table)
    print 'result-set', results
    for row in results:
        print 'row', repr(row)

    from wxoo.table import propertiedview
    from wxPython.wx import *

    class TestApplication(wxPySimpleApp):
        __module__ = __name__

        def OnInit(self):
            wxInitAllImageHandlers()
            frame = wxFrame(NULL, -1, 'test', size=(600, 300))
            panel = propertiedview.CollectionView(frame, value=results)
            frame.Show(1)
            self.SetTopWindow(frame)
            return 1


    app = TestApplication()
    app.MainLoop()