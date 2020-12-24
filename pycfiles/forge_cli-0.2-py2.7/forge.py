# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forge/forge.py
# Compiled at: 2013-08-16 04:39:31
"""
forge.forge
~~~~~

:copyright: (c) 2010-2013 by Luis Morales
:license: BSD, see LICENSE for more details.
"""
import os, sys, argparse, logging, traceback, inspect
from util import load_class_from_name
from module import Module

class Forge(object):
    """
    Forge class loads and starts modules
    """

    def __init__(self, user, path, modules):
        self.log = logging.getLogger('forge')
        self.modules = modules
        self.user = user
        self.path = path

    def load_include_path(self, path):
        """
        Scan for and add paths to the include path
        """
        if not os.path.isdir(path):
            return
        sys.path.append(path)
        for f in os.listdir(path):
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                self.load_include_path(fpath)

    def load_module(self, fqcn):
        """
        Load Module class named fqcn
        """
        cls = load_class_from_name(fqcn)
        if cls == Module or not issubclass(cls, Module):
            raise TypeError('%s is not a valid Module' % fqcn)
        self.log.debug('Loaded Module: %s', fqcn)
        return cls

    def load_modules(self, path):
        """
        Scan for collectors to load from path
        """
        modules = {}
        if not os.path.exists(path):
            raise OSError('Directory does not exist: %s' % path)
        if path.endswith('tests') or path.endswith('fixtures'):
            return modules
        self.log.debug('Loading Modules from: %s', path)
        for f in os.listdir(path):
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                submodules = self.load_modules(fpath)
                for key in submodules:
                    modules[key] = submodules[key]

            elif os.path.isfile(fpath) and len(f) > 3 and f[-3:] == '.py' and f[0:4] != 'test' and f[0] != '.':
                modname = f[:-3]
                try:
                    mod = __import__(modname, globals(), locals(), ['*'])
                except ImportError:
                    self.log.error('Failed to import module: %s. %s', modname, traceback.format_exc())
                    continue

                self.log.debug('Loaded Module: %s', modname)
                for attrname in dir(mod):
                    attr = getattr(mod, attrname)
                    if inspect.isclass(attr) and issubclass(attr, Module) and attr != Module:
                        fqcn = ('.').join([modname, attrname])
                        try:
                            cls = self.load_module(fqcn)
                            modules[cls.__name__] = cls
                        except Exception:
                            self.log.error('Failed to load Module: %s. %s', fqcn, traceback.format_exc())
                            continue

        return modules

    def init_module(self, cls):
        """
        Initialize module
        """
        module = None
        try:
            module = cls(self.user)
            self.log.debug('Initialized Module: %s', cls.__name__)
        except Exception:
            self.log.error('Failed to initialize Module: %s. %s', cls.__name__, traceback.format_exc())

        return module

    def run(self):
        """
        Load module classes and run them
        """
        modules_path = self.path
        self.load_include_path(modules_path)
        modules = self.load_modules(modules_path)
        for module in self.modules:
            c = self.init_module(modules[module.capitalize()])
            c.execute()


def run():
    """
    executes the recipe list to set the system
    """
    parser = argparse.ArgumentParser(prog='forge', description='forge is a command line tool that allows to execute modules to configure a linux system.', epilog='this epilog whose whitespace will be cleaned up and whose words will be wrapped across a couple lines')
    parser.add_argument('-u', '--user', help='Destination user', type=str, required=True)
    parser.add_argument('-m', '--modules', help='List of modules to execute', nargs='+', type=str, required=True)
    parser.add_argument('-p', '--path', help='path to find modules', type=str, required=True)
    args = parser.parse_args()
    init = Forge(args.user, args.path, args.modules)
    init.run()