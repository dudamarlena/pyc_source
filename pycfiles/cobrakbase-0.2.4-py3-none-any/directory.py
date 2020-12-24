# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/pickup/directory.py
# Compiled at: 2016-08-05 01:47:16
import time, os
from utils import log
from app import db, CobraExt

class Directory:

    def __init__(self, path):
        self.path = path

    file_id = 0
    type_nums = {}
    result = {}
    file = []

    def files(self, directory, level=1):
        if level == 1:
            log.debug(directory)
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            file_name, file_extension = os.path.splitext(path)
            self.type_nums.setdefault(file_extension.lower(), []).append(filename)
            if os.path.isdir(path):
                self.files(path, level + 1)
            if os.path.isfile(path):
                path = path.replace(self.path, '')
                self.file.append(path)
                self.file_id += 1
                log.debug(('{0}, {1}').format(self.file_id, path))

    def collect_files(self, task_id=None):
        t1 = time.clock()
        self.files(self.path)
        self.result['no_extension'] = {'file_count': 0, 'file_list': []}
        for extension, values in self.type_nums.iteritems():
            extension = extension.strip()
            self.result[extension] = {'file_count': len(values), 'file_list': []}
            log.debug(('{0} : {1}').format(extension, len(values)))
            if task_id is not None:
                ext = CobraExt(task_id, extension, len(values))
                db.session.add(ext)
            for f in self.file:
                es = f.split(os.extsep)
                if len(es) >= 2:
                    if f.endswith(extension):
                        self.result[extension]['file_list'].append(f)
                else:
                    self.result['no_extension']['file_count'] = int(self.result['no_extension']['file_count']) + 1
                    self.result['no_extension']['file_list'].append(f)

        if task_id is not None:
            db.session.commit()
        t2 = time.clock()
        self.result['file_nums'] = self.file_id
        self.result['collect_time'] = t2 - t1
        return self.result