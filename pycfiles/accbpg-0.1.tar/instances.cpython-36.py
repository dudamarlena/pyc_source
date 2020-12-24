# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\accasim\experimentation\instances.py
# Compiled at: 2018-06-18 10:37:13
# Size of source mod 2**32: 2197 bytes
__doc__ = '\nMIT License\n\nCopyright (c) 2017 cgalleguillosm\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
from accasim.utils.file import file_exists, dir_exists

class InstanceReader:

    def __init__(self):
        pass


class InstanceWriter:

    def __init__(self):
        pass


class InstanceGenerator:

    def __init__(self, name, overwrite=False):
        self.name = name
        self.overwerite = overwrite
        self.n_instances = 0

    def running_jobs(self, running_jobs):
        self.data['running_jobs'] = running_jobs
        self._check_data()

    def queued_jobs(self, queued_jobs):
        self.data['queued_jobs'] = queued_jobs
        self._check_data()

    def _read(self):
        pass

    def _write(self):
        self.n_instances += 1

    def _check_data(self):
        attrs = [
         'running_jobs', 'queued_jobs']
        if attr in attrs:
            if attr not in self.data:
                return False
        return self._write()

    def store(self, **kwargs):
        for k, v in kwargs.items():
            getattr(self, k)(v)