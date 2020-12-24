# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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