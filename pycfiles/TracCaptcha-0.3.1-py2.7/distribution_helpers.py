# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/lib/distribution_helpers.py
# Compiled at: 2010-09-04 01:54:31
from distutils.command.build import build
import os
from setuptools.command.install_lib import install_lib
__all__ = [
 'commands_for_babel_support', 'i18n_aware_commands']

def is_babel_available():
    try:
        import babel
    except ImportError:
        return False

    return True


def commands_for_babel_support():
    if not is_babel_available():
        return {}
    from babel.messages import frontend as babel
    extra_commands = {'extract_messages': babel.extract_messages, 
       'init_catalog': babel.init_catalog, 
       'update_catalog': babel.update_catalog, 
       'compile_catalog': babel.compile_catalog}
    return extra_commands


def module_for_filename(filename):
    if filename.endswith('.py'):
        filename = filename[:-len('.py')]
    module_name = filename.replace(os.sep, '.')
    package_name = module_name.split('.')[(-1)]
    top_level_module = __import__(module_name)
    module = getattr(top_level_module, package_name)
    return module


def information_from_module(module):
    data = dict()
    for symbol_name in dir(module):
        value = getattr(module, symbol_name)
        if not isinstance(value, basestring):
            continue
        data[symbol_name] = value

    return data


def information_from_file(filename):
    data = dict()
    if os.path.exists(filename):
        execfile(filename, data)
    else:
        data = information_from_module(module_for_filename(filename))
    is_exportable_symbol = lambda key: not key.startswith('_')
    externally_defined_parameters = dict()
    for key, value in data.items():
        if is_exportable_symbol(key):
            externally_defined_parameters[key] = value

    return externally_defined_parameters


def i18n_aware_commands():
    if not is_babel_available():
        return dict()

    class i18n_build(build):
        sub_commands = [
         ('compile_catalog', None)] + build.sub_commands

    class i18n_install_lib(install_lib):

        def run(self):
            self.run_command('compile_catalog')
            install_lib.run(self)

    command_dict = dict(build=i18n_build, install_lib=i18n_install_lib)
    command_dict.update(commands_for_babel_support())
    return command_dict