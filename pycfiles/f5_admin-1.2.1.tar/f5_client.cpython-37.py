# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sli/f5-admin/src/f5_client.py
# Compiled at: 2020-03-10 21:26:55
# Size of source mod 2**32: 14280 bytes
import re, paramiko, getpass, datetime
from .util import *
from os import listdir, unlink, symlink, mkdir
from os.path import isfile, isdir, join, dirname, realpath, getsize

class F5Client:

    def __init__(self, credential, timeout, verbose):
        self.verbose = verbose
        self.credential = credential
        self.node = None
        self.port = 22
        self.timeout = timeout
        self.cache_config_base = dirname(realpath(__file__)) + '/conf/'
        if not is_directory(self.cache_config_base):
            mkdir(self.cache_config_base)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        file = self.cache_config_base

    def load(self, node):
        if not is_valid_hostname(node):
            exit(1)
        else:
            self.node = node.lower().split('.')[0]
            self.cache_config_dir = self.cache_config_base + self.node
            if not is_directory(self.cache_config_dir):
                mkdir(self.cache_config_dir)
            self.cache_config = self.cache_config_dir + '/' + self.node + '.txt'
            print('Loading cache_config: ', self.cache_config)
            isfile(self.cache_config) or self.fetch()
        if getsize(self.cache_config) == 0:
            self.fetch()
        self.top_objs = self.parse_conf_file(self.cache_config)
        print('Loading complete')

    def ssh_connect(self):
        try:
            print('Setting up remote SSH session to host:', self.node)
            if self.credential == None:
                user_name = input('Please enter the F5 user name: ')
                password = getpass.getpass('Please enter the F5 password: ')
                self.credential = {'user_name':str(user_name).strip(), 
                 'user_pass':str(password).strip()}
            else:
                if self.credential['user_name'] == None:
                    user_name = input('Please enter the F5 user name: ')
                    self.credential['user_name'] = str(user_name.strip())
                else:
                    if self.credential['user_pass'] == None:
                        password = getpass.getpass('Please enter the F5 password: ')
                        self.credential['user_pass'] = str(password.strip())
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=(self.node), port=(self.port), username=(self.credential['user_name']), password=(self.credential['user_pass']), timeout=(self.timeout))
            return client
        except Exception as e:
            try:
                print('SSH Connection Failed:', self.node)
                print('Trace Error:', e)
                print('Terminate running program')
                exit(1)
            finally:
                e = None
                del e

    def ssh_command(self, ssh_connect, command_string, sudo_pass):
        try:
            print('Execution on the remote host: ', command_string)
            ssh_connect.invoke_shell()
            stdin, stdout, stderr = ssh_connect.exec_command(command_string)
            cmd_out_list = stdout.readlines()
            cmd_err_list = stderr.readlines()
            print(cmd_out_list)
            if self.verbose:
                print('stderr:', cmd_err_list)
            print('Command execution complete.\n')
            if len(cmd_out_list) > 0:
                return cmd_out_list
            if len(cmd_err_list) > 0:
                return cmd_err_list
            return []
        except Exception as e:
            try:
                print('SSH Command Failed:')
                print(e)
            finally:
                e = None
                del e

    def fetch(self):
        try:
            print('Fetch the running configuration on: ', self.node)
            conn = self.ssh_connect()
            if self.credential['user_name'] == 'root':
                f5_conf = self.ssh_command(conn, 'tmsh list', '')
            else:
                f5_conf = self.ssh_command(conn, 'list', '')
            today = datetime.date.today().strftime('%m%d%Y')
            file = self.cache_config_base + self.node + '/' + self.node + '.' + today
            with open(file, 'wb') as (fd):
                for line in f5_conf:
                    fd.write(line.encode('utf-8').rstrip() + b'\n')

            fd.close()
            conn.close()
            if isfile(self.cache_config):
                unlink(self.cache_config)
            symlink(file, self.cache_config)
            print('F5 running configuration is saved to file: ', self.cache_config)
        except Exception as e:
            try:
                print('Fetch Configuration Failed:')
                print(e)
            finally:
                e = None
                del e

    def parse_conf_file(self, f5_config_file):
        try:
            if self.verbose:
                print('Parsing the f5 running configurations ... ')
            confs = []
            with open(f5_config_file, 'r') as (fd):
                confs = list(fd)
            fd.close()
            top_objs = {}
            recording = False
            p_empty = re.compile('^(\\w+\\s)+.*\\{\\s\\}$', re.M | re.I)
            p_start = re.compile('^(\\w+\\s)+.*\\{$', re.M | re.I)
            p_end = re.compile('^\\}$', re.M | re.I)
            obj = []
            for x in confs:
                if self.verbose:
                    print('Parsing line:', x)
                else:
                    if p_empty.match(x):
                        obj_name = x.split('{')[0].rstrip()
                        obj = []
                        top_objs.update({obj_name: obj})
                        continue
                    if p_end.match(x):
                        if self.count_bracket(obj, '{') > self.count_bracket(obj, '}'):
                            obj.append(x.replace('\n', ''))
                            continue
                        else:
                            top_objs.update({obj_name: obj})
                            obj = []
                            recording = False
                            if self.verbose:
                                print('Next object ...')
                            continue
                if p_start.match(x):
                    recording = True
                if recording:
                    if p_start.match(x):
                        if len(obj) == 0:
                            obj_name = x.split('{')[0].rstrip()
                            if self.verbose:
                                print('Top object name: ', obj_name)
                                continue
                    obj.append(x.replace('\n', ''))
                    continue

            if self.verbose:
                print('Parsing done.\n')
            return top_objs
        except Exception as e:
            try:
                print('Parsing F5 Running Configurations Failed:')
                print(e)
            finally:
                e = None
                del e

    def filter_f5_objs(self, objs, p):
        try:
            if self.verbose:
                print('Filtering F5 objects based on string: ', p)
            my_objs = {}
            for key, val in objs.items():
                if self.verbose:
                    print('Filtering object:', key)
                if p in key:
                    my_objs.update({key: val})
                    continue
                for line in val:
                    if self.verbose:
                        print(line)
                    if p in str(line):
                        if self.verbose:
                            print('Match found: ', line)
                        my_objs.update({key: val})
                        break

            print('Filtering done.\n')
            return my_objs
        except Exception as e:
            try:
                print('Filtering F5 Objects Failed:')
                print(e)
                return
            finally:
                e = None
                del e

    def pattern_filter_f5_objs(self, objs, p):
        try:
            if self.verbose:
                print('Filtering F5 objects based on regex pattern: ', p)
            my_objs = {}
            prog = re.compile(p)
            for key, val in objs.items():
                if self.verbose:
                    print('Filtering object:', key)
                if prog.match(key):
                    my_objs.update({key: val})
                    continue
                for line in val:
                    if self.verbose:
                        print(line)
                    if prog.match(line):
                        if self.verbose:
                            print('Match found: ', line)
                        my_objs.update({key: val})
                        break

            print('Pattern filtering done.\n')
            return my_objs
        except Exception as e:
            try:
                print('Pattern filtering F5 Objects Failed:')
                print(e)
                return
            finally:
                e = None
                del e

    def print_obj(self, key, value):
        if len(value) > 0:
            header = key + ' {'
            footer = '}'
            print(header)
            for x in value:
                print(x)

            print(footer)
        else:
            one_liner = key + ' { }'
            print(one_liner)

    def write_obj(self, key, value, file):
        with open(file, 'a') as (fd):
            if len(value) > 0:
                header = key + ' {'
                footer = '}'
                fd.write(header + '\n')
                for x in value:
                    fd.write(x + '\n')

                fd.write(footer + '\n')
            else:
                one_liner = key + ' { }'
                fd.write(one_liner + '\n')

    def search_desc(self, obj_val):
        for line in obj_val:
            if re.match('    description ', line):
                return line.split('description')[1].strip()

        return ''

    def search_vip(self, obj_val):
        for line in obj_val:
            if re.match('    destination ', line):
                return line.split('destination')[1].split(':')[0].strip()

        return ''

    def search_cert_in_client_ssl_profile(self, obj_val):
        for line in obj_val:
            if re.match('    cert ', line):
                return line.split('cert')[1].strip()

        return ''

    def search_client_ssl(self, obj_val):
        previous_line = ''
        prog = re.compile('            context clientside')
        for line in obj_val:
            if prog.match(line):
                return previous_line.replace('{', '').strip()
            previous_line = line.rstrip()

        return ''

    def search_client_ssl_parent(self, obj_val):
        for line in obj_val:
            if ' defaults-from' in line:
                return line.split('defaults-from')[1].strip()

        return 'N/A'

    def count_bracket(self, obj_val, bracket):
        cnt = 0
        p = re.compile(bracket, re.M | re.I)
        for line in obj_val:
            if bracket in line:
                occur = len(p.findall(line))
                cnt += occur

        return cnt

    def get_node_list(self):
        cache_dirs = [d for d in listdir(self.cache_config_base) if isdir(join(self.cache_config_base, d))]
        return cache_dirs

    def get_cache_file_list(self):
        cache_files = [f for f in listdir(self.cache_config_dir) if isfile(join(self.cache_config_dir, f))]
        return cache_files

    def get_cert_local_path(self, conn, cert_name):
        path_command = 'find / -name *' + cert_name + '*'
        outputs = self.ssh_command(conn, path_command, '')
        if len(outputs) > 0:
            return outputs[0]
        return

    def get_cert_expiration_by_path(self, conn, cert_path):
        path_command = 'openssl x509 -noout -dates -in ' + cert_path.strip()
        outputs = self.ssh_command(conn, path_command, '')
        marker = 'notAfter='
        if len(outputs) > 0:
            for line in outputs:
                if marker in line:
                    return line.replace(marker, '').rstrip()

        else:
            return

    def get_cert_expiration_by_name(self, cert_name):
        key = 'sys file ssl-cert ' + cert_name
        obj_val = self.top_objs[key]
        for line in obj_val:
            if 'expiration-date' in line:
                return line.split('expiration-date')[1].lstrip()