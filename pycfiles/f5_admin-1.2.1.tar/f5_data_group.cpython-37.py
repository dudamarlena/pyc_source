# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sli/f5-admin/src/f5_data_group.py
# Compiled at: 2020-03-10 21:27:59
# Size of source mod 2**32: 7546 bytes
from f5_admin import F5Client
from .util import *
import os
from os import listdir, unlink, symlink, mkdir
import datetime, re

class F5DataGroup(F5Client):

    def __init__(self, credential, timeout, verbose):
        F5Client.__init__(self, credential, timeout, verbose)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        file = self.cache_config_base

    def load(self, node):
        self.node = node.lower()
        if not is_directory(self.cache_config_base + node):
            mkdir(self.cache_config_base + node)
        self.cache_config = self.cache_config_base + node + '/' + node + '.txt'
        print('Loading cache_config: ', self.cache_config)
        if not os.path.isfile(self.cache_config):
            self.fetch()
        if os.path.getsize(self.cache_config) == 0:
            self.fetch()
        self.top_objs = self.parse_conf_file(self.cache_config)
        self.load_dgs(self.node)
        print('Loading complete')

    def load_dgs(self, node):
        self.int_dg_objs = self.filter_f5_objs(self.top_objs, 'ltm data-group internal')
        self.int_dg_list = [f.strip().split(' ')[(-1)] for f in list(self.int_dg_objs.keys())]
        self.ext_dg_objs = self.filter_f5_objs(self.top_objs, 'ltm data-group external')
        self.ext_dg_list = [f.strip().split(' ')[(-1)] for f in list(self.ext_dg_objs.keys())]
        self.cache_dg_dir = self.cache_config_base + node + '/ext_dg/'
        if not is_directory(self.cache_dg_dir):
            mkdir(self.cache_dg_dir)
        self.dgs = {'ext':{},  'int':{}}
        self.load_ext_dg_objs()
        self.load_int_dg_objs()

    def search_dg_file_name(self, obj_val):
        for line in obj_val:
            if re.match('    external-file-name ', line):
                return line.split('external-file-name')[1]

        return ''

    def search_dg_type(self, obj_val):
        for line in obj_val:
            if re.match('    type ', line):
                return line.split('type')[1]

        return ''

    def load_ext_dg_objs(self):
        if self.verbose:
            print('Loading external data group into memory on F5 node: ', self.node)
        for x in list(self.ext_dg_objs.keys()):
            dg_name = x.strip().split(' ')[(-1)]
            dg_file_name = self.search_dg_file_name(self.ext_dg_objs[x])
            cache_dg_file = self.cache_dg_dir + dg_name + '.txt'
            if not is_file(cache_dg_file):
                print('Retrieve the external data group file: ', x)
                contents = self.fetch_ext_dg(dg_file_name, cache_dg_file)
            if is_file(cache_dg_file):
                my_dgs = self.parse_ext_dg_file(cache_dg_file)
                if my_dgs != None:
                    self.dgs['ext'][dg_name] = my_dgs

    def load_int_dg_objs(self):
        if self.verbose:
            print('Loading internl data group into memory on F5 node: ', self.node)
        for x in list(self.int_dg_objs.keys()):
            dg_name = x.strip().split(' ')[(-1)]
            self.dgs['int'][dg_name] = self.int_dg_objs[x]

    def fetch_ext_dg(self, dg_file_name, cache_dg_file):
        today = datetime.date.today().strftime('%m%d%Y')
        file = cache_dg_file.replace('.txt', '') + '.' + today
        p_dg = re.compile('^.*\\_\\d+\\_\\d+$', re.M | re.I)
        if self.verbose:
            print('Retrieve the external data group file: ', dg_file_name)
        conn = self.ssh_connect()
        cmd01 = 'find / -name *' + dg_file_name.strip() + '*'
        files = self.ssh_command(conn, cmd01, '')
        dg_files = [f for f in files if p_dg.match(f.rstrip())]
        if len(dg_files) == 0:
            print('Error retrieving external data group file: ', dg_file_name)
            print('dg_files: ', dg_files)
            conn.close()
            return
        if self.verbose:
            print('dg_files: ', dg_files)
        dg_file = self.dg_select(dg_files, conn)
        if self.verbose:
            print('Found dg file: ', dg_file)
        cmd02 = 'cat ' + dg_file
        contents = self.ssh_command(conn, cmd02, '')
        contents_clean = [f.rstrip() for f in contents]
        conn.close()
        if is_file(cache_dg_file):
            unlink(cache_dg_file)
        if list_to_file(contents_clean, file):
            print('Fetch file success:', file)
            symlink(file, cache_dg_file)
            return True
        print('Fetch file fail: ', cache_dg_file)
        return False

    def dg_select(self, dg_files, conn):
        if len(dg_files) == 1:
            return dg_files[0].rstrip()
        dg = dg_files[0]
        for f in dg_files:
            if self.dg_modify_time(f.rstrip(), conn) > self.dg_modify_time(dg, conn):
                dg = f.rstrip()

        return dg

    def dg_modify_time(self, dg_file, conn):
        timestamp_command = 'stat ' + dg_file
        outputs = self.ssh_command(conn, timestamp_command, '')
        for x in outputs:
            if 'Modify: ' in x:
                return x.split('Modify: ')[1]

    def parse_ext_dg_file(self, ext_dg_file):
        dict = {}
        with open(ext_dg_file, 'r') as (f):
            line = f.readline()
            while line:
                entry = line.replace(',\n', '').split(':=')
                if len(entry) > 1:
                    dict.update({entry[0].strip(): entry[1].strip()})
                else:
                    dict.update({entry[0].strip(): ''})
                line = f.readline()

        return dict

    def search_ext_dg_file_name(self, obj_val):
        for line in obj_val:
            if re.match('    external-file-name ', line):
                return line.split('external-file-name')[1].strip()

        return ''

    def print_ext_dg(self, ext_dg_name):
        if self.dgs['ext'][ext_dg_name]:
            for key, val in self.dgs['ext'][ext_dg_name].items():
                print(key, ':=', val, ',')