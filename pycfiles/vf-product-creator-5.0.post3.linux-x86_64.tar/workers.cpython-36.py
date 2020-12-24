# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/workers.py
# Compiled at: 2018-10-04 13:50:12
# Size of source mod 2**32: 1602 bytes
"""
Copyright (2017) Raydel Miranda 

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""
import threading, shutil
from vf_createproducts_core.compose import *

class CopyWorker(threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        (super(CopyWorker, self).__init__)(*args, **kwargs)
        self._CopyWorker__queue = queue

    def run(self):
        while True:
            source, dest = self._CopyWorker__queue.get()
            shutil.copyfile(source, dest)
            self._CopyWorker__queue.task_done()


class ConverterWorker(threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        (super(ConverterWorker, self).__init__)(*args, **kwargs)
        self._ConverterWorker__queue = queue

    def run(self):
        while True:
            images, background, output, verbose = self._ConverterWorker__queue.get()
            compose(images, background, output, verbose)
            self._ConverterWorker__queue.task_done()