# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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