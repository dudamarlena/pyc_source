# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/.virtualenvs/pyscratch/lib/python3.6/site-packages/common/ini.py
# Compiled at: 2020-03-09 05:22:57
# Size of source mod 2**32: 2500 bytes
import os, sys

class IniFile(object):

    def __init__(self, filename=None):
        self.data = {}
        if filename is not None:
            self.filename = filename
            basename = filename.split('/')[(-1)]
            self.filename = filename
            self.root_dir = self.filename[0:len(filename) - len(basename)]
            if os.path.isfile(filename):
                self.load()

    def load(self):
        f = open(self.filename, 'r')
        for line in f:
            line = line.strip()
            whitespace = False
            comment = False
            header = False
            key = False
            if line == '':
                whitespace = True
            else:
                if line.find('#') == 0:
                    comment = True
                else:
                    if line.startswith('['):
                        if line.endswith(']'):
                            header = True
            if line.find('=') > -1:
                key = True
            if whitespace or comment:
                continue
            else:
                if header:
                    current_header = {}
                    header_key = line.strip('[]')
                    if self.data.get(header_key) is None:
                        self.data[header_key] = {}
                    else:
                        if key:
                            key_name, value = line.split('=', 1)
                            self.data[header_key][key_name] = value

        f.close()

    def save(self):
        f = open(self.filename, 'w')
        for header_key in self.get_headers():
            line = '[' + header_key + ']'
            f.write(line)
            f.write('\n')
            for value_key in self.get_header_keys(header_key):
                value = self.get(header_key, value_key)
                if value is None:
                    value = ''
                line = '{}={}'.format(value_key, value)
                f.write(line)
                f.write('\n')

            f.write('\n')

        f.close()

    def get(self, header, key, default_value=None):
        keys = self.data.get(header) or {}
        return keys.get(key) or default_value

    def set(self, header, key, value):
        keys = self.data.get(header) or {}
        self.data[header] = keys
        keys[key] = str(value)

    def get_headers(self):
        return self.data.keys()

    def get_header_keys(self, header):
        entry = self.data.get(header) or {}
        return entry.keys()

    def get_root_dir(self):
        return self.root_dir