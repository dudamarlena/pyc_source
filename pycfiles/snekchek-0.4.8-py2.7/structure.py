# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/structure.py
# Compiled at: 2020-03-03 07:34:32
""" Common classes and utility functions. """
from __future__ import print_function
import json, os, re, subprocess, sys, typing, snekchek.format

def flatten(nested_list):
    """Flattens a list, ignore all the lambdas."""
    return list(sorted(filter(lambda y: y is not None, list(map(lambda x: nested_list.extend(x) if isinstance(x, list) else x, nested_list)))))


def get_py_files(dir_name):
    """Get all .py files."""
    return flatten([ x for x in [ [ ('{0}/{1}').format(path, f) for f in files if f.endswith('.py') ] for path, _, files in os.walk(dir_name) if not path.startswith('./build')
                                ] if x
                   ])


class ModuleNotInstalled(Exception):
    pass


class CheckHandler(object):

    def __init__(self, file, out_json, out_json_indent=0, check_dir='.', files=None):
        from snekchek.baseconfig import config
        import configobj
        if not os.path.isfile(file):
            print(('config file not found: {0}').format(file))
            if file != '.snekrc':
                print('trying snekrc...')
                if not os.path.isfile('.snekrc'):
                    print('no config found falling back to default')
                else:
                    file = '.snekrc'
            else:
                print('no config found falling back to default')
        self.parser = config
        self.parser.merge(configobj.ConfigObj(file))
        self.fn = file
        self.status_code = 0
        self.logs = {}
        self.current = ''
        self.json = out_json
        self.indent = out_json_indent
        self.files = files or get_py_files(check_dir)
        patt = re.compile('^(?P<package>\\S+?)\\s*(?P<version>\\S+)\\s*$', re.M)
        args = [
         sys.executable, '-m', 'pip', 'list']
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        proc.wait()
        matches = list(patt.finditer(proc.stdout.read().decode()))[2:]
        self.installed = [ p.group('package') for p in matches ]

    def exit(self):
        """Raise SystemExit with correct status code and output logs."""
        total = sum(len(logs) for logs in self.logs.values())
        if self.json:
            self.logs['total'] = total
            print(json.dumps(self.logs, indent=self.indent))
        else:
            for name, log in self.logs.items():
                if not log or self.parser[name].as_bool('quiet'):
                    continue
                print(('[[{0}]]').format(name))
                getattr(snekchek.format, name + '_format')(log)
                print('\n')

            print('-' * 30)
            print('Total:', total)
        sys.exit(self.status_code)

    def run_linter(self, linter):
        """Run a checker class"""
        self.current = linter.name
        if linter.name not in self.parser['all'].as_list('linters') or linter.base_pyversion > sys.version_info:
            return
        if any(x not in self.installed for x in linter.requires_install):
            raise ModuleNotInstalled(linter.requires_install)
        linter.add_output_hook(self.out_func)
        linter.set_config(self.fn, self.parser[linter.name])
        linter.run(self.files)
        self.status_code = self.status_code or linter.status_code

    def out_func(self, data):
        self.logs[self.current] = data


class Linter(object):
    """Common shared class for all linters/stylers/tools"""
    requires_install = []
    base_pyversion = (2, 7, 0)

    def __init__(self):
        self.status_code = 0
        self.hook = None
        self.confpath = None
        self.conf = None
        return

    def add_output_hook(self, func):
        self.hook = func

    def set_config(self, confpath, section):
        self.confpath = confpath
        self.conf = section

    def get_ignored_files(self):
        return []

    def run(self, files):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__.lower()