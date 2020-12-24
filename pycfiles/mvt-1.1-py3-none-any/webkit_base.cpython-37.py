# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/webkit_base.py
# Compiled at: 2020-02-11 11:39:52
# Size of source mod 2**32: 1779 bytes
import os, glob
from .base import IOSExtraction

class WebkitBase(IOSExtraction):
    __doc__ = 'This class is a base for other WebKit-related modules.'

    def _process_paths(self, root_paths):
        results = {}
        for root_path in root_paths:
            for found_path in glob.glob(os.path.join(self.base_folder, root_path)):
                if not os.path.exists(found_path):
                    continue
                key = os.path.relpath(found_path, self.base_folder)
                if key not in results:
                    results[key] = []
                for name in os.listdir(found_path):
                    if not name.startswith('http'):
                        continue
                    name = name.replace('http_', 'http://')
                    name = name.replace('https_', 'https://')
                    url = name.split('_')[0]
                    if url not in results[key]:
                        results[key].append(url)

                self._check_domains(results[key])

        return results