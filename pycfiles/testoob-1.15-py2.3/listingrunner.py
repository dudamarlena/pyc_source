# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/listingrunner.py
# Compiled at: 2009-10-07 18:08:46
"""Runner that lists tests that would be run"""
from baserunner import BaseRunner

class ListingRunner(BaseRunner):
    """Just list the test names, don't run them.
    """
    __module__ = __name__

    def __init__(self, output_format=None):
        self.output_format = output_format
        self.history = _TestHistory()

    def run(self, fixture):
        self.history.record_fixture(fixture.get_fixture())

    def done(self):
        if self.output_format == None:
            print self.history.get_string()
        elif self.output_format.lower() == 'csv':
            print self.history.get_csv()
        return


class _TestHistory:
    __module__ = __name__

    def __init__(self):
        self.modules = {}

    def record_fixture(self, fixture):
        """Store the info about each fixture, to show them later.
        """
        from testoob.reporting import TestInfo
        fixture_info = TestInfo(fixture)
        self._class_function_list(fixture_info).append(fixture_info.funcinfo())

    def get_string(self):
        """Show all test methods.
        """
        result = []
        for (module_name, module_info) in self.modules.items():
            result.append('Module: %s (%s)' % (module_name, module_info['filename']))
            for (class_name, functions) in module_info['classes'].items():
                result.append('\tClass: %s (%d test functions)' % (class_name, len(functions)))
                for func in functions:
                    result.append('\t\t%s()%s%s' % (func[0], func[2], func[1] and ' - ' + func[1] or ''))

        return ('\n').join(result)

    def get_csv(self):
        """Returns a CSV file structure for parsing.
        """
        result = [
         'file,module,class,method,docstring']
        for (module_name, module_info) in self.modules.items():
            for (class_name, functions) in module_info['classes'].items():
                for func in functions:
                    data = [
                     module_info['filename'], module_name, class_name, func[0], func[1]]
                    result.append((',').join(data))

        return ('\n').join(result)

    def _module(self, fixture_info):
        self.modules.setdefault(fixture_info.module(), {'filename': fixture_info.filename(), 'classes': {}})
        return self.modules[fixture_info.module()]

    def _class_function_list(self, fixture_info):
        classes_dict = self._module(fixture_info)['classes']
        classes_dict.setdefault(fixture_info.classname(), [])
        return classes_dict[fixture_info.classname()]

    def _num_functions(self):
        result = 0
        for mod_info in self.modules.values():
            for functions in mod_info['classes'].values():
                result += len(functions)

        return result