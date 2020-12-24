# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/finders.py
# Compiled at: 2018-03-27 03:51:51
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import FileSystemFinder as BaseFileSystemFinder, AppDirectoriesFinder as BaseAppDirectoriesFinder
from django.conf import settings
from crum import get_current_request
from layers import get_current_layer_stack

class FileSystemFinder(BaseFileSystemFinder):

    def __init__(self, apps=None, *args, **kwargs):
        super(FileSystemFinder, self).__init__(apps, *args, **kwargs)
        layers = list(get_current_layer_stack(get_current_request()))
        layers.reverse()
        processed = []
        new_locations = []
        for prefix, location in self.locations:
            for layer in layers:
                pth = os.path.join(location, layer)
                if os.path.exists(pth) and pth not in processed:
                    processed.append(pth)
                    new_locations.append(('', pth))

        for location in reversed(new_locations):
            self.locations.insert(0, location)

        for prefix, location in new_locations:
            filesystem_storage = FileSystemStorage(location=location)
            filesystem_storage.prefix = prefix
            self.storages[location] = filesystem_storage


class AppDirectoriesFinder(BaseAppDirectoriesFinder):

    def __init__(self, apps=None, *args, **kwargs):
        super(AppDirectoriesFinder, self).__init__(apps, *args, **kwargs)
        layers = list(get_current_layer_stack(get_current_request()))
        layers.reverse()
        processed = []
        for k, v in list(self.storages.items()):
            for layer in layers:
                pth = os.path.join(v.location, layer)
                if os.path.exists(pth) and pth not in processed:
                    processed.append(pth)
                    self.apps.append(pth)
                    filesystem_storage = FileSystemStorage(location=pth)
                    filesystem_storage.prefix = ''
                    self.storages[pth] = filesystem_storage