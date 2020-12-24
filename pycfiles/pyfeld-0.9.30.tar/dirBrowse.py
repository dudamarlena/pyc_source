# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/dirBrowse.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import re, subprocess

def rfCmd():
    return b'pyfeld browse'


class DirLevel:

    def __init__(self, path, friendly_name, items):
        self.path = path
        self.friendly_name = friendly_name
        self.items = items


class DirBrowse:

    def __init__(self):
        dNull = DirLevel(b'0', b'services', self.retrieve(b'0'))
        self.path = b'0'
        self.pathes = [b'0']
        self.dirs = [dNull]
        self.depth = 0
        self.retrieve(self.pathes[self.depth])

    def get_current_path(self):
        return self.path

    @staticmethod
    def split_browse(lines, nextline):
        result = re.match(b'^([C+]) (.*) \\*(.*)$', nextline)
        if result:
            type_string = b''
            if result.group(1) == b'C':
                type_string = b'D'
            if result.group(1) == b'+':
                type_string = b'F'
            path = result.group(2).encode(b'utf-8')
            friendly_name = result.group(3)
            lines.append([type_string, path, friendly_name])

    def enter(self, index):
        self.path = self.dirs[self.depth].items[index][1]
        items = self.retrieve(self.path)
        new_dir = DirLevel(self.path, self.dirs[self.depth].items[index][2], items)
        self.depth += 1
        if len(self.dirs) <= self.depth:
            self.dirs.append(new_dir)
        else:
            self.dirs[self.depth] = new_dir

    def enter_by_friendly_name(self, name):
        pass

    def leave(self):
        if self.depth != 0:
            self.depth -= 1
        self.path = self.dirs[self.depth].path

    def retrieve(self, path):
        command = rfCmd()
        if type(path).__name__ == b'bytes':
            command += b' "' + path.decode(b'utf-8') + b'"'
        else:
            command += b' "' + path + b'"'
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            return 0

        lines = list()
        while True:
            nextline = process.stdout.readline()
            if len(nextline) == 0 and process.poll() != None:
                break
            self.split_browse(lines, nextline.decode(b'utf-8'))

        return lines

    def get_friendly_path_name(self, separator=b' -> '):
        s = b''
        for i in range(1, self.depth + 1):
            s += self.dirs[i].friendly_name + separator

        return s[:-len(separator)]

    def get_friendly_name(self, index):
        return self.dirs[self.depth].items[index][2]

    def get_path_for_index(self, index):
        return self.dirs[self.depth].items[index][1]

    def get_type(self, index):
        return self.dirs[self.depth].items[index][0]

    def max_entries_on_level(self):
        return len(self.dirs[self.depth].items)