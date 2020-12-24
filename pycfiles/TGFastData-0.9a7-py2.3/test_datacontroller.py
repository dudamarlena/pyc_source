# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\tests\test_datacontroller.py
# Compiled at: 2007-07-14 11:29:05
import turbogears, cherrypy, formmodel, turbogears.testutil as testutil, tgfastdata as fastdata

class TestDataController(testutil.DBTest):
    __module__ = __name__
    model = formmodel

    class MyRoot(turbogears.controllers.RootController):
        __module__ = __name__
        test = fastdata.DataController(sql_class=formmodel.TestStringColWithTitle)

    def test_string_col_with_title(self):
        """ Test case for ticket #272 """
        root = self.MyRoot()
        cherrypy.root = root
        cherrypy.tree.mount_points = {}
        print '\n\nRequest 1'
        testutil.createRequest('/test/')
        print cherrypy.response.body[0]
        assert 'This is the name' in cherrypy.response.body[0]
        print '\n\nRequest 2'
        testutil.createRequest('/test/add')
        print cherrypy.response.body[0]
        assert 'This is the name' in cherrypy.response.body[0]
        formmodel.TestStringColWithTitle(name='testName', age=25)
        testutil.createRequest('/test/1/edit')
        print cherrypy.response.body[0]
        assert 'This is the name' in cherrypy.response.body[0]
        assert 'testName' in cherrypy.response.body[0]
        testutil.createRequest('/test/1/show')
        print cherrypy.response.body[0]
        assert 'testName' in cherrypy.response.body[0]