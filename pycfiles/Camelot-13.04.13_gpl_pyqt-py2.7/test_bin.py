# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_bin.py
# Compiled at: 2013-04-11 17:47:52
import tempfile, unittest, os

class BinCase(unittest.TestCase):
    """test functions from camelot.bin
    """

    def test_create_new_project(self):
        from camelot.bin.meta import CreateNewProject, templates, NewProjectOptions
        new_project_action = CreateNewProject()
        for step in new_project_action.model_run(None):
            pass

        options = NewProjectOptions()
        options.source = 'new_project'
        new_project_action.start_project(options)
        for filename, _template in templates:
            code = open(os.path.join(options.source, filename.replace('{{options.module}}', options.module))).read()
            if filename.endswith('.py'):
                compile(code, filename, 'exec')

        return