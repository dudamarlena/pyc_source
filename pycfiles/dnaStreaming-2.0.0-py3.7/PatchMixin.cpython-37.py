# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/test/PatchMixin.py
# Compiled at: 2020-05-08 11:21:40
# Size of source mod 2**32: 1196 bytes
from __future__ import absolute_import, division, print_function
from unittest import mock
from mock import patch

class PatchMixin(object):
    __doc__ = '\n    Testing utility mixin that provides methods to patch objects so that they\n    will get unpatched automatically.\n    '

    def patch_module(self, module, return_value=None):
        if str(getattr(module, '__class__')) == "<type 'instancemethod'>":
            mock = self.patch_object(getattr(module, '__self__'), getattr(module, '__name__'))
        else:
            module_path = '{0}.{1}'.format(getattr(module, '__module__'), getattr(module, '__name__'))
            mock = self.patch(module_path)
        mock.return_value = return_value
        return mock

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_object(self, *args, **kwargs):
        patcher = (patch.object)(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_dict(self, *args, **kwargs):
        patcher = (patch.dict)(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()