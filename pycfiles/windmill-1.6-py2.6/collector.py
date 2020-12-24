# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_functest/collector.py
# Compiled at: 2011-01-13 01:48:00
import os, sys, inspect, new, imp, copy
from time import sleep

class Collector(object):
    post_collection_functions = []

    def import_module(self, path):
        if os.path.isfile(path):
            sys.path.insert(0, os.path.dirname(path))
            name = os.path.split(path)[(-1)].split('.')[0]
            (filename, pathname, description) = imp.find_module(name, [os.path.dirname(path)])
            module = imp.load_module(name, filename, pathname, description)
            module.functest_module_path = path
            module.__file__ = os.path.abspath(path)
            sys.path.pop(0)
        elif os.path.isdir(path):
            if os.path.isfile(os.path.join(path, '__init__.py')):
                sys.path.insert(0, os.path.abspath(os.path.join(path, os.path.pardir)))
                name = os.path.split(path)[(-1)]
                (filename, pathname, description) = imp.find_module(name, [os.path.abspath(os.path.join(path, os.path.pardir))])
                module = imp.load_module(name, filename, pathname, description)
                module.functest_module_path = path
                module.__file__ = os.path.abspath(os.path.join(path, '__init__.py'))
                sys.path.pop(0)
            else:
                module = new.module(os.path.split(path)[(-1)])
                module.functest_module_path = path
        else:
            raise ImportError('path is not file or directory')
        return module

    def create_module_chain(self, path):
        path = os.path.abspath(path)
        module_chain = []
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        while os.path.isfile(os.path.join(path, '__init__.py')):
            module_chain.append(self.import_module(path))
            path = os.path.join(*os.path.split(path)[:-1])

        module_chain.reverse()
        return module_chain

    def create_test_module(self, path):
        path = os.path.abspath(path)
        if os.path.isfile(path):
            test_module = self.import_module(path)
            for func in self.post_collection_functions:
                func(test_module)

        elif os.path.isdir(path):
            test_module = self.import_module(path)
            for func in self.post_collection_functions:
                func(test_module)

            for filename in [ f for f in os.listdir(path) if not f.startswith('.') if f.startswith('test') if f.endswith('.py') or os.path.isdir(os.path.join(path, f)) and os.path.isfile(os.path.join(path, f, '__init__.py'))
                            ]:
                setattr(test_module, filename.split('.')[0], self.create_test_module(os.path.join(path, filename)))

        else:
            sys.__stdout__.write(path + ' is not a valid python module path or filename\n')
            sys.__stdout__.flush()
            sleep(0.5)
            sys.exit()
        return test_module


def register_post_collection(func):
    test_collector.post_collection_functions.append(func)