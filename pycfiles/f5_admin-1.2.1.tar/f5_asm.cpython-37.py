# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sli/f5-admin/src/f5_asm.py
# Compiled at: 2020-03-10 21:27:34
# Size of source mod 2**32: 6638 bytes
from f5_admin import F5Client
from .util import *
import re, datetime, os
from os import listdir, unlink, symlink, mkdir
from os.path import isfile, isdir, join, dirname, realpath, getsize
import xmltodict
from bs4 import BeautifulSoup

class F5Asm(F5Client):

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
        self.load_asm(self.node)
        print('Loading complete')

    def load_asm(self, node):
        self.asm_objs = self.filter_f5_objs(self.top_objs, 'asm policy')
        self.asm_list = [f.strip().split(' ')[(-1)] for f in list(self.asm_objs.keys())]
        self.cache_asm_dir = self.cache_config_base + node + '/asm/'
        if not is_directory(self.cache_asm_dir):
            mkdir(self.cache_asm_dir)
        self.load_asm_objs()

    def load_asm_objs(self):
        if self.verbose:
            print('Loading asm policy elements into memory on F5 node: ', self.node)
        self.asms = {}
        for x in list(self.asm_objs.keys()):
            asm_name = x.strip().split(' ')[(-1)]
            cache_asm_obj_dir = self.cache_asm_dir + asm_name + '/'
            if not is_directory(cache_asm_obj_dir):
                mkdir(cache_asm_obj_dir)
            cache_asm_file = cache_asm_obj_dir + asm_name + '.xml'
            if not is_file(cache_asm_file):
                print('Retrieve the asm policy file: ', asm_name)
                self.fetch_asm_policy(asm_name)

    def fetch_asm_policy(self, asm_name):
        print('Fetch the ASM policy on: ', self.node)
        conn = self.ssh_connect()
        today = datetime.date.today().strftime('%m%d%Y')
        cache_asm_obj_dir = self.cache_asm_dir + asm_name + '/'
        if not is_directory(cache_asm_obj_dir):
            mkdir(cache_asm_obj_dir)
        cache_asm_file = cache_asm_obj_dir + asm_name + '.xml'
        policy_file_name = asm_name + '_' + today + '.xml'
        remote_file = '/var/tmp/' + policy_file_name
        local_file = cache_asm_obj_dir + policy_file_name
        cmd_01 = 'rm -rf ' + remote_file
        cmd_02 = 'tmsh save asm policy ' + asm_name + ' xml-file ' + remote_file
        for cmd in [cmd_01, cmd_02]:
            self.ssh_command(conn, cmd, '')

        cmd_03 = 'sshpass -p "' + self.credential['user_pass'] + '"' + " scp -o 'StrictHostKeyChecking no' -q " + self.credential['user_name'] + '@' + self.node + ':' + remote_file + ' ' + local_file
        if self.verbose:
            print('Run command: ', cmd_03)
        os.system(cmd_03)
        self.ssh_command(conn, cmd_01, '')
        conn.close()
        if isfile(cache_asm_file):
            unlink(cache_asm_file)
        symlink(local_file, cache_asm_file)
        print('F5 asm policy is saved to file: ', cache_asm_file)

    def traverse(self, obj, prev_path='obj', path_repr='{}[{!r}]'.format):
        if isinstance(obj, dict):
            it = list(obj.items())
        else:
            if isinstance(obj, list):
                it = enumerate(obj)
            else:
                yield (
                 prev_path, obj)
                return
        for k, v in it:
            for data in self.traverse(v, path_repr(prev_path, k), path_repr):
                yield data

    def parse_asm_policy(self, asm_xml_file):
        if self.verbose:
            print('Parsing the F5 ASM policy ... ', asm_xml_file)
        else:
            is_file(asm_xml_file) or print('Error file can not be found: ', asm_xml_file)
            return
        with open(asm_xml_file) as (fd):
            doc = xmltodict.parse(fd.read())
        policies = []
        if '/' in asm_xml_file:
            asm_xml_file = asm_xml_file.split('/')[(-1)]
        for path, value in self.traverse(doc, prev_path=(asm_xml_file.split('.')[0])):
            policies.append({path: value})

        return policies

    def xml_find(self, element_name, file):
        with open(file) as (fp):
            soup = BeautifulSoup(fp, 'xml')
            pl = soup.find(element_name)
            if '/' in pl.text:
                name = pl.text.split('/')[(-1)]
            else:
                name = pl.text
        return name