# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/JDs.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 3960 bytes
__doc__ = '\nCreated on Sep 16, 2013\n\n@author: "Colin Manning"\n'
import os, json, codecs

class JDs(object):
    """JDs"""
    db_root = ''
    classes = {}
    os_userid = None
    os_groupid = None
    setowner = False

    def ensureDirectoryExists(self, path):
        if not os.path.exists(path):
            os.makedirs(path, mode=493)

    def getPathForId(self, oid):
        sid = str(oid)
        l = len(sid)
        return sid[l - 4:l - 2] + '/' + sid[l - 2:]

    def __init__(self, db_root, os_userid, os_groupid):
        self.db_root = db_root
        self.os_userid = os_userid
        self.os_groupid = os_groupid
        self.setowner = self.os_userid is not None and self.os_groupid is not None
        return

    def register_class(self, class_name):
        class_dir = self.db_root + '/' + class_name
        self.ensureDirectoryExists(class_dir)
        self.classes[class_name] = class_dir

    def create(self, class_name, obj):
        object_dir = self.classes[class_name] + '/' + self.getPathForId(obj['id'])
        self.ensureDirectoryExists(object_dir)
        object_file = object_dir + '/' + str(obj['id']) + '.json'
        with codecs.open(object_file, 'w', 'utf-8') as (f):
            json.dump(obj, f, ensure_ascii=False, indent=3)
            f.close()
            if self.setowner:
                os.chown(object_file, self.os_userid, self.os_groupid)
        return object_dir

    def update(self, class_name, obj):
        object_dir = self.classes[class_name] + '/' + self.getPathForId(obj['id'])
        object_file = object_dir + '/' + str(obj['id']) + '.json'
        os.remove(object_file)
        with codecs.open(object_file, 'w', 'utf-8') as (f):
            json.dump(obj, f, ensure_ascii=False, indent=3)
            f.close()
            if self.setowner:
                os.chown(object_file, self.os_userid, self.os_groupid)
        return object_dir

    def delete(self, class_name, oid):
        object_folder = self.classes[class_name] + '/' + self.getPathForId(oid)
        object_file = object_folder + '/' + str(oid) + '.json'
        os.remove(object_file)

    def fetch(self, class_name, oid):
        result = None
        object_folder = self.classes[class_name] + '/' + self.getPathForId(oid)
        object_file = object_folder + '/' + str(oid) + '.json'
        if os.path.exists(object_file):
            with codecs.open(object_file, 'r', 'utf-8') as (f):
                result = json.load(f)
                f.close()
        return result

    def add_index_entry(self, class_name, field, obj):
        index_file = self.classes[class_name] + 'index_' + field + '.json'

    def remove_index_entry(self, class_name, field, value):
        index_file = self.classes[class_name] + 'index_' + field + '.json'

    def build_index(self, class_name, field):
        index_file = self.classes[class_name] + 'index_' + field + '.json'

    def save_index(self, class_name, field):
        index_file = self.classes[class_name] + 'index_' + field + '.json'

    def load_index(self, class_name, field):
        index_file = self.classes[class_name] + 'index_' + field + '.json'