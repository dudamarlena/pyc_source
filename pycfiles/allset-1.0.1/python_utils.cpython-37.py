# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/python_utils.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 340 bytes
import importlib

def instantiate_class(module_name: str, class_name: str):
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_()


class dummy_context_mgr:

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return False